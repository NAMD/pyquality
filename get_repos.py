import requests
import pprint
import subprocess
import os

# We're using the legacy search api
# (http://developer.github.com/v3/search/legacy/), maybe we should use the
# preview of the new api
# (http://developer.github.com/changes/2013-07-19-preview-the-new-search-api/
# https://gist.github.com/jasonrudolph/6065289)
search_url = "https://api.github.com/legacy/repos/search/{}"

query = "language:python"

params = {"sort": "stars"}


projects = []
# Each page returns 100 results. I don't think we need more than this for now,
# but I'll leave the code ready to download more than that.
for page in range(1, 2):
    print("getting page {}".format(page))
    params['start_page'] = page
    response = requests.get(search_url.format(query), params=params)

    for repo in response.json()['repositories']:
        project_name = repo["name"]
        project_url = repo["url"]
        projects.append((project_name, project_url))

pprint.pprint(projects)
print(len(projects))

for project, project_url in projects:
    directory = os.path.join("repos", project)
    subprocess.call(['git', 'clone', project_url, directory])
