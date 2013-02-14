from django.template.loader import render_to_string
from django.template import RequestContext
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase


class ImageField(SmartSnippetWidgetBase):
    name = 'Image Field'

    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string('smartsnippets/widgets/imagefield/widget.html',
            {
                'field': self.variable,
                'value_dict': self.formatted_value
            },
            context_instance=context_instance)

widget_pool.register_widget(ImageField)


class OptionalImageField(ImageField):
    name = 'Optional Image Field'

    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string('smartsnippets/widgets/imagefield/widget.html',
            {
                'field': self.variable,
                'value_dict': self.formatted_value,
                'optional_field': True
            },
            context_instance=context_instance)

widget_pool.register_widget(OptionalImageField)
