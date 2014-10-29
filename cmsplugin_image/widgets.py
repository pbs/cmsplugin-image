from django.template.loader import render_to_string
from django.template import RequestContext
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase


class FileField(SmartSnippetWidgetBase):
    name = 'Filer File Field'

    def _get_render_options(self):
        return {'field': self.variable,
                'value_dict': self.formatted_value,
                'file_type': 'file'}

    def render(self, request):
        return render_to_string(
            'smartsnippets/widgets/filerfield/widget.html',
            self._get_render_options(),
            context_instance=RequestContext(request))

widget_pool.register_widget(FileField)


class ImageField(FileField):
    name = 'Image Field'

    def _get_render_options(self):
        opts = super(FileField, self)._get_render_options()
        opts.update({'file_type': 'image'})
        return opts

widget_pool.register_widget(ImageField)


class OptionalImageField(ImageField):
    name = 'Optional Image Field'

    def _get_render_options(self):
        opts = super(OptionalImageField, self)._get_render_options()
        opts.update({'optional_field': True})
        return opts


widget_pool.register_widget(OptionalImageField)
