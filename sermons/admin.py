from django.contrib import admin
from sermons.models import Pastor, Subject, Sermon, Attachment

class PastorAdmin(admin.ModelAdmin):
    pass

class SubjectAdmin(admin.ModelAdmin):
    pass

class SermonAdmin(admin.ModelAdmin):
    pass

class AttachmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pastor, PastorAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Sermon, SermonAdmin)
admin.site.register(Attachment, AttachmentAdmin)



