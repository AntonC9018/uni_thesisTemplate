from tests.lib.assertions import assert_build_succeeded, assert_toc_row_links_to_text


def test_toc_rows_have_internal_links_to_their_targets(build):
    assert_build_succeeded(build)
    for toc_text, target_text in (
        ("Unnumbered Link Target", "UNNUMBERED LINK TARGET"),
        ("Introducere", "INTRODUCERE"),
        ("Numbered Link Target", "NUMBERED LINK TARGET"),
        ("Section Link Target", "Section Link Target"),
        ("Bibliografie", "BIBLIOGRAFIE"),
        ("Anexe", "ANEXE"),
        ("Appendix Link Target", "Appendix Link Target"),
    ):
        assert_toc_row_links_to_text(build, toc_text, target_text)
