from io import BufferedReader
from typing import Callable

import requests

Option = Callable[[dict], dict]


class Options:
    @staticmethod
    def AsPlainText() -> Option:
        """Output text as plain text format."""

        def apply(opt: dict) -> dict:
            opt["as_plain_text"] = True
            return opt

        return apply

    @staticmethod
    def WithTimeout(seconds: int) -> Option:
        """Set a timeout for text extraction in seconds.
        Timeout must be a positive integer."""
        if not isinstance(seconds, int):
            raise TypeError("Timeout must be an integer")
        if seconds <= 0:
            raise ValueError("Timeout must be positive")

        def apply(opt: dict) -> dict:
            opt["timeout"] = seconds
            return opt

        return apply

    @staticmethod
    def WithRotation(degrees: int) -> Option:
        """Set the rotation angle for the image.
        Must be one of 0, 90, 180, or 270 degrees."""
        if degrees not in (0, 90, 180, 270):
            raise ValueError("Rotation must be one of 0, 90, 180, 270")

        def apply(opt: dict) -> dict:
            if degrees != 0:  # Only include non-default rotation
                opt["rotate_angle"] = degrees
            return opt

        return apply

    @staticmethod
    def WithOCR(inline: bool = False, with_bounding_boxes: bool = False, detect_tables: bool = False) -> Option:
        """Enable Optical Character Recognition (OCR) for text extraction.
        Keyword arguments:
        inline -- If True, use inline OCR. Defaults to False.
        with_bounding_boxes -- If True, return text with bounding boxes. Defaults to False.
        detect_tables -- If True, detect tables in the file. Defaults to False.
        """

        def apply(opt: dict) -> dict:
            opt["with_ocr"] = True
            # Combo option is much cleaner here
            if inline:
                opt["inline_ocr"] = True
            if with_bounding_boxes:
                opt["with_bounding_boxes"] = True
            if detect_tables:
                opt["detect_tables"] = True
            return opt

        return apply


def get_text(file: BufferedReader, *options: Option) -> str:
    """
    Get text from a file using functional options.

    Args:
        file: The file to get text from.
        *options: Zero or more text processing options.

    Returns:
        The extracted text from the file.
    """
    # Start with default empty headers
    headers: dict = {}

    # Apply all options to build the headers
    for option in options:
        headers = option(headers)

    response = requests.post("dummy_url", data=file, headers=headers)
    return response.text


def example_usage():
    with open("example.pdf", "rb") as file:
        text = get_text(
            file,
            Options.WithTimeout(30),  # Options can take parameters!
            # Cleaner to set combo options :)
            Options.WithOCR(
                with_bounding_boxes=True,
                detect_tables=False,
            ),
            Options.WithRotation(180),
        )
        print(text)
