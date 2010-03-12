from django.contrib import admin
from links.models import Category, Link

class LinksAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Link, LinksAdmin)
admin.site.register(Category, CategoryAdmin)

