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

import string
import sys


def main():
    input_text = sys.stdin.read()
    words = input_text.split()

    CHAR_SET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"
    CHAR_TO_INDEX = {char: idx for idx, char in enumerate(CHAR_SET)}

    for word in words:
        if len(word) == 11:
            is_valid = True  # Track if the word stays clean

            for letter in word:
                if letter not in CHAR_TO_INDEX:
                    is_valid = False  # Found a bad character
                    break  # Stop checking this word immediately

            if is_valid:
                print(word)  # Only prints once, and only if all letters passed


if __name__ == "__main__":
    main()

