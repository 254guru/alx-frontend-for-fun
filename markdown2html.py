#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    # Checks that the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    with open(input_file, encoding='utf-8') as read:
        with open(output_file, 'w', encoding='utf-8') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            # bold syntax and paragraph
            for line in read:
                # Handle bold syntax
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
                
                # Handle paragraph syntax
                if line.strip():
                    if not paragraph:
                        html.write('<p>\n')
                        paragraph = True
                    html.write(line)
                elif paragraph:
                    html.write('</p>\n')
                    paragraph = False

                # md5
                md5 = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    for match in md5:
                        line = line.replace(f'[[{match}]]', hashlib.md5(match.encode()).hexdigest())

                # remove the letter C
                remove_c = re.findall(r'\(\((.+?)\)\)', line)
                if remove_c:
                    for match in remove_c:
                        line = line.replace(f'(({match}))', ''.join(c for c in match if c.lower() != 'c'))

                # Check for list syntax
                if line.startswith('- '):
                    if ordered_start:
                        html.write('</ol>\n')
                        ordered_start = False
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    html.write(f'<li>{line[2:].strip()}</li>\n')
                elif line.startswith('* '):
                    if unordered_start:
                        html.write('</ul>\n')
                        unordered_start = False
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    html.write(f'<li>{line[2:].strip()}</li>\n')
                elif line.startswith('#'):
                    html.write(f'<h1>{line.strip("#").strip()}</h1>\n')

            # Close any open tags
            if unordered_start:
                html.write('</ul>\n')
            elif ordered_start:
                html.write('</ol>\n')
            elif paragraph:
                html.write('</p>\n')

if __name__ == '__main__':
    # Test that the number of arguments passed is 2
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
