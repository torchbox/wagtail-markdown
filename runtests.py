#!/usr/bin/env python

import os
import sys

from django.core.management import execute_from_command_line

os.environ["DJANGO_SETTINGS_MODULE"] = "wagtailmarkdown.tests.settings"


def runtests():
    execute_from_command_line([sys.argv[0], "check"])
    execute_from_command_line([sys.argv[0], "makemigrations", "--no-input", "--check"])
    execute_from_command_line([sys.argv[0], "test"] + sys.argv[1:])


if __name__ == "__main__":
    runtests()
