"""

OmniBrain - PDF Ingestion Engine

File: settings.py
Purpose:
    Centralized configuration for project paths and settings.

"""

from pathlib import Path


class Settings:
    """Application configuration."""

    
    # Project Root
    

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    
    # Data Directories
    

    DATA_DIR = PROJECT_ROOT / "data"

    INPUT_DIR = DATA_DIR / "input"
    INPUT_PDF_DIR = INPUT_DIR / "pdfs"

    PROCESSED_DIR = DATA_DIR / "processed"

    TEXT_DIR = PROCESSED_DIR / "text"
    IMAGE_DIR = PROCESSED_DIR / "images"
    TABLE_DIR = PROCESSED_DIR / "tables"
    METADATA_DIR = PROCESSED_DIR / "metadata"
    REPORT_DIR = PROCESSED_DIR / "reports"

    TEMP_DIR = DATA_DIR / "temp"

    
    # Logs
    

    LOG_DIR = PROJECT_ROOT / "logs"

    
    # Supported File Types
    

    SUPPORTED_EXTENSIONS = [".pdf"]

    
    # OCR
    

    OCR_THRESHOLD = 30

    OCR_DPI = 2.0

    OCR_LANGUAGES = ["en"]

    OCR_GPU = False

    
    # Image Extraction
    

    IMAGE_FORMAT = "png"

    
    # Utility Methods
    

    @classmethod
    def create_directories(cls) -> None:
        """
        Create all required project directories
        if they do not already exist.
        """

        directories = [
            cls.INPUT_PDF_DIR,
            cls.TEXT_DIR,
            cls.IMAGE_DIR,
            cls.TABLE_DIR,
            cls.METADATA_DIR,
            cls.REPORT_DIR,
            cls.TEMP_DIR,
            cls.LOG_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)