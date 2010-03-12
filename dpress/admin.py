from models import Post
from django.contrib import admin
from tinymce.settings import JS_URL
from django.conf import settings

class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'publish', 'status')
    list_filter         = ('publish', 'status')
    search_fields       = ('title', 'body', 'tease')
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        js = [JS_URL, 
                settings.MEDIA_URL + 'scripts/admin/TinyMCEAdmin.js',
                settings.MEDIA_URL + 'scripts/admin/EditBlog.js',
                ]

admin.site.register(Post, PostAdmin)
