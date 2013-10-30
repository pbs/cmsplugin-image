from django.template.loader import render_to_string
from django.template import RequestContext
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase
from django.core.urlresolvers import reverse, NoReverseMatch


try:
    from cropduster.models import ImageContext
except ImportError:
    ImageContext = None


class ImageField(SmartSnippetWidgetBase):
    name = 'Image Field'

    def _get_render_options(self):
        size_set_id = ''
        if ImageContext:
            size_set_id = ImageContext.objects.get_size_set(
                self.variable.snippet_variable) or ''

        try:
            cropduster_url = reverse('cropduster-upload')
        except NoReverseMatch:
            cropduster_url = ''

        return {'field': self.variable,
                'value_dict': self.formatted_value,
                'size_set_id': size_set_id,
                'cropduster_url': cropduster_url}

    def render(self, request):
        context_instance = RequestContext(request)
        return render_to_string(
            'smartsnippets/widgets/imagefield/widget.html',
            self._get_render_options(),
            context_instance=context_instance)

widget_pool.register_widget(ImageField)


class OptionalImageField(ImageField):
    name = 'Optional Image Field'

    def _get_render_options(self):
        opts = super(OptionalImageField, self)._get_render_options()
        opts.update({'optional_field': True})
        return opts


widget_pool.register_widget(OptionalImageField)
