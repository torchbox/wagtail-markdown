from django.conf import settings
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def editor_js():
    s = """<script src="{0}wagtailmarkdown/js/simplemde.min.js"></script>"""
    s += """<script src="{0}wagtailmarkdown/js/simplemde.attach.js"></script>"""
    return s.format(settings.STATIC_URL)


@hooks.register('insert_editor_css')
def editor_css():
    s = """<link rel="stylesheet" href="{0}wagtailmarkdown/css/simplemde.min.css">"""
    return s.format(settings.STATIC_URL)
