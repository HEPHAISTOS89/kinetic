"""Contact sheet: every render of a design in one PNG (stdlib only).

Critics judge single screenshots; users meet a system. One sheet shows
sameness (every screen the same template), drift (two screens that look like
two apps) and whether the identity survives the boring states. Decodes 8-bit
non-interlaced PNG (grey, RGB, palette, grey+alpha, RGBA), box-downscales,
composites on a neutral ground, encodes RGB."""
from __future__ import annotations

import os
import struct
import zlib

GROUND = (128, 128, 128)
GAP = 12


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def read_png(path: str):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos, idat, plte, trns = 8, [], None, None
    w = h = depth = ctype = interlace = 0
    while pos < len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif typ == b"PLTE":
            plte = body
        elif typ == b"tRNS":
            trns = body
        elif typ == b"IDAT":
            idat.append(body)
        elif typ == b"IEND":
            break
    if depth != 8 or interlace:
        raise ValueError(f"{path}: only 8-bit non-interlaced PNG is supported")
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(b"".join(idat))
    stride = w * ch
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                left = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((left + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                left = line[x - ch] if x >= ch else 0
                up_left = prev[x - ch] if x >= ch else 0
                line[x] = (line[x] + _paeth(left, prev[x], up_left)) & 255
        rows.append(line)
        prev = line
    px = []
    for line in rows:
        out = bytearray(w * 3)
        for x in range(w):
            if ctype == 2:
                r, g, b = line[3 * x:3 * x + 3]
                a = 255
            elif ctype == 6:
                r, g, b, a = line[4 * x:4 * x + 4]
            elif ctype == 0:
                r = g = b = line[x]
                a = 255
            elif ctype == 4:
                r = g = b = line[2 * x]
                a = line[2 * x + 1]
            else:
                k = line[x]
                r, g, b = plte[3 * k:3 * k + 3] if plte else (k, k, k)
                a = trns[k] if trns and k < len(trns) else 255
            if a < 255:  # composite on white (renders are opaque screens; alpha is edge noise)
                r, g, b = ((c * a + 255 * (255 - a)) // 255 for c in (r, g, b))
            out[3 * x:3 * x + 3] = bytes((r, g, b))
        px.append(out)
    return w, h, px


def downscale(w, h, px, tw):
    k = max(1, round(w / tw))
    nw, nh = w // k, h // k
    out = []
    for y in range(nh):
        row = bytearray(nw * 3)
        for x in range(nw):
            acc = [0, 0, 0]
            for dy in range(k):
                src = px[y * k + dy]
                base = x * k * 3
                for dx in range(k):
                    o = base + dx * 3
                    acc[0] += src[o]
                    acc[1] += src[o + 1]
                    acc[2] += src[o + 2]
            n = k * k
            row[3 * x:3 * x + 3] = bytes((acc[0] // n, acc[1] // n, acc[2] // n))
        out.append(row)
    return nw, nh, out


def write_png(path, w, h, rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(t, b):
        return struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def _collect(items):
    files = []
    for it in items:
        if os.path.isdir(it):
            files += [os.path.join(it, f) for f in sorted(os.listdir(it)) if f.lower().endswith(".png")]
        elif it.lower().endswith(".png"):
            files.append(it)
    return files


def contact_sheet(items, out="contact-sheet.png", cols=0, cell_w=240) -> dict:
    files = [f for f in _collect(items) if os.path.abspath(f) != os.path.abspath(out)]
    if not files:
        raise ValueError("no PNG renders given")
    cells = [downscale(*read_png(f), cell_w) for f in files]
    cols = cols or min(len(cells), 6 if len(cells) > 8 else 4)
    rows_n = -(-len(cells) // cols)
    cw = max(c[0] for c in cells)
    row_h = [max(c[1] for c in cells[r * cols:(r + 1) * cols]) for r in range(rows_n)]
    W = GAP + cols * (cw + GAP)
    H = GAP + sum(rh + GAP for rh in row_h)
    canvas = [bytearray(bytes(GROUND) * W) for _ in range(H)]
    y0 = GAP
    for r in range(rows_n):
        for c in range(cols):
            i = r * cols + c
            if i >= len(cells):
                break
            w, h, px = cells[i]
            x0 = GAP + c * (cw + GAP)
            for y in range(h):
                canvas[y0 + y][3 * x0:3 * (x0 + w)] = px[y]
        y0 += row_h[r] + GAP
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    write_png(out, W, H, canvas)
    return {"tool": "sheet", "out": out, "count": len(files), "cols": cols, "size": [W, H], "order": files}
