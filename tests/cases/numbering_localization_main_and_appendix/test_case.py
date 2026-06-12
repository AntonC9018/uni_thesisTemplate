import pytest

from tests.lib.assertions import assert_build_succeeded, assert_log_not_contains, assert_pdf_contains
from tests.lib.latex import build_latex_case


@pytest.mark.parametrize(
    ("input_file", "expected_text"),
    [
        (
            "main.tex",
            ("Figura 1.1.", "Tabelul 1.1.", "(1.1)", "Figura A1.1.", "Tabelul A1.1.", "(A1.1)"),
        ),
        (
            "main_ru.tex",
            ("Рисунок 1.1.", "Таблица 1.1.", "(1.1)", "Рисунок П1.1.", "Таблица П1.1.", "(П1.1)"),
        ),
    ],
)
def test_main_to_appendix_numbering_and_localization(case_dir, tmp_path, input_file, expected_text):
    result = build_latex_case(case_dir, tmp_path, input_file)

    assert_build_succeeded(result)
    for text in expected_text:
        assert_pdf_contains(result, text)
    assert_log_not_contains(result, "Package config Warning")
