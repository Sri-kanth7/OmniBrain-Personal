"""

OmniBrain - PDF Ingestion Engine

Module: Text Extractor

Purpose:
    Extract textual content from PDF documents using
    PyMuPDF.

Responsibilities:
    - Page-wise extraction
    - Empty page detection
    - Text statistics
    - Save extracted text

"""

from __future__ import annotations

from pathlib import Path

import fitz

from configs.settings import Settings


class TextExtractor:
    """
    Extracts searchable text from a PDF document.
    """

    def __init__(self, pdf_path: Path, document: fitz.Document) -> None:
        self.pdf_path = Path(pdf_path)
        self.document = document

    
    # Extraction
    

    def extract(self) -> dict:
        """
        Extract text page by page.

        Returns
        -------
        dict
            Extraction result.
        """

        pages = []

        total_characters = 0

        empty_pages = []

        for page_number, page in enumerate(self.document, start=1):

            text = page.get_text("text").strip()

            if not text:
                empty_pages.append(page_number)

            total_characters += len(text)

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

        return {
            "pages": pages,
            "page_count": len(pages),
            "empty_pages": empty_pages,
            "total_characters": total_characters,
        }

    
    # Save
    

    def save(self, extraction_result: dict) -> Path:
        """
        Save extracted text.

        Returns
        -------
        Path
        """

        output_file = (
            Settings.TEXT_DIR
            / f"{self.pdf_path.stem}.txt"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:

            for page in extraction_result["pages"]:

                file.write("=" * 80 + "\n")
                file.write(
                    f"PAGE {page['page']}\n"
                )
                file.write("=" * 80 + "\n\n")

                file.write(page["text"])

                file.write("\n\n")

        return output_file