#!/usr/bin/env python
# coding: utf-8

import glob
import os

from strobo import SlideShow


def get_image_names(directory):
    images = glob.glob(os.path.join(directory, '*.png'))
    return sorted(images)


def render_project_history(project_name):
    slides = SlideShow(delay=0.075, size=(1600, 900), fade_in=0.05,
            fade_out=0.05)
    slides.add_images(*get_image_names(project_name))
    slides.create_images()
    slides.render(os.path.join(project_name,
                               os.path.basename(project_name) + '-history'))


def main():
    for project in glob.glob('results/*'):
        print('Rendering video for {}...'.format(project))
        render_project_history(project)


if __name__ == '__main__':
    main()
