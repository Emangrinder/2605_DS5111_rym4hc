#!/usr/bin/env python3
"""Pipeline Step 2B: enrich raw transcripts with Google Gemini.

Reads JSON Lines from stdin (each with ``video_id`` and ``raw_text``), asks the
Gemini model to clean the text and pull out technical terms and book names under
a strict response schema (an API data contract), and streams one schema-compliant
JSON object per line to stdout. Built on the same stream/logging conventions as
``week4/extract_transcripts.py``.
"""
import sys
import os
import json
import logging

from abc import ABC, abstractmethod
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Conditionally load credentials from a local .env file if one is present.
load_dotenv()

# Direct logging statements to a shared audit log asset. Ensure the directory
# exists first so simply importing this module never fails (e.g. under CI,
# where logs/ does not exist yet).
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "pipeline_audit.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LLMStrategy (ABC): # pylint: disable=too-few-public-methods
    """Abstract contract for LLM enrichment strategies."""
    @abstractmethod
    def enrich(self, video_id: str, raw_text: str) -> dict:
        """Must accept raw transcript text and return an enriched schema dict."""

class GeminiStrategy(LLMStrategy):  # pylint: disable=too-few-public-methods
    """Concrete LLMStrategy that enriches transcripts via Google Gemini."""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.response_schema = {
            "type": "OBJECT",
            "properties": {
                "video_id": {"type": "STRING"},
                "cleaned_text": {"type": "STRING"},
                "tech_terms": {"type": "ARRAY", "items": {"type": "STRING"}},
                "book_names": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["video_id", "cleaned_text", "tech_terms", "book_names"],
        }

    def enrich(self, video_id: str, raw_text: str) -> dict:
        """Send raw transcript text to Gemini and return the enriched schema dict."""
        prompt = f"""
            You are an elite data engineer. Clean this transcript text for video_id '{video_id}'.
            1. Strip all timestamps and duration codes.
            2. Extract technical architecture terms and books.
            """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{prompt}\n\nTRANSCRIPT:\n{raw_text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=self.response_schema,
                ),
            )
            return json.loads(response.text)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise RuntimeError(f"Gemini enrichment failed for {video_id}: {exc}") from exc

def main():
    """Stream JSONL transcripts from stdin to Gemini-enriched JSONL on stdout."""
    logging.info("Pipeline Step 2B (Gemini Enrichment) started.")

    # 1. API environment validation and client initialization (fast-fail).
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.critical("GEMINI_API_KEY is not set. Aborting pipeline.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    # 2. Structured output response schema -- the downstream data contract.
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "video_id": {"type": "STRING"},
            "cleaned_text": {"type": "STRING"},
            "tech_terms": {"type": "ARRAY", "items": {"type": "STRING"}},
            "book_names": {"type": "ARRAY", "items": {"type": "STRING"}},
        },
        "required": ["video_id", "cleaned_text", "tech_terms", "book_names"],
    }

    # Process streaming JSON lines from stdin.
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # 3. Safe, row-isolated deserialization of the inbound JSON line.
        try:
            record = json.loads(line)
            video_id = record["video_id"]
            raw_text = record["raw_text"]
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.error("Failed to parse incoming JSON payload row: %s", str(exc))
            continue

        logging.info("Orchestrating Gemini enrichment for video: %s", video_id)

        prompt = f"""
        You are an elite data engineer. Clean this transcript text for video_id '{video_id}'.
        1. Strip all timestamps and duration codes.
        2. Extract technical architecture terms and books.
        """

        # 4. Structured model invocation and instant stream flushing.
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{prompt}\n\nTRANSCRIPT:\n{raw_text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                ),
            )
            # Re-serialize compactly so each record is exactly one JSON Lines row
            # (Gemini may pretty-print its structured output across several lines).
            enriched = json.loads(response.text)
            sys.stdout.write(json.dumps(enriched) + "\n")
            sys.stdout.flush()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.error(
                "Failed processing video %s during LLM generation: %s", video_id, str(exc)
            )

    logging.info("Pipeline Step 2B finished.")

if __name__ == "__main__":
    main()
