from django.test import TestCase

from smartsnippets.models import SmartSnippet, Variable, SmartSnippetVariable, SmartSnippetPointer
from smartsnippets.signals import ss_plugin_var_saved
from ..models import ImageSize, ImageSizeContext, ImageSizeContextManager, ImageCrop
from django.contrib.sites.models import Site


SS_NAME='image_size_test'


SS_VAR_NAME='banner_img'


SS_VAR_WIDGET_TYPE='ImageField'


SS_TEMPLATE_CODE='' \
    '{% comment %} ' \
    '<!-- SmartSnippets Variables \n' + SS_VAR_NAME + '=' + SS_VAR_WIDGET_TYPE + '\n' \
    '--> ' \
    '{% endcomment %} ' \
    '<div><img src=\"{{' + SS_VAR_NAME + '}}\"/></div>'


PYTHON_LOGO_URL='http://www.python.org/community/logos/python-logo-master-v3-TM.png'

class FileOpsTestCase(TestCase):
    """ Small integration test for the most common usage
        of the cropping feature
    """
    def setUp(self):
        self.site = Site.objects.get(pk=1)
        self.assertIsNotNone(self.site)
        self.ss = SmartSnippet.objects.create(name=SS_NAME, 
                                              template_code=SS_TEMPLATE_CODE, 
                                              template_path = '')
        self.ss.save()
        self.ss.sites.add(self.site)
        self.ss.save()
        self.assertIsNotNone(SmartSnippet.objects.get(name=SS_NAME, 
                                                      template_code=SS_TEMPLATE_CODE))

        self.ss_var = SmartSnippetVariable.objects.create(name=SS_VAR_NAME, 
                                                          widget=SS_VAR_WIDGET_TYPE, 
                                                          snippet=self.ss)
        self.ss_var.save()
        self.assertIsNotNone(SmartSnippetVariable.objects.get(name=SS_VAR_NAME, 
                                                              widget=SS_VAR_WIDGET_TYPE))
        
    def testImageCropNotSaved(self):
        """ In this scenario we should not have any ImageCrop instance linked to 
            smart snippet variable, since no ImageSize is associated with the smart 
            snippet variable
        """
        ss_pointer = SmartSnippetPointer.objects.create(snippet=self.ss)
        var = Variable.objects.create(snippet_variable=self.ss_var,
                                value=PYTHON_LOGO_URL,
                                snippet=ss_pointer)
        var.save()
        self.assertIsNotNone(Variable.objects.get(snippet_variable=self.ss_var,
                                                  value=PYTHON_LOGO_URL,
                                                  snippet=ss_pointer))
        
        # TODO no idea why ImageCrop.objects.get(variable=var) gives 'matching query does not exist'
        found = False
        if ImageCrop.objects:
            for crop in ImageCrop.objects.all():
                if crop.variable == var:
                    found = True
        self.assertFalse(found)

    def testImageCropSaved(self):
        """ Test whether an ImageCrop instance is created when we save
            a Variable instance.
            Note: a 100% correct integration tets would make sure this happens when a 
            SmartSnippetPlugin is saved (see SmartSnippetPlugin#save_model())
        """
        img_size = ImageSize.objects.create(name='size_200_200', width=200, height=200)
        img_size_ctx = ImageSizeContext.objects.create(image_size=img_size, content_object=self.ss_var)
        img_size_ctx.save()
        self.assertIsNotNone(img_size_ctx)
        
        ss_pointer = SmartSnippetPointer.objects.create(snippet=self.ss)
        var = Variable.objects.create(snippet_variable=self.ss_var,
                                value=PYTHON_LOGO_URL,
                                snippet=ss_pointer)
        var.save()
        self.assertIsNotNone(Variable.objects.get(snippet_variable=self.ss_var,
                                                  value=PYTHON_LOGO_URL,
                                                  snippet=ss_pointer))

        request = Client().post('/admin/', {
                                            '_current_site':168,
                                            var.id + '_cropx': 0.0, 
                                            var.id + '_cropy': 0.0, 
                                            var.id + '_cropw': 60, 
                                            var.id + '_croph': 60,
                                            })
        ss_plugin_var_saved.send(sender=var, request=request)
        # now the signal mechanism should have created a new ImageCrop
        self.assertIsNotNone(ImageCrop.objects.get(variable=var))