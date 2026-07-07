# 2605_DS5111_rym4hc

## Project Core Objective

This repo implements a small YouTube-transcript data pipeline for the DS5111 course.
Three streaming, UNIX-pipe-style stages, each reading JSON Lines (or plain text) from
`stdin` and writing to `stdout`:

1. **`bin/clean_ids.py`** — validates raw YouTube video ID strings (must be exactly 11
   characters from the modified Base64 character set), dropping anything invalid.
2. **`bin/extract_transcripts.py`** — takes clean video IDs and fetches raw transcript
   text from YouTube (optionally routed through a Webshare residential proxy), emitting
   `{"video_id", "raw_text"}` JSON objects.
3. **`bin/enrich_transcripts.py`** — takes raw transcripts and enriches them via an LLM
   (Google Gemini, wired in behind a Strategy-pattern `LLMStrategy` interface), emitting
   `{"video_id", "cleaned_text", "tech_terms", "book_names"}` JSON objects validated
   against a schema contract via `bin/validate_schema.py`.

Shared, vendor-agnostic infrastructure (e.g. logging setup) lives in `lib/`. One-time VM
bootstrap scripts live in `scripts/`. Test fixtures live in `tests/fixtures/`.

## Prerequisites / Starting Point

Before following these steps you should have:

- A fresh Ubuntu Server VM you can SSH into
- A GitHub SSH key already set up on the VM (so `git clone` over SSH works)

## Bootstrapping Instructions

### 1. Clone the repository

```bash
git clone git@github.com:Emangrinder/2605_DS5111_rym4hc.git
cd 2605_DS5111_rym4hc
```

### 2. Run the bootstrap script

Installs `make`, `python3.14-venv`, and `tree`:

```bash
cd scripts
bash init.sh
cd ..
```

**Quick test:** run `tree` from anywhere — if it lists files instead of throwing
"command not found," it worked.

### 3. Configure git credentials

```bash
cd scripts
bash init_git_creds.sh
cd ..
```

**Quick test:** the script echoes your global git config before and after. Confirm your
`user.email` and `user.name` are set correctly.

### 4. Build the Python virtual environment

```bash
make update
```

This runs `make env` (creates `env/`, upgrades pip) and then installs everything in
`requirements.txt` (`pandas`, `numpy`, `pylint`, `pytest`, `youtube-transcript-api`,
`python-dotenv`, `google-genai`).

**Quick test:**

```bash
. env/bin/activate
pip list
```

You should see `(env)` in your prompt and `pandas`/`pytest`/`google-genai` listed.

### 5. Configure environment variables

Create a `.env` file in the repo root (never commit this — it's gitignored):

```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

See the Environment Variables table below for the full set of supported keys.

## Environment Variables

| Variable | Required? | Used By | Purpose |
| --- | --- | --- | --- |
| `GEMINI_API_KEY` | Yes, for `bin/enrich_transcripts.py` | `enrich_transcripts.py` | Authenticates against the Google Gemini API. Pipeline fast-fails with a clear error if missing. |
| `WEBSHARE_USER` | No | `extract_transcripts.py` | Webshare residential proxy username. If unset, extraction falls back to direct local IP routing (fine for local dev; YouTube may rate-limit or block cloud IPs without a proxy). |
| `WEBSHARE_PASSWORD` | No | `extract_transcripts.py` | Webshare residential proxy password, paired with `WEBSHARE_USER`. |

All variables are loaded from a local `.env` file via `python-dotenv`; none should ever
be committed to git.

## Verification Steps

Once bootstrapped, confirm your environment is fully working:

```bash
make lint          # pylint across bin/ lib/ tests/ — should report 10.00/10
make test           # full pytest suite — should show all tests passed/xfailed/skipped as expected, zero failures
make test_enrich    # pipes tests/fixtures data + mock_transcripts.jsonl through the live enrich pipeline
                     # and bin/validate_schema.py — requires a valid GEMINI_API_KEY in .env
make run STAGE=extract   # launches bin/extract_transcripts.py, reads video IDs from stdin
make run STAGE=enrich    # launches bin/enrich_transcripts.py, reads raw transcripts (JSONL) from stdin
```

If `make lint` or `make test` fail, the CI workflow (`.github/workflows/ci.yml`) runs the
same two commands automatically on every push/PR across Python 3.11, 3.12, and 3.13 —
check the Actions tab for the same failures in a clean environment.

## Summary

After cloning, running `bash init.sh` and `bash init_git_creds.sh` (from `scripts/`),
`make update`, and creating a `.env` with `GEMINI_API_KEY`, the VM is fully ready for
development. Run `make lint && make test` to confirm.
