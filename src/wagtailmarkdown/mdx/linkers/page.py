from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from wagtail.core.models import Page

import xml.etree.ElementTree as etree


# TODO: In Waiflike, this only allowed linking to SitePage (the main
# content type).  Should this be configurable?


class Linker(object):
    def run(self, name, optstr):
        try:
            text = name
            if optstr:
                text = optstr[0]

            page = Page.objects.get(title=name)
            url = page.get_url()
            a = etree.Element("a")
            a.set("href", url)
            a.text = text
            return a
        except ObjectDoesNotExist:
            return '[page "{}" not found]'.format(name)
        except MultipleObjectsReturned:
            return '[multiple pages "{}" found]'.format(name)
