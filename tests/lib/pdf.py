from __future__ import annotations

from pathlib import Path

import fitz


def pdf_text(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text("text") for page in doc)


def page_texts(pdf_path: Path) -> list[str]:
    with fitz.open(pdf_path) as doc:
        return [page.get_text("text") for page in doc]


def text_spans(pdf_path: Path) -> list[dict]:
    spans: list[dict] = []
    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            text = page.get_text("dict")
            for block in text["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        value = span["text"].strip()
                        if not value:
                            continue
                        spans.append(
                            {
                                "page": page_index,
                                "text": value,
                                "bbox": fitz.Rect(span["bbox"]),
                                "color": span.get("color"),
                            }
                        )
    return spans


def page_words(pdf_path: Path, page_index: int) -> list[dict]:
    with fitz.open(pdf_path) as doc:
        page = doc[page_index]
        words = []
        for word in page.get_text("words"):
            words.append({"text": word[4], "bbox": fitz.Rect(word[:4])})
        return words


def page_count(pdf_path: Path) -> int:
    with fitz.open(pdf_path) as doc:
        return doc.page_count


def rect_center_y(rect: fitz.Rect) -> float:
    return (rect.y0 + rect.y1) / 2.0


def union_rect(rects: list[fitz.Rect]) -> fitz.Rect:
    if not rects:
        raise AssertionError("Cannot union an empty rectangle list")
    result = fitz.Rect(rects[0])
    for rect in rects[1:]:
        result.include_rect(rect)
    return result


def find_link_destination_for_text(pdf_path: Path, visible_text: str) -> int | None:
    with fitz.open(pdf_path) as doc:
        for page in doc:
            links = page.get_links()
            for rect in page.search_for(visible_text):
                for link in links:
                    link_rect = fitz.Rect(link["from"])
                    if link_rect.intersects(rect) and "page" in link:
                        return int(link["page"])
    return None
