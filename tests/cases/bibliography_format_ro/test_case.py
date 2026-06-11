from tests.lib.assertions import assert_build_succeeded, assert_no_latex_error_markers, bibliography_text
from tests.lib.snapshots import assert_snapshot


def test_romanian_bibliography_format_snapshot(build):
    assert_build_succeeded(build)
    assert_no_latex_error_markers(build)
    text = bibliography_text(build)
    for expected in (
        "Auditul sistemului de management al securității informației",
        "Teză de doctor",
        "Standard Moldovenesc ISO 690:2022",
        "Lege organică privind dreptul de autor",
        "Scrisoare",
    ):
        assert expected in text
    assert_snapshot(text, build.case_dir / "snapshots" / "bibliography_text.txt")
