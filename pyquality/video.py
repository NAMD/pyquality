#!/usr/bin/env python
# coding: utf-8

import csv
import glob
import os

from strobo import SlideShow
import dateutil.parser


path_join = os.path.join

def get_image_names(project_name, graphs_path, tags_filename):
    with open(tags_filename) as fp:
        tags = list(csv.reader(fp))[1:]
    tags.sort(key=lambda x: x[1])

    images = [path_join(graphs_path, '{}-{}.png'.format(project_name, row[0]))
              for row in tags]
    return images


def render_project_history(project_name, video_filename, tags_filename,
                           graphs_path):
    slides = SlideShow(delay=0.075, size=(1600, 900), fade_in=0.05,
                       fade_out=0.05)
    slides.add_images(*get_image_names(project_name, graphs_path,
                                       tags_filename))
    slides.create_images()
    slides.render(video_filename)
