#!/usr/bin/python3
'''
A script that codes markdown to HTML
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
        for line in file_1:
            if line.startswith('- '):
                if not in_unordered_list:
                    if in_ordered_list:
                        html_content.append('</ol>\n')
                        in_ordered_list = False
                    html_content.append('<ul>\n')
                    in_unordered_list = True
                html_content.append(f'<li>{line[2:]}</li>\n')
            elif line.startswith('* '):
                if not in_ordered_list:
                    if in_unordered_list:
                        html_content.append('</ul>\n')
                        in_unordered_list = False
                    html_content.append('<ol>\n')
                    in_ordered_list = True
                html_content.append(f'<li>{line[2:]}</li>\n')
            else:
                if in_unordered_list:
                    html_content.append('</ul>\n')
                    in_unordered_list = False
                if in_ordered_list:
                    html_content.append('</ol>\n')
                    in_ordered_list = False
                heading = re.split(r'#{1,6} ', line)
                if len(heading) > 1:
                    # Compute the number of the # present to
                    # determine heading level
                    h_level = len(line[:line.find(heading[1])-1])
                    # Append the html equivalent of the heading
                    html_content.append(
                        f'<h{h_level}>{heading[1]}</h{h_level}>\n'
                    )
                else:
                    html_content.append(line)

        if in_unordered_list:
            html_content.append('</ul>\n')
        elif in_ordered_list:
            html_content.append('</ol>\n')

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
