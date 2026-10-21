"""KDL parser: a strict, dependency-free YAML subset (see docs/KDL.md).

Supported: block mappings and lists by indentation, inline lists/maps,
literal blocks (`|`), comments, quoted/bare scalars, bare hex colors.
Every parsed node keeps its source line so findings can point at it.
"""
from __future__ import annotations

import re

__all__ = ["KDLError", "parse", "parse_file", "line_of", "get_path"]


class KDLError(ValueError):
    def __init__(self, line: int, message: str):
        super().__init__(f"line {line}: {message}")
        self.line = line
        self.message = message


class Map(dict):
    """dict that remembers the source line of each key."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lines: dict = {}
        self.line = 0


class Seq(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.lines: list = []
        self.line = 0


_INT = re.compile(r"^[-+]?\d+$")
_FLOAT = re.compile(r"^[-+]?(\d+\.\d*|\.\d+|\d+)([eE][-+]?\d+)?$")
_HEXSTART = re.compile(r"[0-9A-Fa-f]")


def _strip_comment(text: str) -> str:
    """Remove a trailing comment while respecting quotes and bare hex colors."""
    out = []
    quote = None
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            out.append(ch)
            if ch == "\\" and quote == '"' and i + 1 < len(text):
                out.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'" and (i == 0 or text[i - 1] in " \t[{,:"):
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or text[i - 1] in " \t"):
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if nxt == "" or nxt in " \t#" or not _HEXSTART.match(nxt):
                break
            out.append(ch)
        else:
            out.append(ch)
        i += 1
    return "".join(out).rstrip()


def _split_top(text: str, sep: str = ",") -> list:
    parts, depth, quote, buf = [], 0, None, []
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail or parts:
        parts.append(tail)
    return [p for p in parts if p != ""]


def _find_colon(text: str) -> int:
    """Index of the key separator `:` (followed by space/end) outside quotes/brackets."""
    quote, depth = None, 0
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in "\"'" and i == 0:
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == ":" and depth == 0 and (i + 1 == len(text) or text[i + 1] in " \t"):
            return i
    return -1


def _unquote(s: str, line: int) -> str:
    q = s[0]
    if len(s) < 2 or s[-1] != q:
        raise KDLError(line, f"unterminated string {s!r}")
    body = s[1:-1]
    if q == '"':
        body = body.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
    else:
        body = body.replace("''", "'")
    return body


def _scalar(raw: str, line: int):
    s = raw.strip()
    if s == "":
        return None
    if s[0] in "\"'":
        return _unquote(s, line)
    if s[0] == "[":
        if not s.endswith("]"):
            raise KDLError(line, f"unterminated inline list {s!r}")
        seq = Seq(_scalar(p, line) for p in _split_top(s[1:-1]))
        seq.line = line
        seq.lines = [line] * len(seq)
        return seq
    if s[0] == "{":
        if not s.endswith("}"):
            raise KDLError(line, f"unterminated inline map {s!r}")
        m = Map()
        m.line = line
        for part in _split_top(s[1:-1]):
            c = _find_colon(part)
            if c < 0:
                raise KDLError(line, f"inline map entry without ':' {part!r}")
            k = _key(part[:c], line)
            m[k] = _scalar(part[c + 1:], line)
            m.lines[k] = line
        return m
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~"):
        return None
    if _INT.match(s):
        return int(s)
    if _FLOAT.match(s):
        return float(s)
    return s


def _key(raw: str, line: int) -> str:
    k = raw.strip()
    if not k:
        raise KDLError(line, "empty key")
    if k[0] in "\"'":
        return _unquote(k, line)
    return k


def _depth(text: str) -> int:
    depth, quote = 0, None
    for ch in text:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
    return depth


def _tokenize(text: str):
    """Return (line_no, indent, content, raw_line) rows.

    Inline lists/maps may span several lines; continuation lines are joined
    onto the line that opened the bracket."""
    rows = []
    lines = text.splitlines()
    no = 0
    while no < len(lines):
        raw = lines[no]
        no += 1
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise KDLError(no, "tabs are not allowed for indentation; use 2 spaces")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            rows.append((no, None, "", raw))
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        content = _strip_comment(stripped)
        start = no
        while _depth(content) > 0 and no < len(lines):
            nxt = _strip_comment(lines[no].strip())
            no += 1
            content = f"{content} {nxt}" if nxt else content
            rows.append((no, None, "", ""))
        if _depth(content) > 0:
            raise KDLError(start, "unclosed bracket")
        rows.insert(len(rows) - (no - start), (start, indent, content, raw))
    return rows


class _Parser:
    def __init__(self, text: str):
        self.rows = _tokenize(text)
        self.i = 0

    def _skip_blank(self):
        while self.i < len(self.rows) and self.rows[self.i][1] is None:
            self.i += 1

    def _peek(self):
        self._skip_blank()
        return self.rows[self.i] if self.i < len(self.rows) else None

    def parse(self):
        row = self._peek()
        if row is None:
            m = Map()
            return m
        value = self._block(row[1])
        row = self._peek()
        if row is not None:
            raise KDLError(row[0], "unexpected content (check indentation)")
        return value

    def _block(self, indent: int):
        row = self._peek()
        if row[2].startswith("- ") or row[2] == "-":
            return self._seq(indent)
        return self._map(indent)

    def _literal(self, parent_indent: int) -> str:
        lines = []
        block_indent = None
        while self.i < len(self.rows):
            no, ind, _content, raw = self.rows[self.i]
            if ind is None:
                lines.append("")
                self.i += 1
                continue
            if ind <= parent_indent:
                break
            if block_indent is None:
                block_indent = ind
            lines.append(raw[block_indent:])
            self.i += 1
        while lines and lines[-1] == "":
            lines.pop()
        return "\n".join(lines)

    def _value_after_key(self, rest: str, indent: int, line: int):
        rest = rest.strip()
        if rest in ("|", ">", "|-", ">-"):
            text = self._literal(indent)
            return " ".join(text.split("\n")) if rest.startswith(">") else text
        if rest != "":
            return _scalar(rest, line)
        nxt = self._peek()
        if nxt is None:
            return None
        if nxt[1] > indent:
            return self._block(nxt[1])
        if nxt[1] == indent and (nxt[2].startswith("- ") or nxt[2] == "-"):
            return self._seq(indent)
        return None

    def _map(self, indent: int) -> Map:
        m = Map()
        first = True
        while True:
            row = self._peek()
            if row is None or row[1] < indent:
                break
            no, ind, content, _ = row
            if ind > indent:
                raise KDLError(no, "unexpected indentation")
            if content.startswith("- ") or content == "-":
                break
            c = _find_colon(content)
            if c < 0:
                raise KDLError(no, f"expected 'key: value', got {content!r}")
            key = _key(content[:c], no)
            if key in m:
                raise KDLError(no, f"duplicate key {key!r}")
            if first:
                m.line = no
                first = False
            self.i += 1
            m.lines[key] = no
            m[key] = self._value_after_key(content[c + 1:], indent, no)
        return m

    def _seq(self, indent: int) -> Seq:
        s = Seq()
        while True:
            row = self._peek()
            if row is None or row[1] != indent:
                if row is not None and row[1] > indent:
                    raise KDLError(row[0], "unexpected indentation in list")
                break
            no, ind, content, _ = row
            if not (content.startswith("- ") or content == "-"):
                break
            if not s:
                s.line = no
            self.i += 1
            body = content[1:].strip()
            s.lines.append(no)
            if body == "":
                nxt = self._peek()
                s.append(self._block(nxt[1]) if nxt and nxt[1] > indent else None)
                continue
            c = _find_colon(body)
            if c >= 0 and body[0] not in "[{\"'":
                # list item that is a map; its first key sits after "- "
                item_indent = indent + 2
                key = _key(body[:c], no)
                m = Map()
                m.line = no
                m.lines[key] = no
                m[key] = self._value_after_key(body[c + 1:], item_indent, no)
                rest = self._peek()
                if rest is not None and rest[1] == item_indent and not rest[2].startswith("- "):
                    more = self._map(item_indent)
                    for k, v in more.items():
                        if k in m:
                            raise KDLError(more.lines[k], f"duplicate key {k!r}")
                        m[k] = v
                        m.lines[k] = more.lines[k]
                s.append(m)
            else:
                s.append(_scalar(body, no))
        return s


def parse(text: str):
    return _Parser(text).parse()


def parse_file(path: str):
    with open(path, encoding="utf-8") as fh:
        return parse(fh.read())


def get_path(doc, path: str, default=None):
    """Fetch `a.b.0.c` from a parsed document."""
    cur = doc
    for part in path.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return default
        elif isinstance(cur, dict):
            if part not in cur:
                return default
            cur = cur[part]
        else:
            return default
    return cur


def line_of(node, key=None) -> int:
    if key is not None and isinstance(node, Map):
        return node.lines.get(key, node.line)
    if key is not None and isinstance(node, Seq) and isinstance(key, int) and key < len(node.lines):
        return node.lines[key]
    return getattr(node, "line", 0)
