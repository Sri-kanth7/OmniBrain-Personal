"""
OmniBrain - PDF Ingestion Engine

Module: Report Generator

Purpose:
    Generate a structured ingestion report for every PDF.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from configs.settings import Settings


class ReportGenerator:
    """
    Generate a structured PDF ingestion report.
    """

    def __init__(
        self,
        pdf_path: Path,
    ) -> None:

        self.pdf_path = Path(pdf_path)

    def generate(
        self,
        metadata: dict[str, Any],
        text: dict[str, Any],
        chunks: dict[str, Any],
        images: dict[str, Any],
        tables: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate ingestion report.
        """

        report = {

            "document": self.pdf_path.name,

            "generated_at": datetime.now().isoformat(),

            "status": "SUCCESS",

            "metadata": metadata,

            "summary": {

                "pages": metadata["pages"],

                "characters": text["total_characters"],

                "empty_pages": len(
                    text["empty_pages"]
                ),

                "ocr_pages": text["ocr_pages"],

                "chunks": chunks["chunk_count"],

                "images": images["unique_images"],

                "tables": tables["count"],

            },

            "chunk_statistics": chunks["statistics"],

            "processing": {

                "metadata_extracted": True,

                "text_extracted": True,

                "text_cleaned": True,

                "text_chunked": True,

                "chunk_validation": True,

                "ocr_enabled": True,

                "images_extracted": True,

                "tables_extracted": True,

            },

        }

        return report

    def save(
        self,
        report: dict[str, Any],
    ) -> Path:
        """
        Save report as JSON.
        """

        output_path = (
            Settings.REPORT_DIR
            / f"{self.pdf_path.stem}_report.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output_path