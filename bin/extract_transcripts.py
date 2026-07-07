#!/usr/bin/env python3
"""Pipeline Step 2A: extract raw YouTube transcripts.

Reads video IDs from stdin (one per line) and emits one JSON object per line
(JSON Lines) to stdout, each containing ``video_id`` and ``raw_text``. Network
access is routed through a Webshare residential proxy when credentials are
present in the environment (loaded from a local ``.env`` file); otherwise it
falls back to the direct local IP for local testing.
"""
import sys
import os
import json
import logging

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from lib.pipeline_logging import configure_pipeline_logging

# Conditionally load credentials from a local .env file if one is present.
load_dotenv()

# Direct logging statements to a shared audit log asset. Ensure the directory
# exists first so simply importing this module never fails (e.g. under CI,
# where pipeline/logs/ does not exist yet).
configure_pipeline_logging(log_dir="pipeline/logs")

def main():
    """Stream video IDs from stdin to JSON Lines transcripts on stdout."""
    logging.info("Pipeline Step 2A (Raw Extraction) started.")

    # Ingest routing keys from the local shell environment.
    proxy_user = os.getenv("WEBSHARE_USER")
    proxy_pass = os.getenv("WEBSHARE_PASSWORD")

    if proxy_user and proxy_pass:
        logging.info(
            "Proxy credentials detected. Routing traffic via Webshare Residential network."
        )
        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_user,
                proxy_password=proxy_pass,
            )
        )
    else:
        logging.warning(
            "No proxy credentials found. Running with direct raw local IP routing."
        )
        ytt_api = YouTubeTranscriptApi()

    # Process streaming IDs line-by-line from stdin.
    for line in sys.stdin:
        video_id = line.strip()
        if not video_id:
            continue

        logging.info("Processing transcript extraction for video: %s", video_id)

        try:
            # Execute the modern 2026 instance lookup method.
            fetched_transcript = ytt_api.fetch(video_id)
            transcript_list = fetched_transcript.to_raw_data()

            # Stitch chunks with timestamp codes preserved for the staging file.
            raw_text = " ".join(
                f"[{item['start']}] {item['text']}" for item in transcript_list
            )

            # Pack into a simple intermediary JSON object and emit to stdout.
            payload = {"video_id": video_id, "raw_text": raw_text}
            sys.stdout.write(json.dumps(payload) + "\n")
            sys.stdout.flush()

        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Fail gracefully: a bad/unfetchable ID must not crash the stream.
            logging.error(
                "Failed to fetch YouTube transcript for %s: %s", video_id, str(exc)
            )
            continue

    logging.info("Pipeline Step 2A finished.")


if __name__ == "__main__":
    main()
