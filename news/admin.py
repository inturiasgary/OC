from django.contrib import admin

from news.models import NewsItem, NewsAuthor

class NewsItemAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ['title', 'date', 'site']
	list_filter = ['date']
	search_fields = ['title', 'body']
	date_hierarchy = 'date'
	ordering = ['-date']
	fieldsets = (
		('Article info', {
			'fields': ('title', 'body', 'date')
		}),
		('Advanced', {
			'classes': ['collapse'],
			'fields': ('snippet', 'slug',)
		}),
	)
	
	def queryset(self, request):
		return NewsItem.on_site.all()
		
admin.site.register(NewsItem, NewsItemAdmin)