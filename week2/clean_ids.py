#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Name: clean_ids.py
Description: Filters youtube ids
Author: Emmett Hannam (rym4hc)
Date: 2026-06-01

Format
    Length: Exactly 11
    Character Set: (A-Z) (a-z) (0-9) (-) (_)
"""

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

