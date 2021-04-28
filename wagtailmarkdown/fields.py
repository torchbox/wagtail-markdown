# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
import warnings

from django.db.models import TextField

from .blocks import MarkdownBlock
from .warnings import WagtailMarkdownDeprecationWarning
from .widgets import MarkdownTextarea


class MarkdownBlock(MarkdownBlock):
    def __init__(self, *args, **kwargs):
        super(MarkdownBlock, self).__init__(*args, **kwargs)
        warning = (
            "Importing `wagtailmarkdown.fields.MarkdownBlock` is depreceated. "
            "Please use the `wagtailmarkdown.blocks.MarkdownBlock` import "
            "instead."
        )
        warnings.warn(warning, WagtailMarkdownDeprecationWarning, stacklevel=2)


class MarkdownField(TextField):
    def formfield(self, **kwargs):
        defaults = {"widget": MarkdownTextarea}
        defaults.update(kwargs)
        return super(MarkdownField, self).formfield(**defaults)

    def __init__(self, **kwargs):
        super(MarkdownField, self).__init__(**kwargs)
