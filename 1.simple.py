from io import BufferedReader
import requests

def get_text(
    *,
    file: BufferedReader,
    as_plain_text: bool = True,
    with_ocr: bool = False,
) -> str:
    """
    Get text from a file.

    Keyword arguments:
    file -- The file to get text from.
    as_plain_text -- If True, return the text as plain text. If False, return the text as HTML.
    with_ocr -- If True, use OCR to get text from the file. If False, do not use OCR.
    """
    headers = {}

    if not with_ocr:
        headers["SkipOCR"] = "true"

    if as_plain_text:
        headers["Accept"] = "text/plain"

    response = requests.post("dummy_url", data=file, headers=headers)
    return response.text
