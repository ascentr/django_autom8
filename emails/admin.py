from django.contrib import admin
from . models import List, Subscriber, Email, EmailTracking, Sent


# class ModelNameAdmin(admin.ModelAdmin):
#     '''Admin View for ModelName'''
#     list_display = ('',)
#     list_filter = ('',)
#     raw_id_fields = ('',)
#     readonly_fields = ('',)
#     search_fields = ('',)
#     date_hierarchy = ''
#     ordering = ('',))

class EmailTrackingAdmin(admin.ModelAdmin):
  list_display = ['email', 'subscriber', 'opened_at', 'clicked_at']

admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(EmailTracking, EmailTrackingAdmin)
admin.site.register(Sent)