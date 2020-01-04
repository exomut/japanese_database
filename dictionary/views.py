from django.shortcuts import render
from django.http import JsonResponse

from dictionary.models import Kanji, Reading, Sense, Translation


def search(request):
    if request.POST.get('action') == 'post':
        kanji_group = [k.keb for k in Kanji.objects.filter(keb__contains=request.POST.get('query'))[:5]]
        json = {'entries': kanji_group}
        return JsonResponse(json)


def index(request):
    return render(request, 'dictionary/search.html')
