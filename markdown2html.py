#!/usr/bin/python3
import sys
import os
import markdown


def convert_markdown_to_html(markdown_file, output_file):
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Parse headings and replace with HTML equivalent
    html_content = parse_headings(html_content)
    # Parse unordered lists and replace with HTML equivalent
    html_content = parse_unordered_lists(html_content)

    with open(output_file, 'w') as f:
        f.write(html_content)


def parse_headings(html_content):
    # Define the heading levels and their HTML equivalents
    heading_tags = {
        '# ': '<h1>',
        '## ': '<h2>',
        '### ': '<h3>',
        '#### ': '<h4>',
        '##### ': '<h5>',
        '###### ': '<h6>'
    }

    # Replace Markdown headings with HTML headings
    for markdown_heading, html_heading in heading_tags.items():
        html_content = html_content.replace(
                markdown_heading, html_heading).replace('\n', '') + '</h1>'

    return html_content


def parse_unordered_lists(html_content):
    # Replace Markdown unordered lists with HTML unordered lists
    html_content = html_content.replace('\n<ul>', '<ul>').replace(
            '<ul>', '\n<ul>\n').replace('</ul>', '\n</ul>\n')
    html_content = html_content.replace('<li>', '\n\t<li>').replace(
            '</li>', '</li>\n')
    return html_content
