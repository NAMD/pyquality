#!/usr/bin/env python
# coding: utf-8

import csv
import glob
import os

from strobo import SlideShow
import dateutil.parser


path_join = os.path.join

def get_image_names(project_path):
    project_name = os.path.basename(project_path)
    tags_name = path_join(project_path, '{}-tags.csv'.format(project_name))
    with open(tags_name) as fp:
        tags = list(csv.reader(fp))[1:]
    tags.sort(key=lambda x: x[1])

    images = [path_join(project_path, '{}-{}.png'.format(project_name, row[0]))
              for row in tags]
    return images


def render_project_history(project_path):
    slides = SlideShow(delay=0.075, size=(1600, 900), fade_in=0.05,
            fade_out=0.05)
    slides.add_images(*get_image_names(project_path))
    slides.create_images()
    slides.render(path_join(project_path,
                               os.path.basename(project_path) + '-history'))


def main():
    for project in glob.glob('results/*'):
        print('Rendering video for {}...'.format(project))
        render_project_history(project)


if __name__ == '__main__':
    main()
