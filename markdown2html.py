#!/usr/bin/python3
'''
A script that converts Markdown to HTML
'''
import sys
import os
import re

def convert_markdown_to_html(input_file, output_file):
    # Checks that the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    with open(input_file, encoding='utf-8') as file_1:
        html_content = []
        in_unordered_list = False
        in_ordered_list = False
        in_paragraph = False
        for line in file_1:
            # Handle bold syntax
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            # Check for list items
            if line.startswith('- '):
                # Close ordered list if necessary
                if in_ordered_list:
                    html_content.append('</ol>\n')
                    in_ordered_list = False
                # Open unordered list if not already open
                if not in_unordered_list:
                    html_content.append('<ul>\n')
                    in_unordered_list = True
                # Close paragraph if necessary
                if in_paragraph:
                    html_content.append('</p>\n')
                    in_paragraph = False
                html_content.append(f'<li>{line[2:].strip()}</li>\n')
            elif line.startswith('* '):
                # Close unordered list if necessary
                if in_unordered_list:
                    html_content.append('</ul>\n')
                    in_unordered_list = False
                # Open ordered list if not already open
                if not in_ordered_list:
                    html_content.append('<ol>\n')
                    in_ordered_list = True
                # Close paragraph if necessary
                if in_paragraph:
                    html_content.append('</p>\n')
                    in_paragraph = False
                html_content.append(f'<li>{line[2:].strip()}</li>\n')
            else:
                # Close list if necessary
                if in_unordered_list:
                    html_content.append('</ul>\n')
                    in_unordered_list = False
                elif in_ordered_list:
                    html_content.append('</ol>\n')
                    in_ordered_list = False
                # Check for heading
                heading_match = re.match(r'(#{1,6}) (.*)', line)
                if heading_match:
                    h_level = len(heading_match.group(1))
                    html_content.append(f'<h{h_level}>{heading_match.group(2).strip()}</h{h_level}>\n')
                else:
                    # Check for paragraph
                    if not in_paragraph and line.strip():
                        html_content.append('<p>\n')
                        in_paragraph = True
                    elif in_paragraph and not line.strip():
                        html_content.append('</p>\n')
                        in_paragraph = False
                    html_content.append(line)
        
        # Close any open tags
        if in_unordered_list:
            html_content.append('</ul>\n')
        elif in_ordered_list:
            html_content.append('</ol>\n')
        elif in_paragraph:
            html_content.append('</p>\n')

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)

if __name__ == '__main__':
    # Test that the number of arguments passed is 2
    if len(sys.argv[1:]) != 2:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
