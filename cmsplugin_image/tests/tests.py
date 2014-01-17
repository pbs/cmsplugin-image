from django.test import TestCase
from django.contrib.sites.models import Site
from django.http import HttpRequest

from smartsnippets.models import SmartSnippet, Variable, SmartSnippetVariable, SmartSnippetPointer
from smartsnippets.signals import ss_plugin_var_saved
from ..models import ImageSize, ImageSizeContext, ImageSizeContextManager, ImageCrop



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
        from ..widgets import persist_image_crop
        # it seems that the test environment does not connect the signals, hence:
        ss_plugin_var_saved.connect(persist_image_crop, weak=False)
        
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
        # create the crop object, simulating what happens inside ImageField#_get_render_options()
        crop = ImageCrop.objects.get_or_create(variable = var, 
                                               crop_x = 0, 
                                               crop_y = 0,
                                               crop_w = 120,
                                               crop_h = 60)
        self.assertIsNotNone(Variable.objects.get(snippet_variable=self.ss_var,
                                                  value=PYTHON_LOGO_URL,
                                                  snippet=ss_pointer))
        # simulate crop action on the client
        req = HttpRequest()
        req.method = 'POST'
        req.POST = {str(var.id) + '_cropx': 0.0,
                    str(var.id) + '_cropy': 0.0,
                    str(var.id) + '_cropw': 30.0,
                    str(var.id) + '_croph': 30.0
                    }
        req.path = '/irrelevant'
        
        ss_plugin_var_saved.send(sender=var, request=req.POST)
        
        # now the signal mechanism should have updated the ImageCrop object
        # TODO no idea why ImageCrop.objects.get(variable=var) gives 'matching query does not exist'
        for obj in ImageCrop.objects.all():
            if obj.variable == var:
                self.assertTrue(obj.crop_x == 0 and obj.crop_y == 0 and obj.crop_w == 30 and obj.crop_h == 30)
                return
        # TODO: read the image file from s3/FS and compare its size with the crop value
        self.assertFalse(True)