from django.contrib import admin

from .models import Entry, Reading, Definition, Translation


class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'keb']


class ReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry_id', 'reb']


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'reading_id']


class TranslationAdmin(admin.ModelAdmin):
    list_display = ['id', 'definition_id', 'gloss', 'lang']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Translation, TranslationAdmin)
