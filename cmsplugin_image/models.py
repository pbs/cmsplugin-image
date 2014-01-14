# coding=utf-8
from django.db import models
from smartsnippets.models import Variable, SmartSnippetVariable, SmartSnippetPointer, SmartSnippet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class ImageSize(models.Model):
    class Meta:
        db_table = "image_size"

    name = models.CharField(max_length=128, db_index=True, unique=True)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    aspect_ratio = models.FloatField(null=True, blank=True)

    def get_height(self):
        """ Returns calculated height, if possible.

        @return: Height
        @rtype: positive int
        """
        if self.height is None and self.width and self.aspect_ratio:
            return int(round(self.width / self.aspect_ratio))

        return self.height

    def get_width(self):
        """ Returns calculate width, if possible.

        @return: Width
        @rtype: positive int
        """
        if self.width is None and self.height and self.aspect_ratio:
            return int(round(self.height * self.aspect_ratio))

        return self.width

    def get_aspect_ratio(self):
        """ Returns calculated aspect ratio, if possible.

        @return: Aspect Ratio
        @rtype:  float
        """
        if self.aspect_ratio is None and self.height and self.width:
            return round(self.width / float(self.height), 2)

        return self.aspect_ratio

    def get_dimensions(self):
        """
        Returns all calculated dimensions for the size.

        @return: width, height, aspect ratio
        @rtype: (int > 0, int > 0, float > 0)
        """
        return (self.get_width(), self.get_height(), self.get_aspect_ratio())

    def __unicode__(self):
	return self.name


class ImageCrop(models.Model):
    class Meta:
        db_table = "image_crop"

    crop_x = models.IntegerField(null=False)
    crop_y = models.IntegerField(null=False)
    crop_w = models.IntegerField(null=False)
    crop_h = models.IntegerField(null=False)
    original_path = models.CharField(null=True, max_length=512)
    variable = models.ForeignKey(Variable)

class ImageSizeContextManager(models.Manager):

    def update(self, model_instance, image_size):
        img_ctx = self.get_image_context(model_instance)
        if img_ctx:
            if not image_size:
                img_ctx.delete()
            else:
                img_ctx.image_size_id = image_size.id
                img_ctx.save()
        elif image_size:
            img_ctx = ImageSizeContext(content_object=model_instance,
                image_size=image_size)
            img_ctx.save()

    def get_image_context(self, model_instance):
        ct = ContentType.objects.get_for_model(model_instance)
        img_ctx = ImageSizeContext.objects.filter(
            content_type=ct.id,
            object_id=model_instance.id) or [None]
        return img_ctx[0]

    def get_image_size(self, model_instance):
        img_ctx = self.get_image_context(model_instance)
        return img_ctx.image_size.id if img_ctx else None

    def get_by_object_id(self, obj_id):
        return self.filter(object_id=obj_id)


class ImageSizeContext(models.Model):
    """ This model indirectly links a SmartSnippetVariable to an ImageSize
        via the GenericForeignKey mechanism.
    """
    image_size = models.ForeignKey(ImageSize, blank=True, null=True)

    # The standard fields for a GenericForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = ImageSizeContextManager()

    class Meta:
        unique_together = ("content_type", "object_id")


#noinspection PyUnusedLocal,PyUnresolvedReferences
@receiver(pre_delete, sender=SmartSnippetVariable, dispatch_uid='ss_dispatch')
def delete_img_context(sender, instance, **kwargs):
    """ Delete the imgSize_context entries which are indirectly linked 
    (Generic_FK) to the SmartSnippetVariable
    """
    for obj in ImageSizeContext.objects.get_by_object_id(instance.id):
        obj.delete()
