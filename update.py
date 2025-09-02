#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from urllib.parse import quote

EXCLUDE_DIRS = ['.git', 'docs', '.vscode', '.circleci', 'site']
README_MD = ['README.md', 'readme.md', 'index.md']

TXT_EXTS = ['md', 'txt']
TXT_URL_PREFIX = 'https://github.com/whm-billiards/whm-billiards.github.io/blob/master/'
BIN_URL_PREFIX = 'https://github.com/whm-billiards/whm-billiards.github.io/raw/master/'


def list_files(course: str):
    filelist_texts = '## 文件及下载列表\n\n'
    readme_path = ''
    for root, dirs, files in os.walk(course):
        files.sort()
        level = root.replace(course, '').count(os.sep)
        indent = ' ' * 4 * level
        filelist_texts += '{}- {}\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in README_MD:
                if f.split('.')[-1] in TXT_EXTS:
                    filelist_texts += '{}- [{}]({})\n'.format(subindent,
                                                              f, TXT_URL_PREFIX + quote('{}/{}'.format(root, f)))
                else:
                    filelist_texts += '{}- [{}]({})\n'.format(subindent,
                                                              f, BIN_URL_PREFIX + quote('{}/{}'.format(root, f)))
            elif root == course and readme_path == '':
                readme_path = '{}/{}'.format(root, f)
    return filelist_texts, readme_path


def generate_md(course: str, filelist_texts: str, readme_path: str):
    final_texts = ['\n\n', filelist_texts]
    if readme_path:
        with open(readme_path, 'r') as file:
            final_texts = file.readlines() + final_texts
    with open('docs/{}.md'.format(course), 'w') as file:
        file.writelines(final_texts)


if __name__ == '__main__':
    with open('docs/README.md', 'r') as file:
        mainreadme_lines = file.readlines()

    with open('docs/index.md', 'w') as file:
        file.writelines(mainreadme_lines)