from pathlib import Path

import pytest

from tests.lib.latex import build_latex_case


@pytest.fixture
def case_dir(request) -> Path:
    return Path(str(request.fspath)).parent


@pytest.fixture
def build(case_dir: Path, tmp_path: Path):
    return build_latex_case(case_dir, tmp_path)
