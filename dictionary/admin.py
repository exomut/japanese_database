from django.contrib import admin

from .models import Entry, Kanji, Reading, Sense, Translation, Example


class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'ent_seq']


class KanjiAdmin(admin.ModelAdmin):
    list_display = ['keb', 'id', 'entry_id', 'kanji_num', 'ke_inf', 'ke_pri']


class ReadingAdmin(admin.ModelAdmin):
    list_display = ['reb', 'id', 'entry_id', 'reading_num', 're_nokanji', 're_restr', 're_inf', 're_pri']


class SenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry_id', 'sense_num', 'stagk', 'stagr', 'xref', 'ant', 'pos', 'field', 'misc', 'lsource', 'dial', 'pri', 's_inf']


class TranslationAdmin(admin.ModelAdmin):
    list_display = ['gloss', 'id', 'entry_id', 'sense_num', 'translation_num', 'lang', 'g_gend', 'g_type']

class ExampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'example_id', 'english', 'japanese', 'break_down']


admin.site.register(Entry, EntryAdmin)
admin.site.register(Kanji, KanjiAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Sense, SenseAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(Example, ExampleAdmin)
