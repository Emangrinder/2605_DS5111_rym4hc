"""Unit tests for the Lab 4 transcript extraction pipeline.

Both tests use ``monkeypatch`` to swap the real ``youtube_transcript_api``
network call for an isolated stub, so the suite runs offline (and on GitHub
Actions) without ever touching the internet or needing a ``.env`` file.
"""
import sys
import io
import json

from youtube_transcript_api import YouTubeTranscriptApi

# Import the executable main entry point loop from your pipeline package directory.
from week4.extract_transcripts import main


class MockTranscriptContainer:
    """Mimics the 2026 .to_raw_data() array output return schema."""

    def to_raw_data(self):
        """Return a single fake transcript chunk."""
        return [
            {"start": 10.5, "text": "Automated container tracking loop text entry."}
        ]


def test_extract_transcripts_main_pipeline_stream(monkeypatch, capsys):
    """Success case: a valid ID streams exactly one well-formed JSON line.

    Verifies that the main() entrypoint loop correctly processes video IDs via
    stdin and outputs structured JSON Lines objects via stdout without hitting
    the internet.
    """
    # 1. Mock the external third-party API fetch dependency.
    def stubbed_fetch_route(self, video_id):  # pylint: disable=unused-argument
        return MockTranscriptContainer()

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_route)

    # 2. Mock standard input to feed a fake video ID into the script.
    monkeypatch.setattr(sys, "stdin", io.StringIO("fake_video_999\n"))

    # 3. Trigger the script's main entry point execution loop directly.
    main()

    # 4. Intercept the standard console terminal print buffers using capsys.
    captured_output = capsys.readouterr()
    stdout_lines = captured_output.out.strip().split("\n")

    # 5. Validate the emitted JSON Lines payload contract.
    assert len(stdout_lines) == 1, (
        "The pipeline loop should emit exactly one row per valid input ID."
    )

    parsed_json_line = json.loads(stdout_lines[0])
    assert parsed_json_line["video_id"] == "fake_video_999"
    assert "Automated container tracking" in parsed_json_line["raw_text"]


def test_extract_transcripts_handles_unfetchable_id(monkeypatch, capsys):
    """Error case: an unfetchable ID is caught; no crash and nothing emitted."""
    # 1. Mock the fetch dependency to blow up, as the real API would for a
    #    transcript-disabled or non-existent video.
    def failing_fetch(self, video_id):  # pylint: disable=unused-argument
        raise ValueError("Transcripts are disabled for this video")

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", failing_fetch)

    # 2. Feed a bad ID via stdin.
    monkeypatch.setattr(sys, "stdin", io.StringIO("bad_video_id\n"))

    # 3. main() must complete without propagating the exception.
    main()

    # 4. A failed fetch produces no JSON line on stdout.
    captured_output = capsys.readouterr()
    assert captured_output.out.strip() == ""


def test_never_gonna_give_you_up(monkeypatch, capsys):
    """🎵 Easter egg: a fully-offline rickroll for anyone who runs the suite.

    Still a legit pipeline test (mocked, no network) -- it just happens to feed
    the most well-known video ID on the internet.
    """
    rickroll_lyrics = [
        {"start": 43.0, "text": "Never gonna give you up"},
        {"start": 45.2, "text": "Never gonna let you down"},
        {"start": 47.3, "text": "Never gonna run around and desert you"},
    ]

    class RickRollTranscript:
        """Mock transcript container serving the classic."""

        def to_raw_data(self):
            return rickroll_lyrics

    monkeypatch.setattr(
        YouTubeTranscriptApi, "fetch", lambda self, video_id: RickRollTranscript()
    )
    monkeypatch.setattr(sys, "stdin", io.StringIO("dQw4w9WgXcQ\n"))

    main()

    captured = capsys.readouterr()
    payload = json.loads(captured.out.strip())
    assert payload["video_id"] == "dQw4w9WgXcQ"
    assert "Never gonna give you up" in payload["raw_text"]

    # Visible when run with `pytest -s`.
    print("\n🎵 You just got rickrolled by your own test suite. Never gonna let you down. 🎵")
