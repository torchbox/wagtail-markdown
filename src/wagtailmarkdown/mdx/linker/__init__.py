from importlib import import_module

from markdown import Extension
from markdown.inlinepatterns import Pattern


LINKER_RE = r"<:([a-z]+:)?([^>|\n]+)((\|[^>|\n]+){0,})>"


class LinkerPattern(Pattern):
    def __init__(self, pattern, md, link_types):
        super().__init__(pattern, md)
        self.link_types = link_types

    def handleMatch(self, m):
        link_types = self.link_types
        opts = []
        if m.group(3) is not None and len(m.group(4)):
            opts = m.group(4).split("|")[1:]

        link_type = m.group(2)
        if link_type is None:
            link_type = "__default__"

        try:
            mod = import_module(link_types[link_type])
            c = mod.Linker()

            return c.run(m.group(3), opts)
        except KeyError:
            return f'[invalid linker type "{link_type.rstrip(":")}"]'


class LinkerExtension(Extension):
    def __init__(self, link_types, **kwargs):
        super().__init__(**kwargs)
        self.link_types = link_types

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            LinkerPattern(LINKER_RE, md, self.link_types), "linker", 9
        )


def makeExtension(**kwargs):
    """As per https://python-markdown.github.io/extensions/api/#dot_notation"""
    return LinkerExtension(**kwargs)  # pragma: no cover
