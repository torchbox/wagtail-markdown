import subprocess

from setuptools import find_packages, setup


def get_git_revision_hash():
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"])
    except subprocess.CalledProcessError:
        return "main"
    else:
        return git_hash.decode("ascii").splitlines()[0]


README = "https://github.com/torchbox/wagtail-markdown/blob/{hash}/README.md"
README = README.format(hash=get_git_revision_hash())


INSTALL_REQUIRES = [
    "Markdown>=3.3,<4",
    # note: bleach5 requires bleach[css]. Will make one of the next versions require >= 5
    "bleach>=3.3,<5",
    "Wagtail>=2.15",
]


CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: zlib/libpng License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Framework :: Django",
    "Framework :: Django :: 3.0",
    "Framework :: Django :: 3.1",
    "Framework :: Django :: 3.2",
    "Framework :: Django :: 4.0",
    "Framework :: Django :: 4.0",
    "Framework :: Wagtail",
    "Framework :: Wagtail :: 2",
    "Framework :: Wagtail :: 3",
    "Framework :: Wagtail :: 3",
]


setup(
    name="wagtail-markdown",
    version="0.10.0",
    description="Markdown support for Wagtail",
    long_description="Provides Markdown page field and StreamField block for "
    "Wagtail. More info: {}".format(README),
    author="Felicity Tarnell",
    author_email="hello@torchbox.com",
    maintainer="Dan Braghis",
    maintainer_email="dan.braghis@torchbox.com",
    url="https://github.com/torchbox/wagtail-markdown",
    project_urls={
        "Changelog": "https://github.com/torchbox/wagtail-markdown/blob/main/CHANGELOG.md",
    },
    install_requires=INSTALL_REQUIRES,
    license="zlib",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=CLASSIFIERS,
)
