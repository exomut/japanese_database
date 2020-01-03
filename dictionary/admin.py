from django.contrib import admin

from .models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'seq_id', 'japanese']


admin.site.register(Entry, EntryAdmin)
