from django.shortcuts import render
from django.http import JsonResponse

from dictionary.models import Entry, Kanji


def search(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')

        kanji_group = []
        # SQLite does not support calling distinct directly
        for entry in Entry.objects.filter(kanji__keb__contains=query).values('id').distinct()[:10]:
            keb = ", ".join([kanji.keb for kanji in Kanji.objects.filter(entry_id=entry['id'])])
            kanji_group.append({'keb': keb, 'entry_id': entry['id']})

        json = {'entries': kanji_group}

        return JsonResponse(json)


def definition(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        entry = Entry.objects.get(id=query)
        kanji = ', '.join([k.keb for k in entry.kanji_set.all()])
        readings = ', '.join([r.reb for r in entry.reading_set.all()])
        translations = ', '.join([t.gloss for t in entry.translation_set.filter(lang='eng')])

        json = {'reb': readings, 'keb': kanji, 'trans': translations}

        return JsonResponse(json)


def index(request):
    return render(request, 'dictionary/search.html')
