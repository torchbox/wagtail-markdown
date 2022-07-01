from django.db.models import TextField

from .widgets import MarkdownTextarea


class MarkdownField(TextField):
    def formfield(self, **kwargs):
        defaults = {"widget": MarkdownTextarea}
        defaults.update(kwargs)
        return super().formfield(**defaults)
