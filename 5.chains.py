from __future__ import annotations
from typing import Self, Any
from io import BufferedReader

import requests


class Options:
    """Builder class for configuring text extraction options."""
    _options: dict

    def __init__(self):
        """Initialize the options builder with default values."""
        self._options = {}

    def as_plain_text(self) -> Self:
        """Set whether to return the text as plain text."""
        self._options["as_plain_text"] = True
        return self

    def with_ocr(self, inline: bool = True, with_bounding_boxes: bool = False, detect_tables: bool = False) -> Self:
        """Enable Optical Character Recognition (OCR) for text extraction.

        Keyword arguments:
        inline -- If True, use inline OCR. Defaults to True.
        with_bounding_boxes -- If True, return text with bounding boxes. Defaults to False.
        detect_tables -- If True, detect tables in the file. Defaults to False.
        """
        self._options["with_ocr"] = True
        if inline:
            self._options["inline_ocr"] = True
        if with_bounding_boxes:
            self._options["with_bounding_boxes"] = True
        if detect_tables:
            self._options["detect_tables"] = True
        return self

    def timeout(self, seconds: int) -> Self:
        """Set a timeout for text extraction in seconds."""
        # Validation
        if not isinstance(seconds, int):
            raise TypeError("Timeout must be an integer")
        if seconds <= 0:
            raise ValueError("Timeout must be positive")

        # Setting
        self._options["timeout"] = seconds
        return self

    def rotate(self, degrees: int) -> Self:
        """Set the rotation angle for the image.
        Must be one of 0, 90, 180, or 270 degrees.
        """
        if degrees not in (0, 90, 180, 270):
            raise ValueError("Rotation must be one of 0, 90, 180, 270")

        if degrees != 0:  # Only include non-default rotation
            self._options["rotate_angle"] = degrees
        return self

    def build(self) -> dict:
        """Return the built options dictionary."""
        return self._options


def get_text(file: BufferedReader, options: Options) -> str:
    """Extract text from a file using the provided options."""
    headers = options.build()
    response = requests.post("dummy_url", data=file, headers=headers)
    return response.text


def example_usage():
    with open('example.pdf', 'rb') as f:
        options = (
            Options()
            .with_ocr(
                with_bounding_boxes=True,
                inline=True,
                detect_tables=False,
            )
            .timeout(30)
            .rotate(90)
            .as_plain_text()
        )

        # One-liner with explicit annotation for better IDE support
        text = get_text(
            f,
            options  # parentheses help IDE track type
        )
        print(text)
