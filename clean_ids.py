#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Name: clean_ids.py
Description: Filters non-urls
Author: Emmett Hannam (rym4hc)
Date: 2026-06-01

Length: Exactly 11 characters.
Character Set: Uses a modified Base64 encoding consisting of the following 64 possibilities:
    Uppercase letters (A-Z)
    Lowercase letters (a-z)
    Numbers (0-9)
    Hyphen (-)
    Underscore (_)
"""

#!/usr/bin/env python3
import logging
import string
import sys

logging.basicConfig(
    filename="pipeline_autid.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    CHAR_SET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"
    VALID_CHARS = set(CHAR_SET)

    try:
        for line in sys.stdin:
            words = line.split()

            for word in words:
                if len(word) == 11 and all(char in VALID_CHARS for char in word):
                    print(word, flush=True)
                else:
                    logging.info(f"Invalid ID: {word}")

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()

