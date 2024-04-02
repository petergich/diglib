from django.contrib import admin
from django.utils.html import mark_safe
from .models import *
#from report_builder.models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'modified')
    search_fields = ('name',)

class ArchivesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type', 'genre', 'created_at', 'display_preview_image')
    search_fields = ('name', 'description', 'genre')
    list_filter = ('type', 'genre', 'created_at')

class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('get_owner_username', 'account', 'display_profile_image')  # Update list_display
    search_fields = ('get_owner_username', 'account')

    def get_owner_username(self, obj):
        return obj.owner.username
    get_owner_username.short_description = 'Owner Username'

    def display_profile_image(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" style="max-height:100px;max-width:100px;" />')
        else:
            return 'No Preview Available'

    display_profile_image.short_description = 'Profile Image'

admin.site.register(Archive, ArchivesAdmin)
admin.site.register(Profile, ProfilesAdmin)
admin.site.register(Archive_owner)
