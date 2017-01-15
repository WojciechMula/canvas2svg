# -*- coding: utf-8 -*-
from distutils.core import setup

def get_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name                = 'canvasvg',
    version             = '1.0.3',
    description         = "Save Tkinter Canvas in SVG file",
    author              = "Wojciech Muła",
    author_email        = "wojciech_mula@poczta.onet.pl",
    maintainer          = "Wojciech Muła",
    maintainer_email    = "wojciech_mula@poczta.onet.pl",
    url                 = "http://github.com/WojciechMula/canvas2svg",
    license             = "BSD (3 clauses)",
    long_description    = get_readme(),
    packages            = ['canvasvg'],
    package_dir         = {'canvasvg': ''},
    keywords            = [
        "tkinter",
        "tk",
        "canvas",
        "svg",
        "screenshot",
    ],
    classifiers         = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
)
