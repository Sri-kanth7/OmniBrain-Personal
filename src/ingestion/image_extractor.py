"""

OmniBrain - PDF Ingestion Engine

Module: Image Extractor
 
Purpose:
    Extract embedded images from PDF documents.

Responsibilities:
    - Extract original embedded images
    - Skip duplicate images
    - Save images to disk
    - Collect image metadata

"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import fitz

from configs.settings import Settings


class ImageExtractor:
    """
    Extract embedded images from a PDF document.
    """

    def __init__(self, pdf_path: Path, document: fitz.Document) -> None:
        """
        Initialize the Image Extractor.

        Parameters
        ----------
        pdf_path : Path
            Path to the PDF document.

        document : fitz.Document
            Opened PyMuPDF document.
        """

        self.pdf_path = Path(pdf_path)
        self.document = document

    
    # Image Extraction
    

    def extract(self) -> dict[str, Any]:
        """
        Extract embedded images from the PDF.

        Returns
        -------
        dict
            Dictionary containing extracted image metadata.
        """

        output_directory = (
            Settings.IMAGE_DIR /
            self.pdf_path.stem
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        extracted_images = []

        total_images = 0

        # Track already extracted images
        processed_xrefs = set()

        for page_number, page in enumerate(
            self.document,
            start=1,
        ):

            images = page.get_images(full=True)

            for image_index, image in enumerate(
                images,
                start=1,
            ):

                xref = image[0]

                # Skip duplicate embedded images
                if xref in processed_xrefs:
                    continue

                processed_xrefs.add(xref)

                base_image = self.document.extract_image(
                    xref
                )

                image_bytes = base_image["image"]

                extension = base_image["ext"]

                width = base_image["width"]

                height = base_image["height"]

                colorspace = base_image.get(
                    "colorspace",
                    "Unknown",
                )

                image_name = (
                    f"page_{page_number:03d}"
                    f"_img_{image_index:03d}"
                    f".{extension}"
                )

                image_path = (
                    output_directory /
                    image_name
                )

                with open(
                    image_path,
                    "wb",
                ) as image_file:

                    image_file.write(
                        image_bytes
                    )

                extracted_images.append(
                    {
                        "page": page_number,
                        "image": image_index,
                        "xref": xref,
                        "width": width,
                        "height": height,
                        "colorspace": colorspace,
                        "extension": extension,
                        "size_kb": round(
                            len(image_bytes) / 1024,
                            2,
                        ),
                        "path": str(image_path),
                    }
                )

                total_images += 1

        return {
            "count": total_images,
            "unique_images": len(processed_xrefs),
            "images": extracted_images,
        }