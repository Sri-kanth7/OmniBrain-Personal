"""

OmniBrain - PDF Ingestion Engine

Module: OCR Extractor

Purpose:
    OCR service used as a fallback for scanned PDF pages.

"""

from PIL import Image
import easyocr
import fitz

from configs.settings import Settings


class OCRExtractor:
    """
    OCR service for scanned PDF pages.

    This class is intentionally designed to process
    ONE page at a time.

    The TextExtractor decides when OCR is required.
    """

    def __init__(
        self,
        languages: list[str] | None = None,
        gpu: bool = False,
    ):

        self.reader = easyocr.Reader(
            languages or Settings.OCR_LANGUAGES,
            gpu=Settings.OCR_GPU,
        )

    def _page_to_image(
        self,
        page: fitz.Page,
    ) -> Image.Image:
        """
        Convert PDF page into a high-resolution image.
        """

        matrix = fitz.Matrix(
            Settings.OCR_DPI,
            Settings.OCR_DPI,
        )

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image = Image.frombytes(
            "RGB",
            (
                pixmap.width,
                pixmap.height,
            ),
            pixmap.samples,
        )

        return image

    def extract_page(
        self,
        page: fitz.Page,
    ) -> str:
        """
        Perform OCR on a single page.
        """

        image = self._page_to_image(page)

        result = self.reader.readtext(
            image,
            detail=0,
            paragraph=True,
        )

        text = "\n".join(result)

        return text.strip()