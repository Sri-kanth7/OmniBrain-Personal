"""

OmniBrain - PDF Ingestion Engine

Module: Text Extractor

Purpose:
    Extract searchable text from PDF documents using
    PyMuPDF with automatic OCR fallback.

"""

from __future__ import annotations

from pathlib import Path

import fitz

from configs.settings import Settings
from src.ingestion.ocr import OCRExtractor


class TextExtractor:
    """
    Extract searchable text from a PDF.

    Workflow:
        1. Try native PyMuPDF extraction.
        2. If little/no text is found, use OCR.
        3. Save unified text output.
    """

    def __init__(
        self,
        pdf_path: Path,
        document: fitz.Document,
    ) -> None:

        self.pdf_path = Path(pdf_path)
        self.document = document

        # Lazy-loaded OCR service
        self.ocr = None

    
    # Extraction
    

    def extract(self) -> dict:

        pages = []

        total_characters = 0

        empty_pages = []

        ocr_pages = 0

        for page_number in range(self.document.page_count):

            page = self.document.load_page(page_number)

            
            # Native text extraction
            

            text = page.get_text("text").strip()

            print(
                f"[DEBUG] Page {page_number + 1}: "
                f"Native Characters = {len(text)}"
            )

            
            # OCR Fallback
            

            if len(text) < Settings.OCR_THRESHOLD:

                print(
                    f"[INFO] OCR triggered on page {page_number + 1}"
                )

                if self.ocr is None:

                    print(
                        "[INFO] Initializing OCR Engine..."
                    )

                    self.ocr = OCRExtractor()

                try:

                    ocr_text = self.ocr.extract_page(page)

                    if ocr_text.strip():

                        text = ocr_text

                        ocr_pages += 1

                except Exception as error:

                    print(
                        f"[WARNING] OCR failed on page "
                        f"{page_number + 1}: {error}"
                    )

            
            # Empty page
            

            if not text.strip():

                empty_pages.append(page_number + 1)

            total_characters += len(text)

            pages.append(
                {
                    "page": page_number + 1,
                    "text": text,
                }
            )

            print(
                f"[DEBUG] Saved page {page_number + 1}"
            )

        print(
            f"[DEBUG] Total Pages Saved = {len(pages)}"
        )

        return {

            "pages": pages,

            "page_count": len(pages),

            "empty_pages": empty_pages,

            "ocr_pages": ocr_pages,

            "total_characters": total_characters,

        }

    
    # Save
    

    def save(
        self,
        extraction_result: dict,
    ) -> Path:

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