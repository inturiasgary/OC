from django.contrib import admin
from models import Gallery, Picture

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'picture_count')
    list_filter = ['date_added']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('pictures',)

class PictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added')
    list_filter = ['date_added']
    search_fields = ['title', 'title_slug', 'caption']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
