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

from markdown.util import etree

try:
    from wagtail.core.models import Page
except ImportError:
    from wagtail.wagtailcore.models import Page

# TODO: In Waiflike, this only allowed linking to SitePage (the main
# content type).  Should this be configurable?


class Linker(object):
    def run(self, name, optstr):
        try:
            text = name
            if optstr:
                text = optstr[0]

            page = Page.objects.get(title=name)
            url = page.url
            a = etree.Element("a")
            a.set("href", url)
            a.text = text
            return a
        except ObjectDoesNotExist:
            return '[page "{}" not found]'.format(name)
        except MultipleObjectsReturned:
            return '[multiple pages "{}" found]'.format(name)
