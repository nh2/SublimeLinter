# -*- coding: utf-8 -*-
# xml.py - sublimelint package for checking html files

from xmllint_linter import XmllintLinter

CONFIG = {
    'language': 'xml',
    'executable': 'xmllint',
    'lint_args': ['-noout', '-'],
    'test_existence_args': '--version',
}


class Linter(XmllintLinter):
  pass
