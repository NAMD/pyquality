import glob
import os
import sys

import matplotlib
matplotlib.use("Agg")

from matplotlib.pyplot import close, figure
import numpy

data_files = glob.glob('results/*/*.dat')
width = 1280
height = 720
DPI = 80
for data_file in data_files:
    results_dir, project, filename = data_file.split('/')
    base_filename = filename.rsplit('.', 1)[0]
    metadata_file = os.path.join(results_dir, project,
        '{}.metadata'.format(base_filename))

    fig = figure(figsize=(width / DPI, height / DPI), dpi=DPI)
    subplot = fig.add_subplot(111)
    with open(data_file, 'r') as fp:
        lines = fp.readlines()
    hist_data = [float(line.strip()) for line in lines]

    with open(metadata_file, 'r') as fp:
        metadata = fp.read().split(';')
        tag_name, date = metadata[:2]
        authors, commits = map(int, metadata[2:])

    if not hist_data:
        sys.stderr.write("File {} had no data.\n".format(data_file))
        continue

    subplot.hist(hist_data, bins=numpy.arange(0.00, 1.01, 0.05))
    subplot.set_ylim(0, 500)
    subplot.set_xlim(0, 1)
    fig.suptitle('{} - {}'.format(project, tag_name), fontsize=32)
    subplot.set_ylabel('# of Files')
    subplot.set_xlabel('Warnings/LOC')

    graphs_dir = 'results/graphs/{}'.format(project)

    if not os.path.exists(graphs_dir):
        os.mkdir(graphs_dir)

    fig.savefig('{}/{}.png'.format(graphs_dir, base_filename))
    close(fig)
