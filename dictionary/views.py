from django.shortcuts import render
from django.http import JsonResponse

from dictionary.models import Entry


def search(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')

        kanji_group = []
        for entry in Entry.objects.filter(kanji__keb__contains=query)[:10]:
            for kanji in entry.kanji_set.all():
                kanji_group.append({'keb': kanji.keb, 'entry_id': entry.id})

        json = {'entries': kanji_group}

        return JsonResponse(json)


def definition(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        readings = [r.reb for r in Entry.objects.filter(id=query)]

        json = {'entries': readings}

        return JsonResponse(json)


def index(request):
    return render(request, 'dictionary/search.html')
