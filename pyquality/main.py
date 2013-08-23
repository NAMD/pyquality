# coding Utf-8

import csv
import dateutil.parser
import fnmatch
import glob
import os
import shutil
import sys
import tempfile

import flake8.main

from .git_utils import *


def pep8(filename):
    old_stdout = sys.stdout
    temp_file = tempfile.NamedTemporaryFile()
    sys.stdout = temp_file

    with open(filename, 'r') as fp:
        contents = fp.read()
        number_of_lines = contents.count('\n')

    try:
        number_of_pep8_errors = flake8.main.check_file(filename)

        temp_file.seek(0)

        line_numbers = set()
        errors = temp_file.readlines()
        for error in errors:
            line_number = error.split(':')[1]
            line_numbers.add(line_number)

    except Exception as exc:
        return exc

    finally:
        sys.stdout = old_stdout
        temp_file.close()

    return number_of_lines, len(line_numbers), number_of_pep8_errors


def pep8_dir(path):
    results = {}
    for root, dirs, files in os.walk(path):
        for file_ in fnmatch.filter(files, '*.py'):
            #TODO: what about python files that don't end in .py?
            full_path = os.path.join(root, file_)
            result = pep8(full_path)

            if isinstance(result, Exception):
                import traceback
                sys.stderr.write("Error while running flake8 for '{}'.\n".format(
                    full_path))
                sys.stderr.write("\t{}: {}\n".format(result.__class__.__name__,
                    result.message))
                return None

            results[full_path] = result
    return results


def summarize_results(results):
    data = {}
    for filename, result in results.items():
        number_of_lines, number_of_lines_with_errors, number_of_pep8_errors = result
        if number_of_lines == 0:
            continue
        lines_ok = number_of_lines - number_of_lines_with_errors
        data[filename] = {'total_lines': number_of_lines,
                          'lines_with_errors': number_of_lines_with_errors,
                          'lines_without_errors': lines_ok}
    return data

def analyse_repository(repository_path, tags_filename, ratios_filename):
    tags = [git_current_branch(repository_path)] + git_tag_list(repository_path)

    tags_info_csv = csv.writer(open(tags_filename, 'w'))
    tags_info_csv.writerow(('tag_name', 'date', 'authors', 'commits'))
    for tag in tags:
        git_checkout(repository_path, tag)
        git_reset_head(repository_path)
        results = pep8_dir(repository_path)
        if results is None:
            continue
        line_data = summarize_results(results)
        authors = git_count_authors(repository_path)
        commits = git_count_commits(repository_path)
        commit_date = dateutil.parser.parse(git_last_commit_date(repository_path))

        tags_info_csv.writerow((tag, commit_date, authors, commits))

        tag_name = tag.replace('/', '_')
        headers = ('filename', 'total_lines', 'lines_with_errors',
                   'lines_without_errors', 'ratio')
        with open(ratios_filename.format(tag), 'w') as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerow(headers)
            for filename, data in line_data.items():
                total = data['total_lines']
                errors = data['lines_with_errors']
                ok = data['lines_without_errors']
                try:
                    ratio = float(errors) / total
                except ZeroDivisionError:
                    ratio = 0
                filename = filename[len(repository_path) + len(os.path.sep):]
                row = (filename, total, errors,
                       data['lines_without_errors'], ratio)
                csv_writer.writerow(row)

    git_checkout(repository_path, tags[0]) # returns to the branch we found the repo in
