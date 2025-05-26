from io import BufferedReader
from typing import Any
import requests


def get_text(
        *,
        file: BufferedReader,
        as_plain_text: bool = True,
        with_ocr: bool = False,
        timeout: int | None = None,
        with_bounding_boxes: bool = False,
        inline_ocr: bool = False,
        ocr_with_text: bool = False,
        rotate_angle: int = 0,  # 0, 90, 180, or 270
        detect_tables: bool = False,
) -> str:
    """
    Get text from a file.

    Keyword arguments:
    file -- The file to get text from.
    as_plain_text -- If True, return the text as plain text. If False, return the text as HTML.
    with_ocr -- If True, use OCR to get text from the file. If False, do not use OCR.
    timeout -- The timeout for the OCR process in seconds. If None, no timeout is set.
    with_bounding_boxes -- If True, return the text with bounding boxes. If False, return the text without bounding boxes.
    inline_ocr -- If True, use inline OCR to get text from the file. If False, do not use inline OCR.
    ocr_with_text -- If True, use OCR with text. If False, do not use OCR with text.
    rotate_angle -- The angle to rotate the image before processing. Must be 0, 90, 180, or 270.
    detect_tables -- If True, detect tables in the file. If False, do not detect tables.
    """
    headers: dict[str, Any] = {}

    if timeout is not None:
        # Check timeout integer
        if not isinstance(timeout, int):
            raise TypeError("Timeout must be an integer")

        # Check timeout positive
        if timeout <= 0:
            raise ValueError("Timeout must be positive")

        headers["timeout"] = timeout

    # Check rotation is 0, 90, 180, or 270
    if rotate_angle not in [0, 90, 180, 270]:
        raise ValueError("rotate_angle must be 0, 90, 180, or 270")
    if rotate_angle != 0:
        headers["rotate_angle"] = rotate_angle

    if detect_tables:
        headers["detect_tables"] = True

    if with_bounding_boxes:
        headers["with_bounding_boxes"] = True

    if ocr_with_text:
        headers["ocr_with_text"] = True

    if as_plain_text:
        headers["as_plain_text"] = True

    if not with_ocr:
        headers["SkipOCR"] = "true"

    if inline_ocr:
        headers["inline_ocr"] = "true"

    if as_plain_text:
        headers["Accept"] = "text/plain"

    response = requests.post("dummy_url", data=file, headers=headers)
    return response.text


def example_usage():
    # Example usage of our extended function implementation
    with open("example.pdf", "rb") as file:
        text = get_text(
            file=file,
            as_plain_text=True,
            with_ocr=True,
            timeout=30,
            with_bounding_boxes=True,
            inline_ocr=True,
            ocr_with_text=True,
            rotate_angle=90,
            detect_tables=True
        )
        print(text)
