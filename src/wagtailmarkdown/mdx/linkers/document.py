from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

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
