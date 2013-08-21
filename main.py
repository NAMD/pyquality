# coding Utf-8

import fnmatch
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import flake8.main
import numpy


def git_tag_list(repo_path):
    return subprocess.check_output("git tag -l".split(), cwd=repo_path).splitlines()

def git_checkout(repo_path, rev):
    return subprocess.call(["git", "checkout", rev], cwd=repo_path)

def git_reset_head(repo_path):
    return subprocess.call("git reset --hard".split(), cwd=repo_path)

def git_current_branch(repo_path):
    return subprocess.check_output("git rev-parse --abbrev-ref "
            "HEAD".split(), cwd=repo_path).strip()

def git_count_authors(repo_path):
    return len(subprocess.check_output("git shortlog -s -n".split(),
        cwd=repo_path).splitlines())

def git_count_commits(repo_path):
    return int(subprocess.check_output("git rev-list HEAD --count".split(),
        cwd=repo_path).strip())

def git_last_commit_date(repo_path):
    return subprocess.check_output('git log -1 --format="%ad"'.split(),
        cwd=repo_path).strip()

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
    ratios = {}
    for filename, result in results.items():
        number_of_lines, number_of_lines_with_errors, number_of_pep8_errors = result
        if number_of_lines == 0:
            continue
        ratio = float(number_of_lines_with_errors) / number_of_lines
        ratios[filename] = ratio
    return ratios

def analyse(projects):
    for project in projects:
        print project
        repo_path = os.path.abspath(os.path.join(os.path.curdir, 'repos/',
            project))
        tags = [git_current_branch(repo_path)] + git_tag_list(repo_path)

        results_path = os.path.join('results', project)
        try:
            shutil.rmtree(results_path)
        except OSError:
            pass
        finally:
            os.mkdir(results_path)

        for tag in tags:
            print project, tag
            git_checkout(repo_path, tag)
            git_reset_head(repo_path)
            results = pep8_dir(repo_path)
            if results is None:
                continue
            plot_data = summarize_results(results)
            authors = git_count_authors(repo_path)
            commits = git_count_commits(repo_path)
            commit_date = git_last_commit_date(repo_path)

            base_filename = '{}-{}'.format(os.path.basename(repo_path),
                tag.replace('/','_'))
            base_path = os.path.join(os.path.curdir,
                    'results/{}/{}'.format(project, base_filename))
            results_filename = base_path + '.dat'
            metadata_filename = base_path + '.metadata'
            ratios_filename = base_path + '.ratios'

            with open(results_filename, 'w') as fp:
                for line in plot_data.values():
                    fp.write('{}\n'.format(line))

            with open(metadata_filename, 'w') as fp:
                fp.write('{};{};{};{}'.format(tag, commit_date, authors, commits))

            len_repo_path = len(repo_path) + len(os.path.sep)
            with open(ratios_filename, 'w') as fp:
                for filename, ratio in plot_data.iteritems():
                    relative_filename = filename[len_repo_path:]
                    fp.write('{};{}\n'.format(relative_filename, ratio))

        git_checkout(repo_path, tags[0]) # returns to the branch we found the repo in

if __name__ == '__main__':
    projects = map(lambda x: x.split('/')[1], glob.glob('repos/*'))
    analyse(projects)
