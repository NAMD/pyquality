# coding Utf-8

import fnmatch
import glob
import os
import sys
import tempfile

import flake8.main
import numpy


def pep8(filename):
    old_stdout = sys.stdout
    temp_file = tempfile.NamedTemporaryFile()
    sys.stdout = temp_file

    with open(filename, 'r') as fp:
        contents = fp.read()
        number_of_lines = contents.count('\n')
    number_of_pep8_errors = flake8.main.check_file(filename)

    temp_file = sys.stdout
    sys.stdout = old_stdout
    temp_file.seek(0)

    line_numbers = set()
    for error in temp_file.readlines():
        line_number = error.split(':')[1]
        line_numbers.add(line_number)
    temp_file.close()

    return number_of_lines, len(line_numbers), number_of_pep8_errors

def pep8_dir(path):
    results = {}
    for root, dirs, files in os.walk(path):
        for file_ in fnmatch.filter(files, '*.py'):
            #TODO: what about python files that don't end in .py?
            full_path = os.path.join(root, file_)
            results[full_path] = pep8(full_path)
    return results

def summarize_results(results):
    ratios = []
    for filename, result in results.items():
        number_of_lines, number_of_lines_with_errors, number_of_pep8_errors = result
        if number_of_lines == 0:
            continue
        ratio = float(number_of_lines_with_errors) / number_of_lines
        ratios.append(ratio)
    return ratios


if __name__ == '__main__':

    projects = map(lambda x: x.split('/')[1], glob.glob('repos/*'))
    for project in projects:
        print project
        new_path = os.path.join('repos/', project)
        plot_data = summarize_results(pep8_dir(new_path))
        base_filename = os.path.basename(new_path)
        with open('results/{}.dat'.format(base_filename), 'w') as fp:
            for line in plot_data:
                fp.write('{}\n'.format(line))
