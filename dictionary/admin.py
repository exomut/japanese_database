from django.contrib import admin

from .models import Entry, Kanji, Reading, Sense, Translation


class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'ent_seq']


class KanjiAdmin(admin.ModelAdmin):
    list_display = ['entry_id', 'kanji_num', 'keb', 'ke_inf']


class ReadingAdmin(admin.ModelAdmin):
    list_display = ['entry_id', 'reading_num', 'reb', 're_inf']


class SenseAdmin(admin.ModelAdmin):
    list_display = ['entry_id', 'sense_num', 'stagk', 'stagr', 'xref', 'ant', 'pos', 'field', 'misc', 'lsource', 'dial', 'pri', 's_inf']


class TranslationAdmin(admin.ModelAdmin):
    list_display = ['entry_id', 'sense_num', 'translation_num', 'gloss', 'lang']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Kanji, KanjiAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Sense, SenseAdmin)
admin.site.register(Translation, TranslationAdmin)
