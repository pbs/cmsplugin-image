# coding=utf-8
from django.contrib import admin
from cmsplugin_image.models import ImageSize

admin.site.register(ImageSize)


class ImageSizeAdmin(admin.TabularInline):
    model = ImageSize
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'width',
                'height',
                'aspect_ratio',
            ),
        }),
    )
    max_num = 1
    min_num = 1

    def __init__(self, *args, **kwargs):
        super(ImageSizeAdmin, self).__init__(*args, **kwargs)
        self.can_delete = False

class SizeSetAdmin(admin.ModelAdmin):
    inlines = [ImageSizeAdmin]
