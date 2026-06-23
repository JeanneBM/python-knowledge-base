#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zaawansowany konwerter PDF -> Markdown

Instalacja:

# python -m venv .venv

# Linux / macOS
# source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

# Aktualizacja pip
# python -m pip install --upgrade pip

# Instalacja zależności
# pip install pymupdf pillow

Uruchomienie:

# python advanced_pdf_to_md.py input.pdf output_folder

Przykład:

# python advanced_pdf_to_md.py python-for-devops.pdf Python-for-DevOps-md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import median

import fitz  # PyMuPDF


@dataclass
class TextLine:
    text: str
    size: float
    font: str
    page: int
    y: float


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text[:80] or "section"


def clean_text(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")
    text = text.replace("\u2018", "'")
    text = text.replace("\u2019", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("\u201d", '"')
    text = text.replace("\ufeff", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def looks_like_code(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False

    patterns = [
        r"^>>>", r"^\.\.\.", r"^\$ ", r"^#\s",
        r"^from\s+\w+", r"^import\s+\w+", r"^def\s+\w+\(",
        r"^class\s+\w+", r"^if\s+.+:", r"^for\s+.+:",
        r"^while\s+.+:", r"^try:", r"^except\s+", r"^return\s+",
        r"^\w+\s*=\s*.+", r"^pip\s+install", r"^python\s+",
        r"^docker\s+", r"^kubectl\s+", r"^terraform\s+",
        r"^aws\s+", r"^gcloud\s+", r"^az\s+",
    ]
    return any(re.search(pattern, stripped) for pattern in patterns)


def code_language(lines: list[str]) -> str:
    joined = "\n".join(lines)
    if re.search(r"^\$ ", joined, flags=re.MULTILINE):
        return "bash"
    if any(cmd in joined for cmd in ["pip install", "docker ", "kubectl ", "terraform ", "aws ", "gcloud ", "az "]):
        return "bash"
    if any(token in joined for token in ["def ", "class ", "import ", ">>>", "print(", "return "]):
        return "python"
    return ""


def extract_lines(page: fitz.Page, page_number: int) -> list[TextLine]:
    raw = page.get_text("dict")
    lines: list[TextLine] = []

    for block in raw.get("blocks", []):
        if block.get("type") != 0:
            continue

        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue

            text = clean_text("".join(span.get("text", "") for span in spans))
            if not text:
                continue

            sizes = [span.get("size", 0) for span in spans if span.get("size", 0)]
            fonts = [span.get("font", "") for span in spans if span.get("font")]
            y = line.get("bbox", [0, 0, 0, 0])[1]

            lines.append(
                TextLine(
                    text=text,
                    size=max(sizes) if sizes else 0,
                    font=fonts[0] if fonts else "",
                    page=page_number,
                    y=y,
                )
            )

    return lines


def extract_images(doc: fitz.Document, page: fitz.Page, page_number: int, images_dir: Path) -> list[str]:
    image_links: list[str] = []
    images = page.get_images(full=True)

    for index, image_info in enumerate(images, start=1):
        xref = image_info[0]

        try:
            extracted = doc.extract_image(xref)
            image_bytes = extracted["image"]
            ext = extracted.get("ext", "png")
        except Exception:
            continue

        image_name = f"page-{page_number:04d}-img-{index:02d}.{ext}"
        image_path = images_dir / image_name
        image_path.write_bytes(image_bytes)

        image_links.append(f"![Image from page {page_number}](../images/{image_name})")

    return image_links


def detect_heading(line: TextLine, body_size: float) -> str | None:
    text = line.text

    if len(text) > 120 or looks_like_code(text):
        return None

    if re.match(r"^(chapter|appendix)\s+\d+", text, flags=re.I):
        return f"# {text}"

    if re.match(r"^\d+\.\s+.+", text):
        return f"# {text}"

    if line.size >= body_size * 1.65:
        return f"# {text}"

    if line.size >= body_size * 1.35:
        return f"## {text}"

    if line.size >= body_size * 1.18 and len(text.split()) <= 10:
        return f"### {text}"

    return None


def format_markdown(lines: list[TextLine], image_links: list[str], body_size: float, page_number: int) -> str:
    output: list[str] = [f"<!-- Page {page_number} -->\n"]
    paragraph: list[str] = []
    code_block: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(paragraph)
            text = re.sub(r"\s+", " ", text).strip()
            output.append(text + "\n")
            paragraph = []

    def flush_code() -> None:
        nonlocal code_block, in_code
        if code_block:
            lang = code_language(code_block)
            output.append(f"```{lang}")
            output.extend(code_block)
            output.append("```\n")
            code_block = []
        in_code = False

    for line in lines:
        text = line.text
        heading = detect_heading(line, body_size)

        if heading:
            flush_paragraph()
            flush_code()
            output.append(heading + "\n")
            continue

        if looks_like_code(text) or "Mono" in line.font or "Code" in line.font:
            flush_paragraph()
            in_code = True
            code_block.append(text)
            continue

        if in_code:
            flush_code()

        bullet_match = re.match(r"^[-•*]\s+(.+)", text)
        numbered_match = re.match(r"^\d+[.)]\s+(.+)", text)

        if bullet_match:
            flush_paragraph()
            output.append(f"- {bullet_match.group(1)}")
            continue

        if numbered_match:
            flush_paragraph()
            output.append(text)
            continue

        if len(text) < 45 and text.endswith(":"):
            flush_paragraph()
            output.append(f"**{text}**\n")
            continue

        paragraph.append(text)

    flush_paragraph()
    flush_code()

    if image_links:
        output.append("\n## Images extracted from this page\n")
        output.extend(image_links)

    return "\n".join(output).strip() + "\n"


def build_toc(markdown: str) -> str:
    toc: list[str] = ["# Spis treści\n"]

    for line in markdown.splitlines():
        match = re.match(r"^(#{1,3})\s+(.+)", line)
        if not match:
            continue

        level = len(match.group(1))
        title = match.group(2).strip()
        anchor = slugify(title)
        indent = "  " * (level - 1)
        toc.append(f"{indent}- [{title}](#{anchor})")

    return "\n".join(toc) + "\n"


def convert_pdf(pdf_path: Path, output_dir: Path) -> None:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku PDF: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = output_dir / "pages"
    images_dir = output_dir / "images"
    pages_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)

    all_lines: list[TextLine] = []
    page_lines: dict[int, list[TextLine]] = {}

    print("Analizuję rozmiary fontów...")

    for page_index, page in enumerate(doc, start=1):
        lines = extract_lines(page, page_index)
        page_lines[page_index] = lines
        all_lines.extend(lines)

    sizes = [line.size for line in all_lines if line.size > 0]
    body_size = median(sizes) if sizes else 10

    print(f"Rozmiar tekstu bazowego: {body_size:.2f}")
    print("Konwertuję strony...")

    full_parts: list[str] = [
        f"# {pdf_path.stem}\n",
        f"> Wygenerowano automatycznie z pliku PDF: `{pdf_path.name}`.\n",
    ]

    for page_index, page in enumerate(doc, start=1):
        images = extract_images(doc, page, page_index, images_dir)
        md = format_markdown(page_lines[page_index], images, body_size, page_index)

        page_file = pages_dir / f"page-{page_index:04d}.md"
        page_file.write_text(md, encoding="utf-8")

        full_parts.append(md)

        if page_index % 25 == 0:
            print(f"Przetworzono {page_index}/{len(doc)} stron...")

    full_book = "\n\n".join(full_parts)

    full_book_path = output_dir / "full-book.md"
    full_book_path.write_text(full_book, encoding="utf-8")

    summary_path = output_dir / "SUMMARY.md"
    summary_path.write_text(build_toc(full_book), encoding="utf-8")

    readme = f"""# {pdf_path.stem}

Ten katalog zawiera konwersję PDF do Markdown.

## Pliki

- [full-book.md](full-book.md) - cała książka w jednym pliku Markdown
- [SUMMARY.md](SUMMARY.md) - automatycznie wygenerowany spis treści
- [pages/](pages/) - osobne pliki Markdown dla każdej strony
- [images/](images/) - obrazy wyciągnięte z PDF

## Uwaga

Konwersja PDF do Markdown nigdy nie jest idealna, bo PDF przechowuje układ wizualny,
a nie strukturę dokumentu. Ten program stosuje heurystyki dla nagłówków, kodu,
list i obrazów.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    doc.close()

    print("\nGotowe!")
    print(f"Katalog wynikowy: {output_dir}")
    print(f"Pełny Markdown: {full_book_path}")
    print(f"Spis treści: {summary_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Zaawansowany konwerter PDF do Markdown.")
    parser.add_argument("pdf", type=Path, help="Ścieżka do pliku PDF.")
    parser.add_argument("output_dir", type=Path, help="Katalog wynikowy.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        convert_pdf(args.pdf, args.output_dir)
        return 0
    except Exception as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
