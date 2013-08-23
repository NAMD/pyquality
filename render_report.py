#!/usr/bin/env python
# coding: utf-8

import csv
import dateutil.parser
import glob
import os

from jinja2 import Template


def get_project_variables(project_path):
    ''' Given a project name, return a dict with its variables '''
    variables = {}
    project_name = os.path.basename(project_path)
    variables['project_name'] = project_name

    tags_name = os.path.join(project_path, '{}-tags.csv'.format(project_name))
    with open(tags_name) as fp:
        tags_data = list(csv.reader(fp))
    headers = tags_data[0]
    name_index = headers.index('tag_name')
    date_index = headers.index('date')
    tags = [{'date': row[date_index], 'name': row[name_index],
             'graph_filename': '{}-{}.png'.format(project_name, row[name_index])}
            for row in tags_data[1:]]
    tags.sort(key=lambda x: x['date'], reverse=True)
    variables['tags'] = tags

    ratio_filename = os.path.join(project_path,
            '{}-pep8-{}.csv'.format(project_name, tags[0]['name']))
    with open(ratio_filename) as fp:
        file_ratio_data = list(csv.reader(fp))
    headers = file_ratio_data[0]
    ratios = file_ratio_data[1:]
    ratios.sort(key=lambda x: x[headers.index('ratio')])
    ratios = [dict(zip(headers, row)) for row in ratios]
    variables['best_files_tag'] = tag[0]['name']
    variables['worst_files_tag'] = tag[0]['name']
    variables['best_files'] = ratios[:10]
    variables['worst_files'] = ratios[-10:]
    variables['ratios'] = ratios
    variables['video_filename'] = '{}-history.ogv'.format(project_name)

    return variables


def render_report(template_filename, variables):
    with open(template_filename, 'r') as fp:
        template = Template(fp.read())
    return template.render(**variables)


def main():
    template_filename = 'report-template.markdown'
    for project_path in glob.glob('results/*'):
        print('Rendering report for {}...'.format(project_path))
        project_name = os.path.split(project_path)[-1]
        project_variables = get_project_variables(project_path)
        result = render_report(template_filename, project_variables)
        report_filename = os.path.join(project_path,
                project_name + '-report.markdown')
        with open(report_filename, 'w') as fp:
            fp.write(result)


if __name__ == '__main__':
    main()
