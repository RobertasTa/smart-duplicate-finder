# Engine tests - self-contained (create their own temp data, no fixtures dir).
# Run: pytest tests/  (CI: .github/workflows/tests.yml, QT not required here)
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import duplicate_engine as de


def _write(tmp, name, data):
    p = tmp / name
    p.write_bytes(data)
    return p


def test_size_candidates_skips_empty_and_singles(tmp_path):
    _write(tmp_path, "a.txt", b"x" * 100)
    _write(tmp_path, "b.txt", b"y" * 100)
    _write(tmp_path, "empty1.txt", b"")
    _write(tmp_path, "empty2.txt", b"")
    _write(tmp_path, "solo.txt", b"z" * 50)
    files, skipped = de.scan_folders_stats([str(tmp_path)])
    cands = de.size_candidates(files)
    assert len(cands) == 1                       # only the 100-byte size bucket
    assert skipped == 0


def test_hash_groups_freeable_excludes_hardlinks(tmp_path):
    a = _write(tmp_path, "a.bin", b"x" * 1000)
    _write(tmp_path, "b.bin", b"x" * 1000)
    hard = tmp_path / "hard.bin"
    os.link(a, hard)                             # same physical file as a.bin
    files, _ = de.scan_folders_stats([str(tmp_path)])
    res = de.hash_groups(de.size_candidates(files), total_files=len(files))
    st = res["stats"]
    assert len(res["groups"]) == 1
    assert len(res["groups"][0]) == 3            # all three paths reported
    # duplicated: 3 copies x 1000 B; freeable: only ONE physical extra copy
    assert st["duplicated_mb"] == round(3000 / 1024 / 1024, 2)
    assert st["freeable_mb"] == round(1000 / 1024 / 1024, 2)


def test_hash_groups_prefix_filter_correctness(tmp_path):
    big = b"A" * (5 * 1024 * 1024)               # above _PREFIX_RIBA
    _write(tmp_path, "v1.bin", big)
    _write(tmp_path, "v2.bin", big)
    _write(tmp_path, "tail_diff.bin", big[:-1] + b"B")   # same 64K prefix
    _write(tmp_path, "head_diff.bin", b"B" + big[1:])    # differs in prefix
    files, _ = de.scan_folders_stats([str(tmp_path)])
    prog = []
    res = de.hash_groups(de.size_candidates(files), total_files=len(files),
                         progress_cb=lambda d, t: prog.append((d, t)))
    names = sorted(os.path.basename(p) for g in res["groups"] for p in g)
    assert names == ["v1.bin", "v2.bin"]
    assert prog[-1][0] == prog[-1][1]            # progress reaches 100%


def test_find_suspects_returns_truncation_flag(tmp_path):
    _write(tmp_path, "report.txt", b"a" * 1000)
    _write(tmp_path, "report (1).txt", b"b" * 1050)     # same norm name, ~size
    files, _ = de.scan_folders_stats([str(tmp_path)])
    suspects, truncated = de.find_suspects(files)
    assert truncated is False
    assert len(suspects) == 1
    assert suspects[0]["size_a"] != suspects[0]["size_b"]


def test_junk_detection_needs_magic_bytes(tmp_path):
    fake = _write(tmp_path, "Thumbs.db", b"not a real thumbs cache")
    real = _write(tmp_path, "sub", b"")  # placeholder; rewrite below
    real.unlink()
    sub = tmp_path / "sub"
    sub.mkdir()
    real = _write(sub, "Thumbs.db", b"\xd0\xcf\x11\xe0" + b"\x00" * 16)
    assert de.is_junk_name(str(fake)) and de.is_junk_name(str(real))
    assert de.verify_junk(str(fake)) is False    # name alone is NOT enough
    assert de.verify_junk(str(real)) is True


def test_visual_finds_exif_rotated_copy(tmp_path):
    PIL = pytest.importorskip("PIL")
    from PIL import Image
    # deterministic non-uniform image (gradient + stripes)
    im = Image.new("RGB", (320, 240))
    px = im.load()
    for x in range(320):
        for y in range(240):
            px[x, y] = (x % 256, (y * 2) % 256, (x * y) % 256)
    a = tmp_path / "orig.jpg"
    im.save(a, quality=90)
    # camera-style rotated copy: pixels rotated 90 CCW + Orientation=6 tag
    rot = im.rotate(90, expand=True)
    exif = Image.Exif()
    exif[274] = 6
    b = tmp_path / "rotated.jpg"
    rot.save(b, quality=90, exif=exif)
    groups = de.find_similar_images([(str(a), 1), (str(b), 1)])
    assert len(groups) == 1 and len(groups[0]) == 2


def _image_with_hash(hv, scale=10):
    """Build a picture whose dHash is exactly hv.

    Mirrors the engine's fingerprint: bit = left pixel brighter than right,
    read row by row from the most significant bit. Starting at 128 and
    stepping by 8 keeps every value inside 0..255.
    """
    from PIL import Image
    img = Image.new("L", (9, 8))
    px = img.load()
    bit = 63
    for r in range(8):
        v = 128
        px[0, r] = v
        for c in range(8):
            v = v - 8 if (hv >> bit) & 1 else v + 8
            bit -= 1
            px[c + 1, r] = v
    return img.resize((9 * scale, 8 * scale), Image.NEAREST)


def test_crowded_bucket_still_reports_similar_pairs(tmp_path):
    """A crowded fingerprint bucket must not swallow similar pictures.

    All fingerprints share their lower 48 bits, so three of the four 16-bit
    chunks land in the same bucket. With the old ceiling of 300 those buckets
    were skipped without a word, and near-identical pictures vanished from
    the results.
    """
    base = 0x0000_1234_5678_9ABC & ((1 << 48) - 1)
    files = []
    for i in range(320):
        hv = base | (i << 48)
        p = tmp_path / f"p{i:03d}.png"
        _image_with_hash(hv).save(p)
        files.append((str(p), 1))

    stats = {}
    groups = de.find_similar_images(files, stats_out=stats)

    # p000 and p001 differ by a single bit - they belong together
    joined = {os.path.basename(f) for g in groups for f in g}
    assert "p000.png" in joined and "p001.png" in joined
    # and nothing was dropped silently
    assert stats.get("skipped_buckets", 0) == 0
    assert stats.get("skipped_pictures", 0) == 0


def test_bucket_ceiling_is_reported_when_reached(tmp_path):
    """When the ceiling really is hit, the caller must be told."""
    base = 0x0000_1234_5678_9ABC & ((1 << 48) - 1)
    files = []
    for i in range(5):
        p = tmp_path / f"q{i}.png"
        _image_with_hash(base | (i << 48)).save(p)
        files.append((str(p), 1))

    stats = {}
    de.find_similar_images(files, stats_out=stats, max_bucket=1)
    assert stats["skipped_buckets"] >= 1
    assert stats["skipped_pictures"] >= 3


def _gradient_image(w=320, h=240):
    from PIL import Image
    im = Image.new("RGB", (w, h))
    px = im.load()
    for x in range(w):
        for y in range(h):
            px[x, y] = ((x * 3) % 256, (y * 5) % 256, ((x + y) * 2) % 256)
    return im


def test_finds_physically_rotated_copies(tmp_path):
    """A copy turned on its side is still the same picture.

    EXIF orientation only covers pictures the camera tagged. Once the pixels
    themselves are rewritten - by an editor, a chat app or a scanner - the
    tag is gone and the fingerprint changes completely.
    """
    from PIL import Image
    im = _gradient_image()
    a = tmp_path / "orig.jpg"
    im.save(a, quality=92)
    b = tmp_path / "turned.jpg"                      # no EXIF tag at all
    im.transpose(Image.ROTATE_90).save(b, quality=92)
    c = tmp_path / "mirrored.jpg"
    im.transpose(Image.FLIP_LEFT_RIGHT).save(c, quality=92)

    # a different picture that must NOT be dragged in: turning a fingerprint
    # loses detail, so two unrelated pictures can drift together once both are
    # turned. Only upright-against-turned is compared, never turned-against-turned.
    other = _gradient_image(300, 300)
    px = other.load()
    for x in range(300):
        for y in range(300):
            px[x, y] = ((x * 11) % 256, (y * 2) % 256, (x + 2 * y) % 256)
    d = tmp_path / "unrelated.jpg"
    other.save(d, quality=92)

    stats = {}
    groups = de.find_similar_images(
        [(str(a), 1), (str(b), 1), (str(c), 1), (str(d), 1)], stats_out=stats)

    assert len(groups) == 1, "the three variants belong together"
    assert len(groups[0]) == 3, "and the unrelated picture stays out"
    assert "unrelated.jpg" not in {os.path.basename(f) for f in groups[0]}
    # Three different orientations and no majority: the program must not
    # guess which one is "right", so it flags them all and lets the person
    # decide. (Robertas' live test 2026-08-26 caught the earlier version
    # pinning the note on whichever file came first - sometimes the original.)
    turned = {os.path.basename(f) for f in stats.get("rotated_files", [])}
    assert turned == {"orig.jpg", "turned.jpg", "mirrored.jpg"}


def test_only_the_odd_one_out_is_flagged_when_there_is_a_majority(tmp_path):
    """With a clear majority, only the pictures that differ are named."""
    from PIL import Image
    im = _gradient_image()
    upright = []
    for n, q in ((1, 92), (2, 88), (3, 84)):          # three upright copies
        p = tmp_path / f"upright{n}.jpg"
        im.save(p, quality=q)
        upright.append(p)
    turned = tmp_path / "turned.jpg"
    im.transpose(Image.ROTATE_270).save(turned, quality=92)

    stats = {}
    de.find_similar_images(
        [(str(x), 1) for x in upright] + [(str(turned), 1)], stats_out=stats)
    flagged = {os.path.basename(f) for f in stats.get("rotated_files", [])}
    assert flagged == {"turned.jpg"}


def test_upright_copies_are_not_reported_as_turned(tmp_path):
    """Plain copies must not be labelled as turned."""
    im = _gradient_image()
    a = tmp_path / "one.jpg"
    im.save(a, quality=92)
    b = tmp_path / "two.jpg"
    im.save(b, quality=88)                            # same picture, requeezed

    stats = {}
    groups = de.find_similar_images(
        [(str(a), 1), (str(b), 1)], stats_out=stats)
    assert len(groups) == 1
    assert stats.get("rotated_files") == []


def test_pletiniai_kelias_dev_mode_points_to_source_dir():
    p = de.pletiniai_kelias()
    assert p.name == "pletiniai.json"
    assert p.parent == Path(de.__file__).resolve().parent


def test_unopenable_pictures_are_reported_not_swallowed(tmp_path):
    """A picture the program cannot open must still be accounted for.

    Damaged files, unknown formats and enormous images (Pillow refuses
    anything past twice its pixel ceiling) all end up in the same place.
    Until 2026-08-26 they were caught and forgotten, so a scan could quietly
    look at fewer pictures than the user handed it.
    """
    good = tmp_path / "good.jpg"
    _gradient_image().save(good, quality=90)
    broken = tmp_path / "broken.jpg"
    broken.write_bytes(b"this is not a picture at all")
    empty = tmp_path / "empty.png"
    empty.write_bytes(b"")

    stats = {}
    de.find_similar_images(
        [(str(good), 1), (str(broken), 1), (str(empty), 1)], stats_out=stats)
    names = {os.path.basename(p) for p in stats.get("unreadable_pictures", [])}
    assert names == {"broken.jpg", "empty.png"}


def _photolike_image(w=800, h=600):
    """Smooth, photo-like content.

    A fine repeating pattern (like a raw gradient) aliases when shrunk and
    changes its own fingerprint by a dozen bits - that says nothing about
    the program. Real photographs are smooth at that scale, so tests about
    resizing must use something that behaves like one.
    """
    import math
    from PIL import Image
    im = Image.new("RGB", (w, h))
    px = im.load()
    for x in range(w):
        for y in range(h):
            v = int(127 + 100 * math.sin(x / 40.0) * math.cos(y / 33.0)
                    + 30 * math.sin(x / 7.0))
            v = max(0, min(255, v))
            px[x, y] = (v, max(0, min(255, int(v * 0.8 + 40))),
                        max(0, min(255, int(v * 0.6 + 70))))
    return im


def test_a_half_size_copy_is_still_found(tmp_path):
    from PIL import Image
    """Resizing must not break recognition - it is the commonest case.

    A picture shrunk by half and re-compressed is still the same picture,
    and the fingerprint has always caught it. Guarded here because on
    2026-08-26 a change made for turned copies quietly broke exactly this:
    the difference grew from 3 bits to 4, and 3 is the limit. Robertas
    asked "will it miss pictures at a different scale?" - it had started to.
    """
    im = _photolike_image(800, 600)
    full = tmp_path / "full.jpg"
    im.save(full, quality=95)
    half = tmp_path / "half.jpg"
    im.resize((400, 300), Image.LANCZOS).save(half, quality=88)

    groups = de.find_similar_images([(str(full), 1), (str(half), 1)])
    assert len(groups) == 1 and len(groups[0]) == 2


def test_upright_fingerprint_is_unchanged_by_rotation_support(tmp_path):
    """The upright fingerprint must stay exactly what it was before v1.5.

    Rotation support hangs beside the old path, never through it. If this
    ever fails, every earlier comparison silently changed meaning.
    """
    from PIL import Image as _Image, ImageOps as _ImageOps
    im = _gradient_image(640, 480)
    p = tmp_path / "one.jpg"
    im.save(p, quality=92)

    # the pre-v1.5 recipe, spelled out
    with _Image.open(p) as src:
        src.draft("L", (9, 8))
        src = _ImageOps.exif_transpose(src)
        g = src.convert("L").resize((9, 8), _Image.LANCZOS)
        px = list(g.getdata())
        senas = 0
        for r in range(8):
            for c in range(8):
                senas = (senas << 1) | (1 if px[r * 9 + c] > px[r * 9 + c + 1] else 0)

    stats = {}
    de.find_similar_images([(str(p), 1)], stats_out=stats)
    # engine's own upright fingerprint for the same file
    from PIL import Image as I2, ImageOps as O2
    with I2.open(p) as src:
        src.draft("L", (32, 32))
        src = O2.exif_transpose(src)
        g2 = src.convert("L").resize((9, 8), I2.LANCZOS)
        px2 = list(g2.getdata())
        naujas = 0
        for r in range(8):
            for c in range(8):
                naujas = (naujas << 1) | (1 if px2[r * 9 + c] > px2[r * 9 + c + 1] else 0)
    assert naujas == senas, "the upright fingerprint changed"
