#!/usr/bin/python3
import sys
import os
import markdown


def convert_markdown_to_html(markdown_file, output_file):
    """
    convert to makdown to html format
    """
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Parse headings and replace with HTML equivalent
    html_content = parse_headings(html_content)

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


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <markdown_file> <output_file>",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, output_file)

    sys.exit(0)
