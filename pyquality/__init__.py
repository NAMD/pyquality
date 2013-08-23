# coding: utf-8

'''Rich reports for Python code quality'''

import cli

from .git_utils import *
from .graphs import plot_graphs
from .main import analyse_repository
from .report import render_report
from .template import default_template
from .video import render_project_history
