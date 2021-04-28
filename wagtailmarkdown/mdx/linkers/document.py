# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

try:  # wagtail < 2.0
    from wagtail.wagtaildocs.models import Document
except ImportError:  # wagtail >= 2.0
    from wagtail.documents.models import Document

from markdown.util import etree


class Linker(object):
    def run(self, name, optstr):
        try:
            text = name
            if len(optstr):
                text = optstr[0]

            doc = Document.objects.get(title=name)
            url = doc.url
            a = etree.Element("a")
            a.set("href", url)
            a.text = text
            return a
        except ObjectDoesNotExist:
            return '[document "{}" not found]'.format(name)
        except MultipleObjectsReturned:
            return '[multiple documents "{}" found]'.format(name)
