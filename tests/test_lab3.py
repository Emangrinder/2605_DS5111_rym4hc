import sys
import io
import pytest
from week2.clean_ids import main

def load_youtube_ids_from_file(file_path="week2/weekly_youtube_ids"):
    """Reads the IDs from a file and returns them as a single newline-separated string."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Strip trailing/leading empty spaces from each line, keep only non-empty lines
            lines = [line.strip() for line in file if line.strip()]
            # Join them with newlines and add a trailing newline to simulate file EOF properly
            return "\n".join(lines) + "\n"
    except FileNotFoundError:
        return ""

def test_script_execution(monkeypatch, capsys):
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("kcFsuxaJ1es\nasd123\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()

    # 3. Capture the printed output
    captured = capsys.readouterr()
    
    # 4. Assert that the data was modified correctly
    assert captured.out == "kcFsuxaJ1es\n"

def test_script_io(monkeypatch, capsys):
    """Tests file values input matching outputs"""
    # # 5. Looping through "weekly_youtube_ids"
    # Call the helper function to load live file data
    file_data = load_youtube_ids_from_file("week2/weekly_youtube_ids")
    
    if not file_data.strip():
        pytest.fail("The 'weekly_youtube_ids' file is missing or empty.")
        
    # Overwrite stdin with the file contents and run the script logic
    fake_input = io.StringIO(file_data)
    monkeypatch.setattr(sys, "stdin", fake_input)
    main()
    
    # Capture the output produced by processing the live file
    file_captured = capsys.readouterr()
    actual_output = file_captured.out

    # Read and clean the answer file (handling potential double-newlines or extra whitespace)
    try:
        with open("week2/weekly_youtube_ids_ans", "r", encoding="utf-8") as ans_file:
            # Filter out empty lines to get a clean list of expected IDs
            expected_ids = [line.strip() for line in ans_file if line.strip()]
            # Reconstruct the target clean output format (one ID per line)
            expected_output = "\n".join(expected_ids) + "\n"
    except FileNotFoundError:
        pytest.fail("The answer file ('week2/weekly_youtube_ids_ans') could not be found.")

    # Strict assertion to verify the script output matches the answer key exactly
    assert actual_output == expected_output, (
        f"Output mismatch!\n"
        f"Expected:\n{expected_output}\n"
        f"Got:\n{actual_output}"
    )

def test_script_hardware():
    """Tests hardware and software versions to ensure quality"""
    # 6. Test what OS the code is running on (Expected to pass on Ubuntu)
    def test_check_os():
        current_os = platform.system()
        # platform.system() returns 'Linux' on Ubuntu
        assert current_os == "Linux", f"Expected Linux, but got {current_os}"

    # 7. Test the version of Python running in the environment
    def test_check_python_version():
        required_major = 3
        required_minor = 10 # Change to match your target version
    
        # sys.version_info returns a tuple like (3, 10, 2, 'final', 0)
        assert sys.version_info.major == required_major
        assert sys.version_info.minor >= required_minor

    # 8. Test that is expected to fail
    @pytest.mark.xfail(reason="This feature is not yet built")
    def test_expected_to_fail():
        # This assertion will fail, but pytest will mark it as XFAIL (expected fail)
        assert 1 == 2

    # 9. Test that is expected to be skipped
    @pytest.mark.skip(reason="Feature is not ready yet")
    def test_feature_not_ready():
        assert True

    # 10. Parametrized test
    @pytest.mark.parametrize("input_val, expected_val", [
        (2, 4),
        (3, 9),
        (5, 25)
    ])
    def test_squared_values(input_val, expected_val):
        assert input_val ** 2 == expected_val
