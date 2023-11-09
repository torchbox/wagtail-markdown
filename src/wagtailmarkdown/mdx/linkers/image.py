import contextlib
import xml.etree.ElementTree as etree

from django.conf import settings

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from wagtail.images import get_image_model

from wagtailmarkdown.constants import (
    DEFAULT_IMAGE_OPTS,
    SETTINGS_MODE_OVERRIDE,
    WRAP_IMAGES_IN_ANCHORS,
)

OPTS = getattr(settings, "WAGTAILMARKDOWN", {}).get("image_opts", DEFAULT_IMAGE_OPTS)

wrap_images_in_anchors = getattr(settings, "WAGTAILMARKDOWN", {}).get(
    "wrap_images_in_anchors", WRAP_IMAGES_IN_ANCHORS
)


class Linker:
    def run(self, fname, options):
        opts = OPTS

        for opt in options:
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
                with contextlib.suppress(ValueError):
                    opts["spec"] = "width-%d" % int(value)

        try:
            image = get_image_model().objects.get(title=fname)
        except ObjectDoesNotExist:
            return f'[image "{fname}" not found]'
        except MultipleObjectsReturned:
            return f'[multiple images "{fname}" found]'

        image_url = image.file.url
        rendition = image.get_rendition(opts["spec"])

        if not wrap_images_in_anchors:
            img = etree.Element("img")
            img.set("src", rendition.url)
            img.set("class", opts["classname"])
            img.set("width", str(rendition.width))
            img.set("height", str(rendition.height))
            return img
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
