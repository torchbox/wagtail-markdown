# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#

import re

from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist

from wagtail import wagtaildocs

import markdown
from markdown.util import AtomicString
from markdown.util import etree

class Linker:
    def run(self, name, optstr):
        try:
            text = name
            if len(optstr):
                text = optstr[0]

            doc = wagtaildocs.models.Document.objects.get(title = name)
            url = doc.url
            a = etree.Element('a')
            a.set('href', url)
            a.text = text
            return a;
        except ObjectDoesNotExist:
            return '[document %s not found]' % (name,)
