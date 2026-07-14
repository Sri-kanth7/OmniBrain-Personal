"""
Module: Ingestion Pipeline

Purpose:
    Orchestrates the complete PDF ingestion workflow.

"""

from pathlib import Path

from configs.settings import Settings

from src.ingestion.pdf_reader import PDFReader
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.text_extractor import TextExtractor
from src.ingestion.image_extractor import ImageExtractor
from src.ingestion.table_extractor import TableExtractor
from src.ingestion.report_generator import ReportGenerator


class IngestionPipeline:
    """
    Complete PDF ingestion workflow.
    """

    def __init__(self) -> None:

        Settings.create_directories()

    def run(self) -> None:

        pdf_files = list(
            Settings.INPUT_PDF_DIR.glob("*.pdf")
        )

        if not pdf_files:
            print("No PDF found.")
            return

        if len(pdf_files) > 1:
            print("Multiple PDFs found.")
            print("Keep only one PDF for now.")
            return

        pdf_path = pdf_files[0]

        print("=" * 60)
        print("          OMNIBRAIN PDF INGESTION")
        print("=" * 60)

        reader = PDFReader(pdf_path)

        document = reader.open()

        print(f"\nOpened : {pdf_path.name}")
        print(f"Pages  : {reader.page_count}")

        
        # Metadata
        

        metadata = MetadataExtractor(
            pdf_path,
            document,
        )

        metadata_data = metadata.extract()

        metadata.save(metadata_data)

        print("✓ Metadata Extracted")

        
        # Text
        

        text = TextExtractor(
            pdf_path,
            document,
        )

        text_data = text.extract()

        text.save(text_data)

        print("Text Extracted")

        # ------------------------------------------
        # Images
        # ------------------------------------------

        images = ImageExtractor(
            pdf_path,
            document,
        )

        image_data = images.extract()

        print(
            f"Images Extracted : "
            f"{image_data['unique_images']}"
        )

        # ------------------------------------------
        # Tables
        # ------------------------------------------

        tables = TableExtractor(pdf_path)

        table_data = tables.extract()

        print(
            f"Tables Extracted : "
            f"{table_data['count']}"
        )

        # ------------------------------------------
        # Report
        # ------------------------------------------

        report = ReportGenerator(pdf_path)

        report_data = report.generate(
            metadata=metadata_data,
            text=text_data,
            images=image_data,
            tables=table_data,
        )

        report.save(report_data)

        print("Report Generated")

        reader.close()

        print("\nPipeline Completed Successfully.")