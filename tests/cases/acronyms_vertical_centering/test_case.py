from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded


def test_acronym_rows_are_vertically_centered(build):
    assert_build_succeeded(build)
    pages = pdf.page_texts(build.pdf_path)
    glossary_page = next(index for index, text in enumerate(pages) if "LISTA ABREVIERELOR" in text)
    words = pdf.page_words(build.pdf_path, glossary_page)

    label = next(word for word in words if word["text"] == "LONG")
    label_rect = label["bbox"]
    definition_rects = [
        word["bbox"]
        for word in words
        if word["bbox"].x0 > label_rect.x1
        and label_rect.y0 - 30 <= word["bbox"].y0 <= label_rect.y1 + 30
        and word["text"] not in {"Lista", "abrevierelor"}
    ]
    definition_rect = pdf.union_rect(definition_rects)

    assert abs(pdf.rect_center_y(label_rect) - pdf.rect_center_y(definition_rect)) <= 2.0
