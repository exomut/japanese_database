from functools import lru_cache
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q


from dictionary.models import Entry, Kanji, Reading, Translation, Example, Setting


def search(request):
    if request.POST.get('action') == 'post':
        limit = 50
        query = request.POST.get('query')
        pos = int(request.POST.get('pos'))
        type = request.POST.get('type')

        kanji_group = []

        for entry in get_entries(query, pos, limit, type=type):

            kanji = Kanji.objects.filter(entry_id=entry['id'])[:1]
            keb = kanji[0].keb if len(kanji) > 0 else ''

            readings = Reading.objects.filter(entry_id=entry['id'])[:1]
            reb = readings[0].reb if len(readings) > 0 else ''

            translations = Translation.objects.filter(lang='eng').filter(entry_id=entry['id'])[:1]
            trans = translations[0].gloss if len(translations) > 0 else ''

            kanji_group.append({'keb': keb, 'reb': reb, 'trans': trans, 'entry_id': entry['id']})

        count = len(kanji_group)
        json = {'pos': pos+count, 'entries': kanji_group, 'limit': limit}

        return JsonResponse(json)


def definition(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        entry = Entry.objects.get(id=query)

        readings = [r.reb for r in entry.reading_set.all()]
        kanji = [k.keb for k in entry.kanji_set.all()]
        translations = [t.gloss for t in entry.translation_set.filter(lang='eng')]
        pos = [p.pos for p in entry.sense_set.all()]

        search = kanji[0] if len(kanji) > 0 else readings[0]
        examples = get_examples(search)
        json = {'reb': readings, 'keb': kanji, 'trans': translations, 'pos': pos, 'examples': examples}

        return JsonResponse(json)


def get_examples(word: str):
    examples = []

    reg_ex_pre = r'([ ]|^)'
    reg_ex_suf = r'([\[({]|$)'

    reg_ex = f'{reg_ex_pre}{word}{reg_ex_suf}'

    for example in Example.objects.filter(break_down__regex=reg_ex)[:10]:
        examples.append(
            {
                'english': example.english,
                'japanese': example.japanese,
                'break_down': example.break_down
            }
        )

    return examples


def index(request):

    try:
        stats = Setting.objects.get(name='stats').value
    except Setting.DoesNotExist:
        stats = ''

    return render(request, 'dictionary/search.html', {'stats': stats})


@lru_cache(maxsize=10000)
def get_entries(query: str, pos: int, limit: int, type: str = 'st-equa', lang: str = 'eng'):
    entries = []

    if type == "st-cont":
        entries = search_contains(query, pos, limit, lang)
    elif type == "st-staw":
        entries = search_start_with(query, pos, limit, lang)
    elif type == "st-endw":
        entries = search_ends_with(query, pos, limit, lang)
    elif type == "st-equa":
        entries = search_equals(query, pos, limit, lang)

    return entries


def search_contains(query: str, pos: int, limit: int, lang: str = 'eng'):
    # SQLite does not support calling distinct directly
    return Entry.objects.filter(
        Q(kanji__keb__contains=query) | Q(reading__reb__contains=query) |
        (Q(translation__gloss__icontains=query) & Q(translation__lang=lang))
    ).values('id').distinct()[pos:pos + limit]


def search_equals(query: str, pos: int, limit: int, lang: str = 'eng'):
    # SQLite does not support calling distinct directly
    # Include searching for verbs in English using 'to '
    return Entry.objects.filter(
        Q(kanji__keb__exact=query) | Q(reading__reb__exact=query) |
        ((Q(translation__gloss__iexact=f'to {query}') | Q(translation__gloss__iexact=query)) & Q(translation__lang=lang))
    ).values('id').distinct()[pos:pos + limit]


def search_start_with(query: str, pos: int, limit: int, lang: str = 'eng'):
    # SQLite does not support calling distinct directly
    return Entry.objects.filter(
        Q(kanji__keb__startswith=query) | Q(reading__reb__startswith=query) |
        ((Q(translation__gloss__istartswith=f'to {query}') | Q(translation__gloss__istartswith=query)) & Q(translation__lang=lang))
    ).values('id').distinct()[pos:pos + limit]


def search_ends_with(query: str, pos: int, limit: int, lang: str = 'eng'):
    # SQLite does not support calling distinct directly
    q = Entry.objects.filter(
        Q(kanji__keb__endswith=query) | Q(reading__reb__endswith=query) |
        (Q(translation__gloss__iendswith=query) & Q(translation__lang=lang))
    ).values('id').distinct()[pos:pos + limit]
    print(f"Query: {q.query}")
    return q
