#!/usr/bin/env python
# coding: utf-8

import csv
import dateutil.parser
import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")

from matplotlib.pyplot import close, figure, xkcd
import numpy

xkcd()

def main():
    projects = glob.glob(os.path.join('results', '*'))
    width = 1280
    height = 720
    DPI = 80
    for project in projects:
        project_name = os.path.basename(project)
        tags_name = os.path.join(project, '{}-tags.csv'.format(project_name))
        with open(tags_name) as fp:
            tags = list(csv.reader(fp))[1:]

        for tag_name, date, authors, commits in tags:
            fig = figure(figsize=(width / DPI, height / DPI), dpi=DPI)

            ratios_filename = os.path.join(project,
                    '{}-pep8-{}.csv'.format(project_name, tag_name))
            with open(ratios_filename, 'r') as fp:
                ratio_data = list(csv.reader(fp))
                headers = ratio_data[0]
                ratio_index = headers.index('ratio')
                ratios = [float(row[ratio_index]) for row in ratio_data[1:]]
            if not ratios:
                sys.stderr.write("File {} had no data.\n".format(data_file))
                continue

            subplot = fig.add_subplot(111)
            subplot.hist(ratios, bins=numpy.arange(0.00, 1.01, 0.05))
            subplot.set_ylim(0, 500)
            subplot.set_xlim(0, 1)
            title = '{} - {} ({})'.format(project_name, tag_name,
                    date.split(' ')[0])
            authors_commits = "{:06d} authors\n{:06d} commits"\
                    .format(int(authors), int(commits))
            fig.suptitle(title, fontsize=32)
            fig.text(0.6, 0.7, authors_commits, fontsize=24,
                     bbox={'boxstyle': 'round', 'facecolor': 'white'})
            subplot.set_ylabel('# of Files', fontsize=24)
            subplot.set_xlabel('Warnings/LOC', fontsize=24)

            graph_filename = os.path.join(project,
                    '{}-{}.png'.format(project_name, tag_name))
            fig.savefig(graph_filename)
            close(fig)


if __name__ == '__main__':
    main()
