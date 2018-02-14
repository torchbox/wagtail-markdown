#! /usr/bin/env/python
# vim:sw=4 ts=4 et:
#
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#

from setuptools import setup, find_packages
import subprocess


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


README = 'https://github.com/torchbox/wagtail-markdown/blob/{hash}/README.md'
README = README.format(
    hash=get_git_revision_hash()
)


setup(
    name='wagtail-markdown',
    version='0.5a1',
    description='Markdown support for Wagtail',
    long_description="Provides Markdown page field and streamfield block for "
                     "Wagtail. More info: {}".format(README),
    author='Felicity Tarnell',
    author_email='felicity@torchbox.com',
    url='https://github.com/torchbox/wagtail-markdown',
    install_requires=[
        'Markdown>=2.6,<2.7',
        'bleach>=1.4.2,<2.2',
    ],
    license='zlib',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: zlib/libpng License',
        'Programming Language :: Python :: 3',
    ],
)
