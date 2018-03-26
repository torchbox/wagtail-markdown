# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# tomasz.knapik@torchbox.com 2017-12-07
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
try:
    from wagtail.admin.edit_handlers import FieldPanel
except ImportError:
    from wagtail.wagtailadmin.edit_handlers import FieldPanel


class MarkdownPanel(FieldPanel):
    pass
