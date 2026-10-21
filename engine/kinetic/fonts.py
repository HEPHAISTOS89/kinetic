"""Split a TrueType/OpenType collection (.ttc) into standalone fonts (stdlib only).

macOS ships many of the native faces Kinetic deals (Charter, Avenir Next,
Copperplate, Didot…) as .ttc collections, which Flutter and React Native
cannot load. `kinetic font split` writes one .ttf/.otf per face, named by its
PostScript name, so a dealt type system can be bundled for renders and builds.
Licensing is the project's responsibility: Apple faces may be used on Apple
platforms; bundle the dealt Android/OFL face for Android builds."""
from __future__ import annotations

import os
import re
import struct


def _ps_name(data: bytes, tables: dict) -> str:
    if b"name" not in tables:
        return ""
    off, _ = tables[b"name"]
    _, count, str_off = struct.unpack(">HHH", data[off:off + 6])
    best = ""
    for i in range(count):
        pid, eid, lid, nid, ln, so = struct.unpack(">HHHHHH", data[off + 6 + 12 * i: off + 18 + 12 * i])
        if nid not in (6, 4):
            continue
        raw = data[off + str_off + so: off + str_off + so + ln]
        try:
            s = raw.decode("utf-16-be") if pid in (0, 3) else raw.decode("mac_roman")
        except UnicodeDecodeError:
            continue
        if nid == 6:
            return s
        best = best or s
    return best


def split(path: str, out_dir: str) -> list:
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:4] != b"ttcf":
        raise ValueError(f"{path}: not a font collection (.ttc)")
    n = struct.unpack(">I", data[8:12])[0]
    offsets = struct.unpack(f">{n}I", data[12:12 + 4 * n])
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for i, base in enumerate(offsets):
        sfnt, num = struct.unpack(">IH", data[base:base + 6])
        recs, tables = [], {}
        for t in range(num):
            tag, csum, toff, tlen = struct.unpack(">4sIII", data[base + 12 + 16 * t: base + 28 + 16 * t])
            recs.append((tag, csum, toff, tlen))
            tables[tag] = (toff, tlen)
        head = struct.pack(">IHHHH", sfnt, num, *data[base + 6:base + 12] and struct.unpack(">HHH", data[base + 6:base + 12]))
        body, dir_entries = b"", b""
        cursor = 12 + 16 * num
        for tag, csum, toff, tlen in sorted(recs):
            chunk = data[toff:toff + tlen]
            pad = (-len(chunk)) % 4
            dir_entries += struct.pack(">4sIII", tag, csum, cursor + len(body), tlen)
            body += chunk + b"\0" * pad
        name = _ps_name(data, tables) or f"{os.path.splitext(os.path.basename(path))[0]}-{i}"
        name = re.sub(r"[^\w.-]+", "-", name)
        ext = ".otf" if sfnt == 0x4F54544F else ".ttf"
        dest = os.path.join(out_dir, name + ext)
        with open(dest, "wb") as fh:
            fh.write(head + dir_entries + body)
        written.append(dest)
    return written
