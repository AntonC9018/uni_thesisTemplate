import pytest

from tests.lib.assertions import (
    assert_build_succeeded,
    assert_log_not_contains,
    assert_pdf_contains,
    assert_pdf_text_is_linked,
)
from tests.lib.latex import build_latex_case


@pytest.mark.parametrize(
    ("input_file", "expected_text"),
    [
        (
            "main.tex",
            (
                "figură 1.1",
                "figura 1.1",
                "figurii 1.1",
                "o figură 1.1",
                "unei figuri 1.1",
                "figuri 1.1",
                "figurile 1.1",
                "figurilor 1.1",
                "niște figuri 1.1",
                "unor figuri 1.1",
                "Figurile 1.1, 1.2 și 1.3",
                "Figurile 1.1 și 1.2 păstrează spațiul.",
                "Tabelul 1.1",
                "tabelului 1.1",
                "un tabel 1.1",
                "unui tabel 1.1",
                "Tabelele 1.1",
                "tabelelor 1.1",
                "niște tabele 1.1",
                "unor tabele 1.1",
                "Codul 1.1",
                "codului 1.1",
                "un cod 1.1",
                "unui cod 1.1",
                "Codurile 1.1",
                "codurilor 1.1",
                "niște coduri 1.1",
                "unor coduri 1.1",
            ),
        ),
        (
            "main_ru.tex",
            (
                "рисунок 1.1",
                "рисунка 1.1",
                "рисунку 1.1",
                "рисунком 1.1",
                "рисунке 1.1",
                "рисунки 1.1",
                "рисунков 1.1",
                "рисункам 1.1",
                "рисунками 1.1",
                "рисунках 1.1",
                "Рисунки 1.1, 1.2 и 1.3",
                "Рисунки 1.1 и 1.2 демонстрируют пробел.",
                "Таблица 1.1",
                "таблицу 1.1",
                "таблице 1.1",
                "Таблицы 1.1",
                "таблиц 1.1",
                "таблицах 1.1",
                "Листинг 1.1",
                "листингом 1.1",
                "Листинги 1.1",
                "листингов 1.1",
                "листингами 1.1",
                "Уравнение (1.1)",
                "Глава I",
            ),
        ),
    ],
)
def test_object_case_helpers_render_localized_words(case_dir, tmp_path, input_file, expected_text):
    result = build_latex_case(case_dir, tmp_path, input_file)

    assert_build_succeeded(result)
    for text in expected_text:
        assert_pdf_contains(result, text)
    assert_log_not_contains(result, "Package config Warning")


@pytest.mark.parametrize(
    ("input_file", "linked_words"),
    [
        ("main.tex", ("figură", "Figurile", "Tabelul", "Codul", "Tabelele")),
        ("main_ru.tex", ("рисунок", "Рисунки", "Таблица", "Листинг", "Таблицы")),
    ],
)
def test_object_reference_words_are_inside_pdf_links(case_dir, tmp_path, input_file, linked_words):
    result = build_latex_case(case_dir, tmp_path, input_file)

    assert_build_succeeded(result)
    for word in linked_words:
        assert_pdf_text_is_linked(result, word)
