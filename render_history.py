#!/usr/bin/env python
# coding: utf-8

import glob
import os

from strobo import SlideShow
import dateutil.parser


def get_image_names(directory):
    metadata_files = glob.glob(os.path.join(directory, '*.metadata'))
    taglist = []
    for metadata_file in metadata_files:
        with open(metadata_file, 'r') as fp:
            tag_name, tag_date, _, _ = fp.read().strip().split(';')
        tag_date = dateutil.parser.parse(tag_date.replace('"', ''))
        taglist.append((tag_name, tag_date))

    taglist.sort(key=lambda x: x[1])

    project = directory.split(os.path.sep)[-1]
    images = [os.path.join(directory, '{}-{}.png'.format(project, tag[0])) for tag
        in taglist]

    return images


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
