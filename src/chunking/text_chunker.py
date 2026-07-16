"""
OmniBrain

Module: Text Chunker

Purpose:
    Split cleaned text into semantic chunks for
    embedding and retrieval.
"""

from __future__ import annotations

import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from configs.settings import Settings


class TextChunker:
    """
    Split cleaned text into overlapping chunks.
    """

    def __init__(self, pdf_path: Path) -> None:

        self.pdf_path = Path(pdf_path)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Settings.CHUNK_SIZE,
            chunk_overlap=Settings.CHUNK_OVERLAP,
            separators=Settings.CHUNK_SEPARATORS,
            length_function=len,
            is_separator_regex=False,
        )

    def chunk(self, text_data: dict) -> dict:
        """
        Generate chunks from extracted text.
        """

        chunks = []

        chunk_id = 1

        for page in text_data["pages"]:

            page_number = page["page"]

            text = page["text"]

            if not text.strip():
                continue

            page_chunks = self.splitter.split_text(text)

            for index, chunk in enumerate(page_chunks, start=1):

                chunk = chunk.strip()

                if not chunk:
                    continue

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "page": page_number,
                        "chunk_index": index,
                        "document": self.pdf_path.name,
                        "text": chunk,
                        "char_count": len(chunk),
                        "word_count": len(chunk.split()),
                    }
                )

                chunk_id += 1

        return {
            "document": self.pdf_path.name,
            "chunk_count": len(chunks),
            "chunks": chunks,
        }

    def save(self, chunk_data: dict) -> Path:
        """
        Save chunks as JSON.
        """

        output_path = (
            Settings.CHUNK_OUTPUT_DIR
            / f"{self.pdf_path.stem}_chunks.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                chunk_data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output_path