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

try:  # wagtail < 2.0
    from wagtail.wagtailimages import get_image_model
except ImportError:  # wagtail >= 2.0
    from wagtail.images import get_image_model


# TODO: Default spec and class should be configurable, because they're
# dependent on how the project is set up.  Hard-coding of 'left',
# 'right' and 'full-width' should be removed.


class Linker(object):
    def run(self, fname, optstr):
        opts = {}

        opts["spec"] = "width-500"
        opts["classname"] = "left"

        for opt in optstr:
            bits = opt.split("=", 1)
            opt = bits[0]
            value = ""

            if len(bits) > 1:
                value = bits[1]

            if opt == "left":
                opts["classname"] = "left"
            elif opt == "right":
                opts["classname"] = "right"
            elif opt == "full":
                opts["classname"] = "full-width"
            elif opt == "width":
                try:
                    opts["spec"] = "width-%d" % int(value)
                except ValueError:
                    pass
        try:
            image = get_image_model().objects.get(title=fname)
        except ObjectDoesNotExist:
            return '[image "{}" not found]'.format(fname)
        except MultipleObjectsReturned:
            return '[multiple images "{}" found]'.format(fname)

        image_url = image.file.url
        rendition = image.get_rendition(opts["spec"])

        a = etree.Element("a")
        a.set("data-toggle", "lightbox")
        a.set("data-type", "image")
        a.set("href", image_url)
        img = etree.SubElement(a, "img")
        img.set("src", rendition.url)
        img.set("class", opts["classname"])
        img.set("width", str(rendition.width))
        img.set("height", str(rendition.height))
        return a
