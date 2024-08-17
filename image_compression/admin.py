from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html


def get_img_size(obj):
  return f'{obj.size / (1024*1024):.2f} MB' if len(str(obj.size)) > 6 else f'{obj.size /1024:.2f} KB'


class CompressImageAdmin(admin.ModelAdmin):
  def thumbnail(self, obj):
    return format_html(f'<img src="{obj.compressed_img.url}" width="40" height="40">')

  def original_img_size(self, obj):
    return format_html(get_img_size(obj.original_img))

  def compressed_img_size(self, obj):
    return format_html(get_img_size(obj.compressed_img))

  list_display = ['user', 'thumbnail', 'original_img_size', 'compressed_img_size', 'quality', 'compressed_at']


admin.site.register(CompressImage, CompressImageAdmin)


