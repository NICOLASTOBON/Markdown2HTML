#!/usr/bin/python3
""" Markdown to HTML """

import os
import re
import sys
import hashlib


def parse_text_style(string):
    """
    Convert text to <b> or <em> HTML tags
    Args:
        string: Is a text
    Return: HTML tag
    """
    string = string.replace('**', '<b>', 1).replace('**', '</b>', 1)
    string = string.replace('__', '<em>', 1).replace('__', '</em>', 1)

    return string


def parse_text_encode(string):
    """
    Convert text in MD5 code
    Args:
        string: Is a text
    Return: Encrypted text
    """
    md5_str = re.findall(r'\[\[(.+?)\]\]', string)
    if md5_str:
        string = string.replace(
            '[[{}]]'.format(md5_str[0]),
            hashlib.md5(md5_str[0].encode()).hexdigest()
        )

    return string


def parse_text_remove_c(string):
    """
    Remove c character in a string
    Args:
        string: Is a text
    Return: text whitout c character
    """
    text = re.findall(r'\(\((.+?)\)\)', string)
    if text:
        new_line = re.sub(r'[cC]', '', text[0])
        string = string.replace(
            "(({}))".format(text[0]),
            new_line
        )
    return string


def parse_text_heading(string):
    """
    Convert text in heading tag
    Args:
        string: Is a text
    Return: <h#>string</h#> tag
    """
    heading = re.findall(r'(^#{1,6})\s', string)
    heading_exits = False

    if heading:
        idx = len(heading[0])
        string = "<h{}>{}</h{}>\n".format(idx, string[idx + 1:-1], idx)
        heading_exits = True
    return (string, heading_exits)


def main(root, dest):
    """
    parsing to HTML tags
    args:
        root: Is a Readme file
        dest: Is a HTML file
    """
    try:
        with open(root, encoding="utf-8") as r:
            with open(dest, 'w', encoding="utf-8") as w:
                unordered_start, ordered_start, paragraph = False, False, False
                for line in r:
                    line = parse_text_style(line)
                    line = parse_text_encode(line)
                    line = parse_text_remove_c(line)
                    line, heading_exits = parse_text_heading(line)

                    length = len(line)
                    unordered = line.lstrip('-')
                    unordered_count = length - len(unordered)
                    ordered = line.lstrip('*')
                    ordered_count = length - len(ordered)

                    if unordered_count:
                        if not unordered_start:
                            w.write('<ul>\n')
                            unordered_start = True
                        line = '<li>' + unordered.strip() + '</li>\n'
                    if unordered_start and not unordered_count:
                        w.write('</ul>\n')
                        unordered_start = False

                    if ordered_count:
                        if not ordered_start:
                            w.write('<ol>\n')
                            ordered_start = True
                        line = '<li>' + ordered.strip() + '</li>\n'
                    if ordered_start and not ordered_count:
                        w.write('</ol>\n')
                        ordered_start = False

                    if not (heading_exits or unordered_start or ordered_start):
                        if not paragraph and length > 1:
                            w.write('<p>\n')
                            paragraph = True
                        elif length > 1:
                            w.write('<br/>\n')
                        elif paragraph:
                            w.write('</p>\n')
                            paragraph = False
                    if length > 1:
                        w.write(line)

                if unordered_start:
                    w.write('</ul>\n')
                if ordered_start:
                    w.write('</ol>\n')
                if paragraph:
                    w.write('</p>\n')

    except IOError:
        print("Missing {}".format(file_name), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        io = sys.stderr
        print("Usage: ./markdown2html.py README.md README.html", file=io)
        sys.exit(1)
    else:
        file_name = sys.argv[1]
        file_dest = sys.argv[2]

        main(file_name, file_dest)
    exit(0)
