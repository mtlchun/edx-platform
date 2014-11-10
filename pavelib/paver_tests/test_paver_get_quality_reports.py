import os
import tempfile
import unittest
from mock import patch, Mock
from ddt import ddt, file_data

import pavelib.quality
import paver.easy
from paver.easy import BuildFailure



class TestGetReportFiles(unittest.TestCase):
    """
    Ensure only the report files we want are returned as part of run_quality.
    """

    @patch('os.walk')
    def test_get_pylint_reports(self, my_mock):

        my_mock.return_value = iter([
            ('/foo', ('',), ('pylint.report',)),
            ('/bar', ('/baz',), ('pylint.report',))
        ])
        reports = pavelib.quality.get_violations_reports("pylint")
        self.assertEqual(len(reports), 2)

    @patch('os.walk')
    def test_get_pep8_reports(self, my_mock):
        my_mock.return_value = iter([
            ('/foo', ('',), ('pep8.report',)),
            ('/bar', ('/baz',), ('pep8.report',))
        ])
        reports = pavelib.quality.get_violations_reports("pep8")
        self.assertEqual(len(reports), 2)

    @patch('os.walk')
    def test_get_pep8_reports_noisy(self, my_mock):
        """ Several conditions: different report types, different files, multiple files """
        my_mock.return_value = iter([
            ('/foo', ('',), ('pep8.report',)),
            ('/fooz', ('/ball',), ('pylint.report',)),
            ('/fooz', ('/ball',), ('non.report',)),
            ('/fooz', ('/ball',), ('lms.xml',)),
            ('/bar', ('/baz',), ('pep8.report',))
        ])
        reports = pavelib.quality.get_violations_reports("pep8")
        self.assertEqual(len(reports), 2)