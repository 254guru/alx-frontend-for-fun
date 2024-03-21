#!/usr/bin/python3

import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f'Missing {sys.argv[1]}', file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            for line in read:
                # Replace bold and italic syntax
                line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

                # MD5 conversion
                md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
                for match in md5_matches:
                    line = line.replace(f'[[{match}]]', hashlib.md5(match.encode()).hexdigest())

                # Remove letter 'C'
                line = re.sub(r'\(\((.+?)\)\)', lambda m: ''.join(c for c in m.group(1) if c not in 'Cc'), line)

                # Heading conversion
                if line.startswith('#'):
                    heading_level = min(6, line.count('#'))
                    line = f'<h{heading_level}>{line.strip("#").strip()}</h{heading_level}>\n'

                # List conversion
                if line.startswith('- '):
                    if not html.tell():  # If the HTML file is empty, start an unordered list
                        html.write('<ul>\n')
                    line = f'<li>{line[2:].strip()}</li>\n'

                # Paragraph separation
                elif line.strip():
                    if not html.tell():  # If the HTML file is empty, start a paragraph
                        html.write('<p>\n')
                    line = f'{line.strip()}\n'

                # Write the line to the HTML file
                html.write(line)

            # Close HTML tags
            if html.tell():  # If the HTML file is not empty
                if line.startswith('- '):
                    html.write('</ul>\n')
                elif line.strip():
                    html.write('</p>\n')

    exit(0)
