"""
OmniBrain

Module: Chunk Validator

Purpose:
    Validate generated chunks before they are
    embedded and stored in the vector database.
"""

from __future__ import annotations

from configs.settings import Settings


class ChunkValidator:
    """
    Validate generated chunks.
    """

    def validate(
        self,
        chunk_data: dict,
    ) -> dict:
        """
        Validate chunk collection.

        Parameters
        ----------
        chunk_data : dict

        Returns
        -------
        dict
        """

        valid_chunks = []

        for chunk in chunk_data["chunks"]:

            text = chunk["text"].strip()

            if not text:
                continue

            if chunk["char_count"] < Settings.MIN_CHUNK_SIZE:
                continue

            valid_chunks.append(chunk)

        statistics = self._statistics(valid_chunks)

        return {
            "document": chunk_data["document"],
            "chunk_count": len(valid_chunks),
            "statistics": statistics,
            "chunks": valid_chunks,
        }

    def _statistics(
        self,
        chunks: list,
    ) -> dict:
        """
        Calculate chunk statistics.
        """

        if not chunks:

            return {
                "largest_chunk": 0,
                "smallest_chunk": 0,
                "average_chunk_size": 0,
                "total_characters": 0,
            }

        sizes = [
            chunk["char_count"]
            for chunk in chunks
        ]

        return {
            "largest_chunk": max(sizes),
            "smallest_chunk": min(sizes),
            "average_chunk_size": round(
                sum(sizes) / len(sizes),
                2,
            ),
            "total_characters": sum(sizes),
        }