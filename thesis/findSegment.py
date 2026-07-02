import sys
import os
import hashlib
from pathlib import Path

from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.util import ClassNotFound

MINTED_ALIAS_UNSAFE_CHARS = set("\\{}#$%&_~^/")


def latex_escape(value):
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "_": r"\_",
        "^": r"\textasciicircum{}",
        "~": r"\textasciitilde{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def print_warning(segment_name, file_path):
    print(
        "\\codeSegmentWarning"
        f"{{{latex_escape(segment_name)}}}"
        f"{{{latex_escape(file_path)}}}",
        flush=True,
    )


def print_unsupported_language_warning(language, file_path):
    print(
        "\\codeSegmentUnsupportedLanguageWarning"
        f"{{{latex_escape(language)}}}"
        f"{{{latex_escape(file_path)}}}",
        flush=True,
    )


def generated_segment_path(file_path, segment_name, language):
    cache_key = f"{Path(file_path).resolve()}\0{segment_name}".encode("utf-8")
    file_hash = hashlib.sha256(cache_key).hexdigest()[:16]
    segment_dir = Path("generated-code-segments")
    segment_dir.mkdir(exist_ok=True)
    return segment_dir / f"{file_hash}.{language}"


def safe_minted_alias(lexer, preferred_alias=None):
    aliases = getattr(lexer, "aliases", ())
    if preferred_alias in aliases and is_safe_minted_alias(preferred_alias):
        return preferred_alias

    for alias in aliases:
        if is_safe_minted_alias(alias):
            return alias

    return aliases[0] if aliases else None


def is_safe_minted_alias(alias):
    return not any(char in MINTED_ALIAS_UNSAFE_CHARS for char in alias)


def minted_language_for_file(file_path):
    path = Path(file_path)
    extension = path.suffix.lstrip(".").lower()

    if extension:
        try:
            lexer = get_lexer_by_name(extension)
            alias = safe_minted_alias(lexer, extension)
            if alias:
                return alias, extension
        except ClassNotFound:
            pass

    try:
        lexer = get_lexer_for_filename(str(path))
    except ClassNotFound:
        return None, extension or "unknown"

    alias = safe_minted_alias(lexer)
    if not alias:
        return None, extension or "unknown"

    return alias, extension or alias


def main():
    filePath = sys.argv[1]
    segmentName = sys.argv[2]
    extraOptions = sys.argv[3].strip() if len(sys.argv) > 3 else ""
    language, requested_language = minted_language_for_file(filePath)

    if language is None:
        print_unsupported_language_warning(requested_language, filePath)
        return 0

    if not os.path.exists(filePath):
        print_warning(segmentName, filePath)
        return 0

    segmentBeginString = f"Segment {segmentName} begin"
    segmentEndString = f"Segment {segmentName} end"

    segmentBegin = -1
    segmentEnd = -1
    lines = []
    with open(filePath, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for index, line in enumerate(lines):
            if segmentBeginString in line:
                segmentBegin = index
            if segmentEndString in line:
                segmentEnd = index

    if segmentBegin == -1 or segmentEnd == -1 or segmentEnd <= segmentBegin:
        print_warning(segmentName, filePath)
        return 0

    segment_path = generated_segment_path(filePath, segmentName, language)
    segment_path.write_text("".join(lines[segmentBegin + 1 : segmentEnd]), encoding="utf-8")

    options = f"firstnumber={segmentBegin + 2}"
    if extraOptions:
        options = f"{options},{extraOptions}"

    print(f"\\inputminted[{options}]{{{language}}}{{{segment_path}}}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.stderr.close()
