from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from dictionary.models import Entry, Kanji, Reading


def search(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')

        kanji_group = []
        # SQLite does not support calling distinct directly
        for entry in Entry.objects.filter(
                Q(kanji__keb__contains=query) | Q(reading__reb__contains=query) |
                (Q(translation__gloss__contains=query) & Q(translation__lang='eng'))
        ).values('id').distinct()[:10]:

            kanji = Kanji.objects.filter(entry_id=entry['id'])
            if len(kanji) > 0:
                keb = ', '.join(k.keb for k in kanji)
            else:
                keb = ', '.join(r.reb for r in Reading.objects.filter(entry_id=entry['id']))

            kanji_group.append({'keb': keb, 'entry_id': entry['id']})

        json = {'entries': kanji_group}

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
