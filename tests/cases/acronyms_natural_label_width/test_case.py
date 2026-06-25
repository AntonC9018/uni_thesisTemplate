from tests.lib import pdf
from tests.lib.assertions import assert_build_succeeded


def find_word(words, text):
    return next(word for word in words if word["text"] == text)


def test_acronym_label_column_uses_natural_width(build):
    assert_build_succeeded(build)
    pages = pdf.page_texts(build.pdf_path)
    glossary_page = next(index for index, text in enumerate(pages) if "СПИСОК СОКРАЩЕНИЙ" in text)
    words = pdf.page_words(build.pdf_path, glossary_page)

    widest_label = find_word(words, "ICT/ИКТ")
    first_definition_word = find_word(words, "Artificial")

    assert first_definition_word["bbox"].x0 - widest_label["bbox"].x1 < 40


def test_api_definition_fits_on_one_line(build):
    assert_build_succeeded(build)
    pages = pdf.page_texts(build.pdf_path)
    glossary_page = next(index for index, text in enumerate(pages) if "СПИСОК СОКРАЩЕНИЙ" in text)
    words = pdf.page_words(build.pdf_path, glossary_page)

    definition_words = [
        find_word(words, text)
        for text in (
            "Application",
            "Programming",
            "Interface,",
            "программный",
            "интерфейс",
            "приложения",
        )
    ]

    y_positions = [word["bbox"].y0 for word in definition_words]
    assert max(y_positions) - min(y_positions) <= 2.0
