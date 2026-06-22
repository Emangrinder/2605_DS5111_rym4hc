# Lab 2: YouTube ID Cleaner Submission

1. Lab Source Link

*  https://github.com

2. Code Description

* This Python script (`clean_ids.py`) acts as a component in a Linux data pipeline to process and sanitize incoming YouTube video IDs from a stream (`sys.stdin`). It filters out invalid records by ensuring every ID is exactly 11 characters long and strictly composed of the modified Base64 character set (`A-Z`, `a-z`, `0-9`, `-`, `_`). Valid IDs are output cleanly to the console, while invalid elements are silently captured and written to a dedicated log file.

3. Verification & Testing

I verified that the script functions exactly as required through the following manual tests:

* **Pipeline Testing:** Ran `cat weekly_youtube_ids | ./clean_ids.py` 
* **Log Verification:** Checked `pipeline_autid.log` after execution and confirmed that both `abcd` and `1234` were successfully logged as errors.
* **Interactive Mode Testing:** Ran `python3 clean_ids.py` directly. Verified that typing `1234` produced no echo, typing `CctJNYYCPo0` echoed instantly due to output flushing, and pressing `Ctrl-C` gracefully exited the process back to the terminal prompt without an error traceback.

4. Additional Notes

* The script utilizes Python's built-in `logging` module to handle error tracking.
* Output flushing (`flush=True`) was explicitly added to ensure real-time terminal feedback during interactive CLI mode execution.

