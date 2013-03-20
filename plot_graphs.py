import glob
import os
import sys

from matplotlib.pyplot import figure
import numpy

data_files = glob.glob('results/*.dat')
width = 800
height = 600
for data_file in data_files:
    f = figure(figsize=(width / 80, height / 80), dpi=80)
    s = f.add_subplot(1, 1, 1)
    with open(data_file, 'r') as fp:
        plot_data = [float(line.strip()) for line in fp.readlines()]
    if not plot_data:
        sys.stderr.write("File {} had no data.\n".format(data_file))
        continue
    s.hist(plot_data, bins=numpy.arange(0.00, 1.01, 0.05))
    project_name = os.path.basename(data_file).rsplit('.dat')[0]
    f.savefig('results/graphs/{}.png'.format(project_name))
