import xml.etree.ElementTree as etree

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from wagtail.documents import get_document_model


class Linker:
    def run(self, name, options):
        try:
            text = name
            if options:
                text = options[0]

            a = etree.Element("a")
            a.set("href", get_document_model().objects.get(title=name).url)
            a.text = text
            return a
        except ObjectDoesNotExist:
            return f'[document "{name}" not found]'
        except MultipleObjectsReturned:
            return f'[multiple documents "{name}" found]'
