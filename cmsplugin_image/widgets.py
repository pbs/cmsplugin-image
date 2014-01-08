from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.signals import request_finished
from django.dispatch import receiver
from smartsnippets.widgets_pool import widget_pool
from smartsnippets.widgets_base import SmartSnippetWidgetBase
from models import ImageSize, ImageSizeContext, ImageSizeContextManager, ImageCrop
from smartsnippets.models import SmartSnippetVariable
from PIL import Image, ImageFile
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from cmsplugin_image.settings import S3_CROPPED_PREFIX, S3_FILER_STORAGE
from django.conf import settings
import os
import cStringIO
import urllib
import datetime
import math


class ImageField(SmartSnippetWidgetBase):
    name = 'Image Field'

    def _get_render_options(self):
        image_size = get_image_size(self.variable)
        image_crop = None
        if image_size:
            image_crops = ImageCrop.objects.filter(variable=self.variable)
            if not image_crops:
                image_crop = ImageCrop(crop_x=CANVAS_WIDTH/4, crop_y=100, 
                    crop_w=CANVAS_WIDTH/2, crop_h=200, 
                    variable_id=self.variable.id)
                image_crop.save()
            else:
                image_crop = image_crops[0]
        # we want to show the original image, not the cropped one 
        # (if the image was already cropped)
        image_path = image_crop.original_path if image_crop and image_crop.original_path else self.variable.value
        canvas_w, canvas_h, zoom_factor = get_width_height_zoom(image_path)
        return {'field': self.variable,
                'value_dict': self.formatted_value,
                'image_size': image_size,
                'image_crop': image_crop,
                'image_path': image_path,
                'canvas_w': canvas_w,
                'canvas_h': canvas_h,
                # how much smaller is the image in the canvas?
                'zoom_factor': zoom_factor      
                }

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


CANVAS_WIDTH=600
CANVAS_HEIGHT=400


def get_width_height_zoom(image_path):
    """ Calculate the area of the canvas and the zoom_factor 
    (for factoring the crop)
    """
    img = load_image(image_path) if image_path else None
    if not img:
        return CANVAS_WIDTH, CANVAS_HEIGHT, 1.0
    (img_width,img_height) = img.size if img else (CANVAS_WIDTH, CANVAS_HEIGHT)
    aspect_ratio = round(float(img_width) / float(img_height), 2)
    
    canvas_w = CANVAS_WIDTH if img_width > CANVAS_WIDTH else img_width
    canvas_h = round(canvas_w / aspect_ratio, 2)
    zoom_factor = float(img_width) / float(canvas_w)
    return canvas_w, canvas_h, zoom_factor


def get_image_size(smartsnippet_variable):
    smartsnippet_var = SmartSnippetVariable.objects.filter(
        id=smartsnippet_variable.snippet_variable_id)[0]
    img_context = ImageSizeContext.objects.get_img_ctx(smartsnippet_var)
    if img_context:
        return img_context.image_size
    return None


try:
    from smartsnippets.signals import smartsnippet_var_saved
except ImportError:
    smartsnippet_var_saved = None       


def load_image(image_path):
    _file = cStringIO.StringIO(urllib.urlopen(image_path).read())
    img = Image.open(_file)
    img.load()
    _file.close()
    return img


@receiver(smartsnippet_var_saved)
def persist_image_crop(sender, request, **kwargs):
    image_crops = ImageCrop.objects.filter(variable=sender)
    image_size = get_image_size(sender)
    if not image_crops or not image_crops[0] or not image_size:
        return
    image_crop = image_crops[0]
    
    crop_x = request.get(str(sender.id) + '_cropx', '')
    crop_y = request.get(str(sender.id) + '_cropy', '')
    crop_w = request.get(str(sender.id) + '_cropw', '')
    crop_h = request.get(str(sender.id) + '_croph', '')
    
    if crop_x and crop_y and crop_w and crop_h:
        image_crop.crop_x = int(round(float(crop_x), 1))
        image_crop.crop_y = int(round(float(crop_y), 1))
        image_crop.crop_w = int(round(float(crop_w), 1))
        image_crop.crop_h = int(round(float(crop_h), 1))
        if not CROP in sender.value:
            image_crop.original_path = sender.value
        image_crop.save()
        cropped_img_path = crop_and_save(image_crop.original_path, 
            image_crop, image_size)
        sender.value = cropped_img_path
        sender.save()


UNKNOWN_EXTENSION = "##invalid##"


def crop_image(img, x1, y1, x2, y2):
    cropped_img = img.crop((x1, y1, x2, y2))
    cropped_img.load()
    cropped_img.format = img.format
    return cropped_img


def resize_image(img, img_size):
    (w,h) = img.size
    resize_ratio = min(img_size.width / float(w), img_size.height / float(h))
    new_size = int(math.ceil(w * resize_ratio)), int(math.ceil(h * resize_ratio))
    img.thumbnail(new_size, Image.ANTIALIAS)
    

def crop_and_save(image_path, image_crop, image_size):
    img = load_image(image_path)
    cropped_img = crop_image(img, image_crop.crop_x, image_crop.crop_y, 
        image_crop.crop_x + image_crop.crop_w, 
        image_crop.crop_y + image_crop.crop_h)
    resize_image(cropped_img, image_size)
    # compose a name for the cropped image by using a naming convention
    cropped_file_name = rename_cropped_file(image_path)
    # it is good to have the correct file extension determined
    cropped_file_name = replace_file_extension(img, cropped_file_name)
    return save_to_s3(cropped_img, cropped_file_name)


SEP = '__'
CROP = SEP + 'crop' + SEP


def rename_cropped_file(file_path):
    """
    Naming convention for cropped files
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    crt_file_name = os.path.basename(file_path)
    already_cropped = crt_file_name.startswith(CROP)

    if not already_cropped:
        # __crop__$timestamp__$original_filename
        filename = CROP + '{0}{1}{2}'.format(timestamp, SEP, crt_file_name)
    else:
        # replace old $timestamp with new $timestamp => 
        # __crop__$new_timestamp__$original_filename
        start = len(CROP)
        end = crt_file_name.find(SEP, start)
        if (start, end) != (-1, -1):
            filename = crt_file_name[:start] + timestamp + crt_file_name[end:]
        else:
            # maybe it was renamed from the interface and does not follow the 
            # (exact) naming convention
            filename = '{0}{1}{2}'.format(timestamp, SEP, crt_file_name)
    return filename


def replace_file_extension(img, img_filename):
    """
    Replace (junk or invalid extension) OR append the correct extension to an 
    image file,
    based on the file's format metadata
    """
    file_ext = try_to_guess_extension(img)
    if file_ext != UNKNOWN_EXTENSION:
        idx = img_filename.rfind('.')
        # assume an extension length of maximum 4 chars
        # in case the file has a junk extension, that junk will be replaced: 
        # 'name.blah' -> 'name.jpeg'
        if idx != -1 and len(img_filename) - idx <= 5:
            img_filename = img_filename[0:idx] + '.' + file_ext
        else:
            # ...but 'something.blablabla' will be replaced with 
            # 'something.blablabla.jpeg'
            img_filename += '.' + file_ext
    return img_filename


def try_to_guess_extension(img):
    try:
        return str(img.format).lower()
    except AttributeError:
        return UNKNOWN_EXTENSION


def save_to_s3(img, filename):
    FILER_STORAGES = getattr(settings, 'FILER_STORAGES')
    if not FILER_STORAGES:
        return
    access_key = FILER_STORAGES[S3_FILER_STORAGE]['main']['OPTIONS']['access_key']
    secret_key = FILER_STORAGES[S3_FILER_STORAGE]['main']['OPTIONS']['secret_key']
    bucket_name= FILER_STORAGES[S3_FILER_STORAGE]['main']['OPTIONS']['bucket']
    conn = S3Connection(access_key, secret_key)
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket, S3_CROPPED_PREFIX + '/' + filename)
    data = cStringIO.StringIO()
    img.save(data, img.format)
    data.seek(0)
    k.set_contents_from_file(data)
    # TODO: a way to generate permanent URLs? - poor boto s3 doc
    return k.generate_url(expires_in=20*365*24*3600, query_auth=True, 
        force_http=True)

