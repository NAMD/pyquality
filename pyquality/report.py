#!/usr/bin/env python
# coding: utf-8

import csv
import dateutil.parser
import glob
import os

from jinja2 import Template


def get_project_variables(project_name, tags_filename, ratios_filename,
                          video_filename):
    ''' Given some project info, return a dict with its variables '''
    variables = {}
    variables['project_name'] = project_name

    with open(tags_filename) as fp:
        tags_data = list(csv.reader(fp))
    headers = tags_data[0]
    name_index = headers.index('tag_name')
    date_index = headers.index('date')
    tags = [{'date': row[date_index], 'name': row[name_index],
             'graph_filename': '{}-{}.png'.format(project_name, row[name_index])}
            for row in tags_data[1:]]
    tags.sort(key=lambda x: x['date'], reverse=True)
    variables['tags'] = tags

    with open(ratios_filename.format(tags[0]['name'])) as fp:
        file_ratio_data = list(csv.reader(fp))
    headers = file_ratio_data[0]
    ratios = file_ratio_data[1:]
    ratios.sort(key=lambda x: x[headers.index('ratio')])
    ratios = [dict(zip(headers, row)) for row in ratios]
    variables['best_files_tag'] = tags[0]['name']
    variables['worst_files_tag'] = tags[0]['name']
    variables['best_files'] = ratios[:10]
    variables['worst_files'] = reversed(ratios[-10:])
    variables['ratios'] = ratios
    variables['video_filename'] = os.path.basename(video_filename)

    return variables


def render_report(project_name, tags_filename, ratios_filename, video_filename,
                  template, report_filename):
    variables = get_project_variables(project_name, tags_filename,
                                      ratios_filename, video_filename)
    template = Template(template)
    result = template.render(**variables)
    with open(report_filename, 'w') as fp:
        fp.write(result)
