#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF -> Markdown Converter

Instalacja:

# python -m venv .venv

# Linux / macOS
# source .venv/bin/activate

# Windows
# .venv\Scripts\activate

# Aktualizacja pip
# python -m pip install --upgrade pip

# Instalacja biblioteki
# pip install pymupdf

Uruchomienie:

# python pdf_to_md.py input.pdf output.md

Przykład:

# python pdf_to_md.py python-for-devops.pdf python-for-devops.md
"""

from pathlib import Path
import sys
import fitz  # PyMuPDF


def convert_pdf_to_markdown(pdf_path: str, md_path: str) -> None:
    """
    Konwertuje PDF do Markdown.

    Parametry:
        pdf_path - ścieżka do pliku PDF
        md_path  - ścieżka do pliku wynikowego Markdown
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku: {pdf_file}")

    document = fitz.open(pdf_file)

    markdown = []

    markdown.append(f"# {pdf_file.stem}\n")

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        markdown.append(f"\n---\n")
        markdown.append(f"## Strona {page_number}\n")

        if text:
            markdown.append(text)
        else:
            markdown.append("*Brak tekstu na stronie.*")

    Path(md_path).write_text(
        "\n\n".join(markdown),
        encoding="utf-8",
    )

    document.close()


def main():

    if len(sys.argv) != 3:
        print("Użycie:")
        print("python pdf_to_md.py input.pdf output.md")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_md = sys.argv[2]

    try:
        convert_pdf_to_markdown(input_pdf, output_md)
        print(f"\n✓ Gotowe!")
        print(f"PDF : {input_pdf}")
        print(f"MD  : {output_md}")

    except Exception as error:
        print(f"\nBłąd: {error}")


if __name__ == "__main__":
    main()
