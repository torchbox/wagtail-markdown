# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
from importlib import import_module

import markdown

LINKER_RE = r"<:([a-z]+:)?([^>|\n]+)((\|[^>|\n]+){0,})>"


class LinkerPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, re, md, linktypes):
        markdown.inlinepatterns.Pattern.__init__(self, re, md)
        self.linktypes = linktypes

    def handleMatch(self, m):
        linktypes = self.linktypes
        opts = []
        if m.group(3) is not None and len(m.group(4)):
            opts = m.group(4).split("|")[1:]

        type = m.group(2)
        if type is None:
            type = "__default__"
        mod = import_module(linktypes[type])
        c = mod.Linker()

        return c.run(m.group(3), opts)
        return "[invalid link]"


class LinkerExtension(markdown.Extension):
    def __init__(self, linktypes):
        markdown.Extension.__init__(self)
        self.linktypes = linktypes

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["linker"] = LinkerPattern(LINKER_RE, md, self.linktypes)


def makeExtension(configs=None):
    return LinkerExtension(configs=configs)
