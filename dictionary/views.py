from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from dictionary.models import Entry, Kanji, Reading


def search(request):
    if request.POST.get('action') == 'post':
        limit = 50
        query = request.POST.get('query')
        pos = int(request.POST.get('pos'))

        kanji_group = []

        entries = search_contains(query, pos, limit)

        for entry in entries:

            kanji = Kanji.objects.filter(entry_id=entry['id'])
            if len(kanji) > 0:
                keb = ', '.join(k.keb for k in kanji)
            else:
                keb = ', '.join(r.reb for r in Reading.objects.filter(entry_id=entry['id']))

            kanji_group.append({'keb': keb, 'entry_id': entry['id']})

        count = len(kanji_group)
        json = {'pos': pos+count, 'entries': kanji_group, 'limit': limit}

        return JsonResponse(json)


def definition(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        entry = Entry.objects.get(id=query)

        readings = ', '.join([r.reb for r in entry.reading_set.all()])
        kanji = ', '.join([k.keb for k in entry.kanji_set.all()]) or readings
        translations = ', '.join([t.gloss for t in entry.translation_set.filter(lang='eng')])

        json = {'reb': readings, 'keb': kanji, 'trans': translations}

        return JsonResponse(json)


def index(request):
    return render(request, 'dictionary/search.html')


def search_contains(query: str, pos: int, limit: int, lang: str = 'eng'):
    # SQLite does not support calling distinct directly
    return Entry.objects.filter(
        Q(kanji__keb__contains=query) | Q(reading__reb__contains=query) |
        (Q(translation__gloss__contains=query) & Q(translation__lang=lang))
    ).values('id').distinct()[pos:pos + limit]


def search_only(query: str, pos: int, limit: int, lang: str = 'eng'):
    # SQLite does not support calling distinct directly
    return Entry.objects.filter(
        Q(kanji__keb__exact=query) | Q(reading__reb__exact=query) |
        (Q(translation__gloss__exact=query) & Q(translation__lang=lang))
    ).values('id').distinct()[pos:pos + limit]
