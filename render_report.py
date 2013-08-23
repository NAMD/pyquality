#!/usr/bin/env python
# coding: utf-8

import datetime
import glob
import os

from jinja2 import Template


def convert_date(date_as_string):
    date_format = '%a %b %d %H:%M:%S %Y'
    base_time = datetime.datetime.strptime(date_as_string[1:-7], date_format)
    signal = date_as_string[-6:-5]
    hours = int(date_as_string[-5:-3])
    minutes = int(date_as_string[-3:-1])
    delta = datetime.timedelta((hours * 3600 + minutes * 60) / (24.0 * 3600))
    if signal == '+':
        delta = - delta
    return base_time + delta


def get_project_variables(project_path):
    ''' Given a project name, return a dict with its variables '''
    variables = {}
    project_name = os.path.split(project_path)[-1]
    variables['project_name'] = project_name

    tags = []
    for filename in glob.glob(os.path.join(project_path, '*.metadata')):
        with open(filename) as fp:
            data = fp.read().split(';')
        graph_filename = '{}-{}.png'.format(project_name, data[0])
        tags.append({'name': data[0], 'date': convert_date(data[1]),
                     'graph_filename': graph_filename})
    tags.sort(lambda a, b: cmp(b['date'], a['date']))
    variables['tags'] = tags

    variables['best_files'] = ({'filename': 'test', 'ratio': 3.14}) # TODO
    variables['worst_files'] = ({'filename': 'test', 'ratio': 3.14}) # TODO

    #TODO: number of lines (ok/error/total)
    #TODO: total table

    variables['video_filename'] = '{}-history.ogv'.format(project_name)

    return variables


def render_report(template_filename, variables):
    with open(template_filename, 'r') as fp:
        template = Template(fp.read())
    return template.render(**variables)


def main():
    template_filename = 'report-template.html'
    for project_path in glob.glob('results/*'):
        print('Rendering report for {}...'.format(project_path))
        project_name = os.path.split(project_path)[-1]
        project_variables = get_project_variables(project_path)
        result = render_report(template_filename, project_variables)
        report_filename = os.path.join(project_path,
                project_name + '-report.html')
        with open(report_filename, 'w') as fp:
            fp.write(result)


if __name__ == '__main__':
    main()
