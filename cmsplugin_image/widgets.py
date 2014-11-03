from django.template.loader import render_to_string
from django.template import RequestContext
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase


class FileField(SmartSnippetWidgetBase):
    name = 'Filer File Field'
    filer_file_type = 'file'
    optional_field = False

    def _get_render_options(self):
        return {
            'field': self.variable,
            'value_dict': self.formatted_value,
            'file_type': self.filer_file_type,
            'optional_field': self.optional_field
        }

    def render(self, request):
        return render_to_string(
            'smartsnippets/widgets/filerfield/widget.html',
            self._get_render_options(),
            context_instance=RequestContext(request))


class ImageField(FileField):
    name = 'Image Field'
    filer_file_type = 'image'


class OptionalImageField(ImageField):
    name = 'Optional Image Field'
    optional_field = True


FILER_WIDGETS = (FileField, ImageField, OptionalImageField)
for widget in FILER_WIDGETS:
    widget_pool.register_widget(widget)
