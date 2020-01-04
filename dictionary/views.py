from django.shortcuts import render
from django.http import JsonResponse

from dictionary.models import Kanji, Reading, Sense, Translation


def search(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        kanji_group = [{'keb': k.keb, 'entry_id': k.entry_id}
                       for k in Kanji.objects.filter(keb__contains=query)[:5]]
        json = {'entries': kanji_group}

        return JsonResponse(json)


def definition(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        readings = [r.reb for r in Reading.objects.filter(entry_id=query)]

        json = {'entries': readings}

        return JsonResponse(json)



def index(request):
    return render(request, 'dictionary/search.html')
