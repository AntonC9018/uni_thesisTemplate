from pathlib import Path


def test_each_case_has_fixture_and_assertions():
    cases_dir = Path(__file__).parent / "cases"
    case_dirs = sorted(
        path for path in cases_dir.iterdir() if path.is_dir() and path.name != "__pycache__"
    )

    assert case_dirs, "No regression test cases were found under tests/cases"
    for case_dir in case_dirs:
        assert (case_dir / "main.tex").is_file(), f"{case_dir.name} is missing main.tex"
        assert (case_dir / "test_case.py").is_file(), f"{case_dir.name} is missing test_case.py"
