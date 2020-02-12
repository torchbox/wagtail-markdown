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
    try:
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
    except subprocess.CalledProcessError:
        return 'master'
    else:
        return git_hash.decode('ascii').splitlines()[0]


README = 'https://github.com/torchbox/wagtail-markdown/blob/{hash}/README.md'
README = README.format(
    hash=get_git_revision_hash()
)


INSTALL_REQUIRES = [
    'Markdown>=2.6,<2.7',
    'bleach>=1.4.2,<2.2',
    'Wagtail>=2.0',
]


TESTING_REQUIRES = [
    'dj_database_url==0.4.2',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django',
    'License :: OSI Approved :: zlib/libpng License',
    'Programming Language :: Python :: 3',
    'Framework :: Wagtail',
]


setup(
    name='wagtail-markdown',
    version='0.6',
    description='Markdown support for Wagtail',
    long_description="Provides Markdown page field and streamfield block for "
                     "Wagtail. More info: {}".format(README),
    author='Felicity Tarnell',
    author_email='felicity@torchbox.com',
    url='https://github.com/torchbox/wagtail-markdown',
    install_requires=INSTALL_REQUIRES,
    license='zlib',
    packages=find_packages(),
    include_package_data=True,
    classifiers=CLASSIFIERS,
    extras_require={'testing': TESTING_REQUIRES},
)
