import markdown


class ImagePattern(markdown.inlinepatterns.ImagePattern):

    def __init__(self, object_lookup_negotiator, *args, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator
        super().__init__(*args, **kwargs)

    def handleMatch(self, match):
        element = super().handleMatch(match)
        url = element.get('src', '')
        image = self.object_lookup_negotiator.retrieve(url)
        if image:
            rendition = image.get_rendition('width-500')
            element.set('src', rendition.url)
            element.set('class', 'left')
            element.set('width', str(rendition.width))
            element.set('height', str(rendition.height))
        return element


class LinkPattern(markdown.inlinepatterns.LinkPattern):

    def __init__(self, object_lookup_negotiator, *args, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator
        super().__init__(*args, **kwargs)

    def sanitize_url(self, url):
        instance = self.object_lookup_negotiator.retrieve(url)
        if instance:
            url = instance.url
        return super().sanitize_url(url)
