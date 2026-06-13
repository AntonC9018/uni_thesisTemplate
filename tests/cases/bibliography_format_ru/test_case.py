from tests.lib.assertions import assert_build_succeeded, assert_no_latex_error_markers, bibliography_text
from tests.lib.snapshots import assert_snapshot


def test_russian_bibliography_format_snapshot(build):
    assert_build_succeeded(build)
    assert_no_latex_error_markers(build)
    text = bibliography_text(build)
    for expected in (
        "Аудит системы управления информационной безопасностью",
        "Диссертация на соискание",
        "Молдавский стандарт ISO 690:2022",
        "закон об авторском праве",
        "Письмо",
    ):
        assert expected in text
    assert_snapshot(text, build.case_dir / "snapshots" / "bibliography_text.txt")
