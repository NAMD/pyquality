# coding: utf-8

import glob
import os
import tempfile
import unittest

from re import compile as regexp_compile
from shlex import split as shlex_split
from shutil import rmtree
from subprocess import Popen, PIPE
from textwrap import dedent

import pyquality


def execute(command):
    process = Popen(shlex_split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.wait()
    return process


class GenerateCSVTestCase(unittest.TestCase):
    # TODO: test only a directory (without history)

    def setUp(self):
        self.original_pwd = os.getcwd()
        self.temp_path = tempfile.mkdtemp()
        os.chdir(self.temp_path)

    def tearDown(self):
        rmtree(self.temp_path)
        os.chdir(self.original_pwd)

    def assert_file_contents(self, regexp_str, filename):
        regexp_str = (dedent(regexp_str).strip() + '\n').replace('\n', '\r\n')
        regexp = regexp_compile(regexp_str)
        with open(filename) as fp:
            file_contents = fp.read()

        self.assertEqual(regexp.findall(file_contents), [file_contents])

    def test_simple_repository(self):
        repository_path = os.path.join(self.temp_path, 'git_repo')
        script_path = os.path.join(self.original_pwd,
                                   'tests/test_1_file_2_tags.sh')

        execute('bash {} {}'.format(script_path, repository_path))
        tags = ['0.1.0', '0.1.1', 'master']

        results_path = os.path.join(self.temp_path, 'results')
        os.mkdir(results_path)
        tags_filename = os.path.join(results_path, 'git_repo-tags.csv')
        ratios_filename = os.path.join(results_path, 'git_repo-pep8-{}.csv')
        pyquality.analyse_repository(repository_path, tags_filename,
                                     ratios_filename)

        filenames = glob.glob(os.path.join(results_path, '*'))
        filenames = set([os.path.basename(filename) for filename in filenames])
        expected_filenames = set([tags_filename] +
                                 [ratios_filename.format(tag) for tag in tags])
        expected_filenames = set([os.path.basename(filename)
                                  for filename in expected_filenames])

        self.assertEqual(filenames, expected_filenames)

        expected_tagfile = '''
        tag_name,date,authors,commits
        master,....-..-.. ..:..:..-..:..,1,4
        0.1.0,....-..-.. ..:..:..-..:..,1,1
        0.1.1,....-..-.. ..:..:..-..:..,1,3
        '''
        self.assert_file_contents(expected_tagfile, tags_filename)

        expected_tag_010 = '''
        filename,total_lines,lines_with_errors,lines_without_errors,ratio
        first_file.py,3,2,1,0.6666666666666666
        '''
        self.assert_file_contents(expected_tag_010,
                                  ratios_filename.format('0.1.0'))


        expected_tag_011 = '''
        filename,total_lines,lines_with_errors,lines_without_errors,ratio
        first_file.py,5,3,2,0.6
        '''
        self.assert_file_contents(expected_tag_011,
                                  ratios_filename.format('0.1.1'))

        expected_tag_master = '''
        filename,total_lines,lines_with_errors,lines_without_errors,ratio
        first_file.py,6,3,3,0.5
        '''
        self.assert_file_contents(expected_tag_master,
                                  ratios_filename.format('master'))

