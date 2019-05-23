# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# tomasz.knapik@torchbox.com 2017-12-07
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#


def setup():
    # Make warnings visible
    import warnings
    from .warnings import WagtailMarkdownDeprecationWarning
    warnings.simplefilter('default', WagtailMarkdownDeprecationWarning)


setup()


# Classes below are here so users who use old imports get
# meaningful errors.
class DeprecatedObject(object):
    def __init__(self, *args, **kwargs):
        warning = (
            "The `wagtailmarkdown.{class_name}` import is not valid. Please "
            "use `wagtailmarkdown.{new_path}` instead."
        ).format(
            new_path=self.new_path,
            class_name=self.class_name
        )
        raise ImportError(warning)


old_classes = [
    ('MarkdownBlock', 'blocks.MarkdownBlock'),
    ('MarkdownField', 'fields.MarkdownField'),
    ('MarkdownPanel', 'edit_handlers.MarkdownPanel'),
    ('MarkdownTextarea', 'widgets.MarkdownTextarea'),
]

for class_name, new_path in old_classes:
    locals()[class_name] = type(class_name, (DeprecatedObject,), {
        'class_name': class_name,
        'new_path': new_path,
    })
