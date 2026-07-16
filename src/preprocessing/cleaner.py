"""

OmniBrain

Module: Text Cleaner

Purpose:
    Clean extracted PDF text before chunking.

"""

from __future__ import annotations

import re


class TextCleaner:
    """
    Clean extracted PDF text while preserving meaning.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean extracted text.

        Parameters
        ----------
        text : str
            Raw extracted text.

        Returns
        -------
        str
            Cleaned text.
        """

        if not text:
            return ""

        
        # Normalize line endings
        

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        
        # Remove trailing whitespace
        

        lines = [
            line.rstrip()
            for line in text.split("\n")
        ]

        text = "\n".join(lines)

        
        # Replace tabs with spaces
        

        text = text.replace("\t", " ")

        
        # Collapse multiple spaces
        

        text = re.sub(
            r"[ ]{2,}",
            " ",
            text,
        )

        
        # Collapse excessive blank lines
        

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        
        # Remove leading/trailing whitespace
        

        text = text.strip()

        return text