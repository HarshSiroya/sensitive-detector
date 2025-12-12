from pathlib import Path
from typing import List
import re
import logging
from PyPDF2 import PdfReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(path: str) -> str:
    p = Path(path) ## create a Path object from the path string
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    reader = PdfReader(str(p)) ## create a PdfReader object from the path string
    pages = [] ## create an empty list to store the pages
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            logger.warning("Failed to extract page %s: %s", i, e)
            text = ""
        pages.append(text)
    full_text = "/n/n".join(pages)
    full_text = re.sub(r"\r\n?", "\r", full_text)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    full_text = re.sub(r"[ \t]{2,}", " ", full_text)
    return full_text.strip()
        
