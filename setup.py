from setuptools import setup, find_packages
import re
import ast

# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('q2_plotly/__init__.py', 'rb') as f:
    hit = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(hit))

setup(
    name="q2-plotly",
    version=version,
    packages=find_packages(),
    # Dependencies go in here
    # plotly needs to be >1.12 for offline, >1.12.9 for native drop-down menus
    install_requires=['qiime >= 2.0.6', 'pandas', 'q2templates >= 0.0.6',
                      'plotly >= 1.12.9'],
    author="Michael Hall",
    author_email="mike.hall@dal.ca",
    description="Visualizations of QIIME2 artifacts using the Plotly library.",
    entry_points={
        "qiime.plugins":
        ["q2-plotly=q2_plotly.plugin_setup:plugin"]
    },
    # If you are creating a visualizer, all template assets must be included in
    # the package source, if you are not using q2templates this can be removed
    package_data={
        "q2_plotly": ["assets/index.html"]
    }
)
