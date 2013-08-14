# coding Utf-8

import fnmatch
import glob
import os
import sys
import tempfile
from multiprocessing import Pool
import subprocess

import flake8.main
import numpy

def git_tag_list(repo_path):
    return subprocess.check_output("git tag -l".split(), cwd=repo_path).splitlines()

def git_checkout(repo_path, rev):
    return subprocess.call(["git", "checkout", rev], cwd=repo_path)

def git_reset_head(repo_path):
    return subprocess.call("git reset --hard".split(), cwd=repo_path)


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
    process_pool = Pool(1)
    for root, dirs, files in os.walk(path):
        for file_ in fnmatch.filter(files, '*.py'):
            #TODO: what about python files that don't end in .py?
            full_path = os.path.join(root, file_)
            result = process_pool.apply(pep8, (full_path, ))

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

def analyse(projects):
    for project in projects:
        print project
        repo_path = os.path.abspath(os.path.join(os.path.curdir, 'repos/',
            project))
        tags = git_tag_list(repo_path)
        for tag in tags:
            print project, tag
            git_checkout(repo_path, tag)
            git_reset_head(repo_path)
            results = pep8_dir(repo_path)
            if results is None:
                continue
            plot_data = summarize_results(results)

            base_filename = '{}-{}'.format(os.path.basename(repo_path),
                tag)
            results_filename = os.path.join(base_dir,
                'results/{}.dat'.format(base_filename))
            with open(results_filename, 'w') as fp:
                for line in plot_data:
                    fp.write('{}\n'.format(line))

if __name__ == '__main__':
    projects = map(lambda x: x.split('/')[1], glob.glob('repos/*'))
    analyse(projects)
