from importlib import import_module

from markdown import Extension
from markdown.inlinepatterns import Pattern


LINKER_RE = r"<:([a-z]+:)?([^>|\n]+)((\|[^>|\n]+){0,})>"


class LinkerPattern(Pattern):
    def __init__(self, re, md, linktypes):
        super().__init__(re, md)
        self.linktypes = linktypes

    def handleMatch(self, m):
        linktypes = self.linktypes
        opts = []
        if m.group(3) is not None and len(m.group(4)):
            opts = m.group(4).split("|")[1:]

        link_type = m.group(2)
        if link_type is None:
            link_type = "__default__"
        mod = import_module(linktypes[link_type])
        c = mod.Linker()

        return c.run(m.group(3), opts)


class LinkerExtension(Extension):
    def __init__(self, linktypes):
        super().__init__()
        self.linktypes = linktypes

    def extendMarkdown(self, md):
        md.inlinePatterns.register(LinkerPattern(LINKER_RE, md, self.linktypes),
                                   "linker", 9)
#
#
# def makeExtension(configs=None):
#     return LinkerExtension(configs=configs)
