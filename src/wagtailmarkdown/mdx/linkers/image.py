import contextlib
import xml.etree.ElementTree as etree

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from wagtail.images import get_image_model


# TODO: Default spec and class should be configurable, because they're
# dependent on how the project is set up.  Hard-coding of 'left',
# 'right' and 'full-width' should be removed.


class Linker:
    def run(self, fname, options):
        opts = {
            "spec": "width-500",
            "classname": "left",
        }

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
                    opts["spec"] = f"width-{int(value)}"

        try:
            image = get_image_model().objects.get(title=fname)
        except ObjectDoesNotExist:
            return f'[image "{fname}" not found]'
        except MultipleObjectsReturned:
            return f'[multiple images "{fname}" found]'

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
