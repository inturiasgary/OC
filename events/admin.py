from django.contrib import admin
from events.models import Event

class EventsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Event, EventsAdmin)


