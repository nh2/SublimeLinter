# -*- coding: utf-8 -*-
# html.py - sublimelint package for checking html files

# HTML allows unclosed tags, while xmllint's XML warnings are very HTML unspecific.
# This HTML+XML linter implements "stricter" HTML linting.
# It first lints the file as HTML, and then as XML.
# (In this order because xmllint's HTML errors are generally more helpful).

from xmllint_linter import XmllintLinter

CONFIG = {
    'language': 'html',
    'executable': 'xmllint',
    'test_existence_args': '--version',
}

XMLLINT_RUN_ARGS = [
    ['-html', '-noout', '-'],  # First lint as HTML
    ['-noout', '-'],           # then as XML
]

class Linter(XmllintLinter):

    def __init__(self, config):
        super(Linter, self).__init__(config)
        self._run_index = 0

    def get_lint_args(self, view, code, filename):
        return XMLLINT_RUN_ARGS[self._run_index]

    # WARNING: This method is not side-effect-free!
    # This is because SublimeLinter does not allow overriding `lint_args` for `executable_check()` yet,
    # so we work around this by overriding `get_lint_args()`.
    def executable_check(self, view, code, filename):

        # First run with xmllint args for HTML linting
        html_errors = super(Linter, self).executable_check(view, code, filename)

        # Change linting mode: make get_lint_args return XML linting args from now on
        self._run_index += 1

        # Run it again, now wieth args for XML linting
        xml_errors = super(Linter, self).executable_check(view, code, filename)

        # Reset `_run_index` in case `built_in_check()` is called multiple times on this `Linter` object.
        self._run_index = 0

        return html_errors + xml_errors
