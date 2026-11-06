#!/usr/bin/env python3
"""Extract plain text from Drive-downloaded files (PDF, Office, ebooks, HTML, …)."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

MAX_DEFAULT = 12000

# Suffixes we attempt (lowercase). Unknown → empty + reason in meta.
TEXT_SUFFIXES = {".txt", ".md", ".markdown", ".csv", ".tsv", ".json", ".xml", ".rtf"}
HTML_SUFFIXES = {".html", ".htm", ".xhtml"}
PDF_SUFFIXES = {".pdf"}
OFFICE_SUFFIXES = {".docx", ".pptx", ".xlsx", ".doc", ".ppt", ".xls"}
EBOOK_SUFFIXES = {".epub", ".mobi", ".azw", ".azw3", ".prc", ".fb2", ".djvu", ".cbz", ".cbr"}


class _StripHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return " ".join(self.parts)


def _clip(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "…"


def _read_utf8(path: Path, max_chars: int) -> str:
    return _clip(path.read_text(encoding="utf-8", errors="replace"), max_chars)


def _html_to_text(raw: str, max_chars: int) -> str:
    parser = _StripHTML()
    parser.feed(raw)
    return _clip(parser.text(), max_chars)


def _pdftotext(path: Path, max_chars: int) -> str:
    try:
        r = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(path), "-"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode == 0 and r.stdout.strip():
            return _clip(r.stdout, max_chars)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    try:
        import pypdf  # type: ignore

        reader = pypdf.PdfReader(str(path))
        chunks: list[str] = []
        for page in reader.pages[:40]:
            chunks.append(page.extract_text() or "")
            if sum(len(c) for c in chunks) > max_chars:
                break
        return _clip("\n".join(chunks), max_chars)
    except Exception:
        return ""


def _docx_text(path: Path, max_chars: int) -> str:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        data = zf.read("word/document.xml")
    root = ET.fromstring(data)
    bits = [el.text for el in root.iter(f"{{{ns['w']}}}t") if el.text]
    return _clip("".join(bits), max_chars)


def _pptx_text(path: Path, max_chars: int) -> str:
    bits: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for name in sorted(zf.namelist()):
            if not name.startswith("ppt/slides/slide") or not name.endswith(".xml"):
                continue
            root = ET.fromstring(zf.read(name))
            for el in root.iter():
                if el.tag.endswith("}t") and el.text:
                    bits.append(el.text)
    return _clip(" ".join(bits), max_chars)


def _xlsx_text(path: Path, max_chars: int) -> str:
    bits: list[str] = []
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for el in root.iter():
                if el.tag.endswith("}t") and el.text:
                    shared.append(el.text)
        bits.extend(shared[:500])
        for name in zf.namelist():
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
                root = ET.fromstring(zf.read(name))
                for el in root.iter():
                    if el.tag.endswith("}v") and el.text:
                        bits.append(el.text)
    return _clip(" ".join(bits), max_chars)


def _epub_text(path: Path, max_chars: int) -> str:
    bits: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            low = name.lower()
            if not (low.endswith(".html") or low.endswith(".xhtml") or low.endswith(".htm")):
                continue
            try:
                raw = zf.read(name).decode("utf-8", errors="replace")
            except OSError:
                continue
            bits.append(_html_to_text(raw, max_chars))
            if sum(len(b) for b in bits) > max_chars:
                break
    return _clip(" ".join(bits), max_chars)


def _fb2_text(path: Path, max_chars: int) -> str:
    root = ET.parse(path).getroot()
    bits: list[str] = []
    for el in root.iter():
        if el.text and el.text.strip():
            bits.append(el.text.strip())
    return _clip(" ".join(bits), max_chars)


def _calibre_ebook_convert_candidates() -> list[str]:
    import shutil

    out: list[str] = []
    for name in ("ebook-convert",):
        found = shutil.which(name)
        if found:
            out.append(found)
    home_local = Path.home() / ".local/bin/ebook-convert"
    for fixed in (
        home_local,
        Path("/opt/homebrew/bin/ebook-convert"),
        Path("/usr/local/bin/ebook-convert"),
        Path("/Applications/calibre.app/Contents/MacOS/ebook-convert"),
    ):
        if fixed.is_file() and os.access(fixed, os.X_OK):
            s = str(fixed)
            if s not in out:
                out.append(s)
    return out


def _calibre_convert_to_txt(path: Path, max_chars: int) -> str:
    for cmd in _calibre_ebook_convert_candidates():
        try:
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                out = Path(tmp.name)
            subprocess.run([cmd, str(path), str(out)], capture_output=True, timeout=300, check=True)
            if out.is_file():
                text = _read_utf8(out, max_chars)
                out.unlink(missing_ok=True)
                return text
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
    return ""


def extract_text_from_path(path: Path, *, max_chars: int = MAX_DEFAULT) -> tuple[str, str]:
    """Return (text, method_or_error). Empty text → second value explains skip."""
    if not path.is_file():
        return "", "not a file"
    suffix = path.suffix.lower()
    name = path.name.lower()

    if suffix in TEXT_SUFFIXES or suffix == "":
        try:
            return _read_utf8(path, max_chars), "utf8"
        except OSError as exc:
            return "", str(exc)

    if suffix in HTML_SUFFIXES:
        try:
            return _html_to_text(path.read_text(encoding="utf-8", errors="replace"), max_chars), "html"
        except OSError as exc:
            return "", str(exc)

    if suffix in PDF_SUFFIXES:
        t = _pdftotext(path, max_chars)
        return (t, "pdftotext") if t else ("", "pdf empty or unreadable (scan/OCR needed)")

    if suffix == ".docx":
        try:
            t = _docx_text(path, max_chars)
            return (t, "docx") if t else ("", "docx empty")
        except Exception as exc:
            return "", f"docx: {exc}"

    if suffix == ".pptx":
        try:
            t = _pptx_text(path, max_chars)
            return (t, "pptx") if t else ("", "pptx empty")
        except Exception as exc:
            return "", f"pptx: {exc}"

    if suffix == ".xlsx":
        try:
            t = _xlsx_text(path, max_chars)
            return (t, "xlsx") if t else ("", "xlsx empty")
        except Exception as exc:
            return "", f"xlsx: {exc}"

    if suffix == ".epub":
        try:
            t = _epub_text(path, max_chars)
            return (t, "epub") if t else ("", "epub empty")
        except Exception as exc:
            return "", f"epub: {exc}"

    if suffix == ".fb2":
        try:
            t = _fb2_text(path, max_chars)
            return (t, "fb2") if t else ("", "fb2 empty")
        except Exception as exc:
            return "", f"fb2: {exc}"

    if suffix in {".mobi", ".azw", ".azw3", ".prc", ".azw4"} or name.endswith(".mobi"):
        t = _calibre_convert_to_txt(path, max_chars)
        return (t, "calibre") if t else ("", "mobi/azw needs calibre ebook-convert in PATH")

    if suffix in {".doc", ".ppt", ".xls"}:
        return "", "legacy Office: upload as Google Doc or export docx/xlsx on Drive"

    if suffix in {".djvu", ".cbz", ".cbr"}:
        return "", f"{suffix}: not supported yet (convert to pdf/epub on Drive)"

    return "", f"unsupported suffix {suffix or '(none)'}"


def collect_text_from_tree(root: Path, *, max_chars: int = MAX_DEFAULT) -> str:
    """After gdocs drive download, extract text from all files under root."""
    if not root.is_dir():
        return ""
    parts: list[str] = []
    budget = max_chars
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        text, _ = extract_text_from_path(path, max_chars=budget)
        if text:
            parts.append(text)
            budget = max_chars - len("\n\n".join(parts))
            if budget <= 200:
                break
    return _clip("\n\n".join(parts), max_chars)


def main() -> int:
    p = argparse.ArgumentParser(description="Extract text from a Drive corpus file or download directory")
    p.add_argument("path", type=Path, nargs="?", help="File or directory (gdocs download output dir)")
    p.add_argument("--max-chars", type=int, default=MAX_DEFAULT)
    p.add_argument("--self-test", action="store_true", help="Run lightweight checks")
    args = p.parse_args()

    if args.self_test:
        t, m = extract_text_from_path(Path(__file__), max_chars=500)
        assert m == "unsupported suffix .py" or t == ""
        print("self-test ok")
        return 0

    if args.path is None:
        p.error("path required unless --self-test")

    path = args.path if args.path.is_absolute() else Path.cwd() / args.path

    if path.is_dir():
        out = collect_text_from_tree(path, max_chars=args.max_chars)
        print(out or "(no extractable text)")
        return 0 if out else 1

    text, method = extract_text_from_path(path, max_chars=args.max_chars)
    if text:
        print(text)
        print(f"# method: {method}", file=sys.stderr)
        return 0
    print(method, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
