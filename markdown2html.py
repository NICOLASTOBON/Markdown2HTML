#!/usr/bin/python3
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)
    elif not os.path.exists(sys.argv[1]):
        print(f"Missing {sys.argv[1]}")
        sys.exit(1)
    else:
        sys.exit(0)
