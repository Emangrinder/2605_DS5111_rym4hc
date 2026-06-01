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

import sys

def main():
    input_text = sys.stdin.read()
    words = input_text.split()

    valids = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    print(f"Processed {len(words)} words.")
    for word in words:
        if len(word) == n word:
            for letter in wor in valids:
                if letter not in valid:
                    continue
        print(word)


if __name__ == "__main__":
    main()

