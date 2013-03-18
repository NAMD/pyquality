import requests
from bs4 import BeautifulSoup
import pprint
import subprocess
import os
#search_url = "https://api.github.com/legacy/repos/search/language:python"
#
#response = requests.get(search_url)
#for repo in response.json()['repositories']:
#    print(repo['owner'], repo['name'])

projects = []

most_watched_url = "https://github.com/languages/Python/most_watched?page={}"
for page in range(1, 6):
    print("getting page {}".format(page))
    response = requests.get(most_watched_url.format(page))

    soup = BeautifulSoup(response.content)
    for project in soup.find_all('h3'):
        project_name = project.a.text
        project_url = project.a.attrs['href']
        projects.append((project_name, project_url))


pprint.pprint(projects)
print(len(projects))

base_repo_url = "https://github.com"
for project, project_url in projects:
    url = base_repo_url + project_url
    directory = os.path.join("repos", project)
    subprocess.call(['git', 'clone', url, directory])
