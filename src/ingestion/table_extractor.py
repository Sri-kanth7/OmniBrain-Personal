"""
Module: Table Extractor

Purpose:
    Extract tabular data from PDF documents and save
    each detected table as a CSV file.

"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import pdfplumber

from configs.settings import Settings


class TableExtractor:
    """
    Extract tables from PDF documents.
    """

    def __init__(self, pdf_path: Path) -> None:
        self.pdf_path = Path(pdf_path)

    def extract(self) -> dict[str, Any]:
        """
        Extract tables from the PDF.

        Returns
        -------
        dict
            Information about extracted tables.
        """

        output_directory = (
            Settings.TABLE_DIR /
            self.pdf_path.stem
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        extracted_tables = []

        total_tables = 0

        with pdfplumber.open(self.pdf_path) as pdf:

            for page_number, page in enumerate(
                pdf.pages,
                start=1,
            ):

                tables = page.extract_tables()

                if not tables:
                    continue

                for table_index, table in enumerate(
                    tables,
                    start=1,
                ):

                    if not table:
                        continue

                    dataframe = pd.DataFrame(table)

                    if dataframe.empty:
                        continue

                    csv_name = (
                        f"page_{page_number:03d}"
                        f"_table_{table_index:03d}.csv"
                    )

                    csv_path = (
                        output_directory /
                        csv_name
                    )

                    dataframe.to_csv(
                        csv_path,
                        index=False,
                        header=False,
                    )

                    extracted_tables.append(
                        {
                            "page": page_number,
                            "table": table_index,
                            "rows": dataframe.shape[0],
                            "columns": dataframe.shape[1],
                            "path": str(csv_path),
                        }
                    )

                    total_tables += 1

        return {
            "count": total_tables,
            "tables": extracted_tables,
        }