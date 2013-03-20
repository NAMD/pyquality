# coding Utf-8

import fnmatch
import glob
import os
import sys
import tempfile
from multiprocessing import Pool

import flake8.main
import numpy


def pep8(filename):
    old_stdout = sys.stdout
    temp_file = tempfile.NamedTemporaryFile()
    sys.stdout = temp_file

    with open(filename, 'r') as fp:
        contents = fp.read()
        number_of_lines = contents.count('\n')
    try:
        number_of_pep8_errors = flake8.main.check_file(filename)
    except Exception as exc:
        return exc

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
            result = Pool(1).apply(pep8, (full_path, ))

            if isinstance(result, Exception):
                import traceback
                sys.stderr.write("Error while running flake8 for '{}'.\n".format(
                    project))
                sys.stderr.write("\t{}: {}\n".format(result.__class__.__name__,
                    result.message))
                return None

            results[full_path] = result
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
        results = pep8_dir(new_path)
        if results is None:
            continue
        plot_data = summarize_results(results)

        base_filename = os.path.basename(new_path)
        with open('results/{}.dat'.format(base_filename), 'w') as fp:
            for line in plot_data:
                fp.write('{}\n'.format(line))
