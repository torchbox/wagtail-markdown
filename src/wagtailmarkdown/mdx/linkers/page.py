import xml.etree.ElementTree as etree

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from wagtail.models import Page


class Linker:
    def run(self, name, options):
        try:
            text = name
            if options:
                text = options[0]

            a = etree.Element("a")
            a.set("href", Page.objects.get(title=name).get_url())
            a.text = text
            return a
        except ObjectDoesNotExist:
            return f'[page "{name}" not found]'
        except MultipleObjectsReturned:
            return f'[multiple pages "{name}" found]'
