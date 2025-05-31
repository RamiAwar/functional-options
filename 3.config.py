from io import BufferedReader
from typing import Optional

import requests
from pydantic import BaseModel, field_validator


class TextExtractionConfig(BaseModel):
    """
    Configuration options for text extraction.

    Keyword arguments:
        as_plain_text -- If True, return the text as plain text. If False, return the text as HTML.
        with_ocr -- If True, use OCR to get text from the file. If False, do not use OCR.
        timeout -- The timeout for the OCR process in seconds. If None, no timeout is set.
        with_bounding_boxes -- If True, return the text with bounding boxes.
        inline_ocr -- If True, use inline OCR to get text from the file. If False, do not use inline OCR.
        ocr_with_text -- If True, use OCR with text. If False, do not use OCR with text.
        rotate_angle -- The angle to rotate the image before processing. Must be 0, 90, 180, or 270.
        detect_tables -- If True, detect tables in the file. If False, do not detect tables.
    """

    as_plain_text: bool = True
    with_ocr: bool = False
    timeout: Optional[int] = None
    with_bounding_boxes: bool = False
    inline_ocr: bool = False
    ocr_with_text: bool = False
    rotate_angle: int = 0  # 0, 90, 180, or 270
    detect_tables: bool = False

    @field_validator("timeout")
    def validate_timeout(cls, value):
        """Validate the timeout value."""
        if value is not None:
            if value <= 0:
                raise ValueError("Timeout must be positive")
        return value

    @field_validator("rotate_angle")
    def validate_rotate_angle(cls, value):
        """Validate the rotate_angle value."""
        if value not in [0, 90, 180, 270]:
            raise ValueError("rotate_angle must be 0, 90, 180, or 270")
        return value

    def to_headers(self) -> dict:
        """Convert the config to a headers dictionary, omitting default values."""
        headers = {}

        # Only include non-default values in the headers
        if self.timeout is not None:
            headers["timeout"] = self.timeout

        if self.rotate_angle != 0:
            headers["rotate_angle"] = self.rotate_angle

        if self.with_ocr:
            headers["with_ocr"] = True

            # Sub-options: ignore if with_ocr is False
            if self.with_bounding_boxes:
                headers["with_bounding_boxes"] = True
            if self.inline_ocr:
                headers["inline_ocr"] = True
            if self.detect_tables:
                headers["detect_tables"] = True

        if self.as_plain_text:
            headers["as_plain_text"] = True

        return headers


def get_text(file: BufferedReader, config: TextExtractionConfig | None = None) -> str:
    """
    Get text from a file using the provided configuration.

    Args:
        file: The file to get text from.
        config: Configuration options for text extraction.
               If None, default configuration will be used.

    Returns:
        The extracted text from the file.
    """
    if config is None:
        config = TextExtractionConfig()

    headers = config.to_headers()
    response = requests.post("dummy_url", data=file, headers=headers)
    return response.text


def example_usage():
    """
    Example usage of our config class implementation
    """
    with open("example_file.pdf", "rb") as file:
        config = TextExtractionConfig(
            as_plain_text=True,
            with_ocr=True,
            timeout=30,
            with_bounding_boxes=True,
            inline_ocr=True,
        )
        text = get_text(file, config)
        print(text)
