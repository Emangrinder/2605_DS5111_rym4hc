"""Lint and pytest suite for the clean_ids script (Lab 3).

Covers:
  - stdin/stdout behavior of clean_ids.main()
  - live input compared against the answer key
  - environment checks (OS, Python version)
  - an expected-fail test, a skipped test, and a parametrized test
"""

import io
import platform
import sys

import pytest

from bin.clean_ids import main


def load_youtube_ids_from_file(file_path="tests/fixtures/weekly_youtube_ids"):
    """Read IDs from a file and return them as a single newline-separated string."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Strip whitespace per line and keep only the non-empty lines.
            lines = [line.strip() for line in file if line.strip()]
            # Join with newlines and add a trailing newline to simulate file EOF.
            return "\n".join(lines) + "\n"
    except FileNotFoundError:
        return ""


# --- Script behavior tests -------------------------------------------------

def test_script_execution(monkeypatch, capsys):
    """One good ID and one bad line: only the good ID should be emitted."""
    # 1. Simulate stdin with a readable stream.
    fake_input = io.StringIO("kcFsuxaJ1es\nasd123\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic.
    main()

    # 3. Capture stdout.
    captured = capsys.readouterr()

    # 4. Assert the data was cleaned correctly.
    assert captured.out == "kcFsuxaJ1es\n"


def test_script_io(monkeypatch, capsys):
    """Live input file should clean to exactly match the answer key."""
    # 5. Load live file data via the helper.
    file_data = load_youtube_ids_from_file("tests/fixtures/weekly_youtube_ids")
    if not file_data.strip():
        pytest.fail("The 'weekly_youtube_ids' file is missing or empty.")

    # Feed the file contents in as stdin and run the script.
    fake_input = io.StringIO(file_data)
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()

    file_captured = capsys.readouterr()
    actual_output = file_captured.out

    # Read and clean the answer file (handling extra whitespace / blank lines).
    try:
        with open("tests/fixtures/weekly_youtube_ids_ans", "r", encoding="utf-8") as ans_file:
            expected_ids = [line.strip() for line in ans_file if line.strip()]
            expected_output = "\n".join(expected_ids) + "\n"
    except FileNotFoundError:
        pytest.fail("The answer file ('tests/fixtures/weekly_youtube_ids_ans') could not be found.")

    # Strict comparison: script output must match the answer key exactly.
    assert actual_output == expected_output, (
        f"Output mismatch!\n"
        f"Expected:\n{expected_output}\n"
        f"Got:\n{actual_output}"
    )


# --- Environment tests -----------------------------------------------------

def test_check_os():
    """6. The code is expected to run on Linux (Ubuntu)."""
    current_os = platform.system()  # platform.system() returns 'Linux' on Ubuntu.
    assert current_os == "Linux", f"Expected Linux, but got {current_os}"


def test_check_python_version():
    """7. Verify the interpreter meets the minimum supported version."""
    required_major = 3
    required_minor = 10  # Change to match your target version.
    # sys.version_info looks like (3, 10, 2, 'final', 0).
    assert sys.version_info.major == required_major
    assert sys.version_info.minor >= required_minor


@pytest.mark.xfail(reason="This feature is not yet built")
def test_expected_to_fail():
    """8. Known-failing assertion; pytest reports it as XFAIL."""
    assert 1 == 2 # pylint: disable=comparison-of-constants


@pytest.mark.skip(reason="Feature is not ready yet")
def test_feature_not_ready():
    """9. Placeholder test, skipped until the feature lands."""
    assert True


@pytest.mark.parametrize("input_val, expected_val", [
    (2, 4),
    (3, 9),
    (5, 25),
])
def test_squared_values(input_val, expected_val):
    """10. Parametrized: each input squared equals the expected value."""
    assert input_val ** 2 == expected_val


# --- Additional required tests (Lab 3, Part 2) -----------------------------

def test_multiple_good_ids_interspersed_with_bad_lines(monkeypatch, capsys):
    """Several valid IDs mixed with junk lines: only the valid IDs are emitted, in order."""
    stdin_data = (
        "kcFsuxaJ1es\n"   # valid (11 chars)
        "this is junk\n"  # invalid: three short words
        "CctJNYYCPo0\n"   # valid (11 chars)
        "1234\n"          # invalid: too short
        "dQw4w9WgXcQ\n"   # valid (11 chars)
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_data))

    main()

    captured = capsys.readouterr()
    assert captured.out == "kcFsuxaJ1es\nCctJNYYCPo0\ndQw4w9WgXcQ\n"


@pytest.mark.parametrize("bad_id", [
    "abcdefghij",    # 10 chars -> too short
    "abcdefghijkl",  # 12 chars -> too long
])
def test_ids_outside_length_range_are_rejected(bad_id, monkeypatch, capsys):
    """Only IDs of exactly 11 chars are valid; 10- and 12-char IDs must be dropped."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(bad_id + "\n"))

    main()

    captured = capsys.readouterr()
    assert captured.out == "", (
       f"Expected no output for length-{len(bad_id)} id, got {captured.out!r}"
    )

def test_exactly_eleven_chars_passes_length_check(monkeypatch, capsys):
    """Boundary: an ID of exactly 11 valid characters is accepted."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("abcdefghijk\n"))

    main()

    captured = capsys.readouterr()
    assert captured.out == "abcdefghijk\n"
