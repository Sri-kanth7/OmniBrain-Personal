"""
Module: Metadata Extractor

Purpose:
    Extracts metadata from a PDF document and stores
    it as a structured JSON file.

Responsibilities:
    - Extract document metadata
    - Format PDF date fields
    - Calculate file size
    - Save metadata to JSON

"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import fitz

from configs.settings import Settings


class MetadataExtractor:
    """
    Extracts metadata from a PDF document.
    """

    def __init__(self, pdf_path: Path, document: fitz.Document) -> None:
        self.pdf_path = Path(pdf_path)
        self.document = document

    
    # Private Methods
    

    @staticmethod
    def _format_pdf_date(date_string: str | None) -> str | None:
        """
        Convert PDF date format into a readable format.

        Example
        -------
        Input:
            D:20240714132000

        Output:
            2024-07-14 13:20:00
        """

        if not date_string:
            return None

        try:
            cleaned = date_string.replace("D:", "")[:14]

            return datetime.strptime(
                cleaned,
                "%Y%m%d%H%M%S"
            ).strftime("%Y-%m-%d %H:%M:%S")

        except Exception:
            return date_string

    
    # Metadata Extraction
    

    def extract(self) -> dict[str, Any]:
        """
        Extract metadata from the PDF.

        Returns
        -------
        dict
            Metadata dictionary.
        """

        raw = self.document.metadata

        metadata = {
            "filename": self.pdf_path.name,
            "file_path": str(self.pdf_path.resolve()),
            "file_size_mb": round(
                self.pdf_path.stat().st_size / (1024 * 1024),
                2,
            ),
            "pages": self.document.page_count,
            "title": raw.get("title"),
            "author": raw.get("author"),
            "subject": raw.get("subject"),
            "keywords": raw.get("keywords"),
            "creator": raw.get("creator"),
            "producer": raw.get("producer"),
            "creation_date": self._format_pdf_date(
                raw.get("creationDate")
            ),
            "modification_date": self._format_pdf_date(
                raw.get("modDate")
            ),
            "encrypted": self.document.needs_pass,
            "pdf_version": self.document.metadata.get("format", "Unknown"),
        }

        return metadata

    
    # Save Metadata
    

    def save(self, metadata: dict[str, Any]) -> Path:
        """
        Save metadata as JSON.

        Parameters
        ----------
        metadata : dict

        Returns
        -------
        Path
            Saved JSON path.
        """

        output_path = (
            Settings.METADATA_DIR
            / f"{self.pdf_path.stem}.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as json_file:

            json.dump(
                metadata,
                json_file,
                indent=4,
                ensure_ascii=False,
            )

        return output_path