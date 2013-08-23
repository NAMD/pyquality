# coding: utf-8

import subprocess

import requests


def git_clone(repository_url, path_to_save):
    ''' Clone a Git repository using `git` binary '''
    subprocess.call(['git', 'clone', repository_url, path_to_save])


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
            cwd=repo_path).strip()[1:-1]


def github_list_repositories(page, query='language:python', sort='stars'):
    # We're using the legacy search api
    # (http://developer.github.com/v3/search/legacy/), maybe we should use the
    # preview of the new api
    # (http://developer.github.com/changes/2013-07-19-preview-the-new-search-api/
    # https://gist.github.com/jasonrudolph/6065289)
    search_url = "https://api.github.com/legacy/repos/search/{}"
    params['start_page'] = page
    response = requests.get(search_url.format(query), params=params)

    projects = []
    for repo in response.json()['repositories']:
        project_name = repo["name"]
        project_url = repo["url"]
        projects.append({'name': project_name, 'url': project_url})

    return projects
