"""Tests for the enrich_transcripts pipeline: real-SDK mock and Strategy-pattern mock."""
import sys
import io
import json

from google.genai.models import Models
from bin.enrich_transcripts import main, TranscriptEnricher, LLMStrategy

class MockLLMStrategy(LLMStrategy):  # pylint: disable=too-few-public-methods
    """Test double for LLMStrategy — returns a canned response, no network calls."""

    def enrich(self, video_id: str, raw_text: str) -> dict:
        return {
            "video_id": video_id,
            "cleaned_text": raw_text.strip().lower(),
            "tech_terms": ["mock_term"],
            "book_names": ["Mock Book"],
        }

# 1. Build a dummy container mimicking the Gemini SDK response hierarchy
class MockGeminiResponse: # pylint: disable=too-few-public-methods
    """Dummy container mimicking the Gemini SDK response object (.text attribute)."""
    def __init__(self, text_payload):
        self.text = text_payload

def test_enrich_transcripts_streaming_pipeline(monkeypatch, capsys):
    """
    Verifies that main() reads mock lines from stdin, calls the Gemini client structure,
    and streams verified JSON objects out to stdout without making live API network requests.
    """
    # A dummy key so TODO 1's fast-fail check passes offline. CI has no .env, so
    # without this the script would log CRITICAL and sys.exit(1) before streaming.
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")

    # 2. Mock out the core GenAI Client methods
    def mock_generate_content(self, model, contents, config=None): # pylint: disable=unused-argument
        # Return a pre-baked, schema-compliant JSON string mimicking the model output
        mock_data = {
            "video_id": "ds5111_v001",
            "cleaned_text": "Welcome to class. Today we are testing mock frameworks.",
            "tech_terms": ["mock frameworks"],
            "book_names": []
        }
        return MockGeminiResponse(json.dumps(mock_data))

    # Corrected Module Target: Patch the actual Models service class inside the SDK
    monkeypatch.setattr(Models, "generate_content", mock_generate_content)

    # 3. Simulate your stream input pipeline using an in-memory text buffer
    mock_input_row = {
        "video_id": "ds5111_v001",
        "raw_text": "00:01 Welcome to class. Today we are testing mock frameworks.",
    }
    mock_stdin = io.StringIO(json.dumps(mock_input_row) + "\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)

    # 4. Trigger the main pipeline script execution loop
    main(argv=[])

    # 5. Intercept the standard console text buffers
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split("\n")

    # 6. Execute data integrity validation assertions
    assert len(stdout_lines) == 1
    parsed_output = json.loads(stdout_lines[0])
    assert parsed_output["video_id"] == "ds5111_v001"
    assert "mock frameworks" in parsed_output["tech_terms"]

def test_transcript_enricher_with_mock_strategy(monkeypatch, capsys):
    """Verifies TranscriptEnricher processes stdin/stdout correctly using a
    dummy strategy — no live network calls, no SDK involved."""
    mock_input_row = {"video_id": "test_v001", "raw_text": "  RAW transcript text  "}
    mock_stdin = io.StringIO(json.dumps(mock_input_row) + "\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)

    enricher = TranscriptEnricher(MockLLMStrategy())
    enricher.run_stream()

    captured = capsys.readouterr()
    parsed_output = json.loads(captured.out.strip())
    assert parsed_output["video_id"] == "test_v001"
    assert parsed_output["tech_terms"] == ["mock_term"]
