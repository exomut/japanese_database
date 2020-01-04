from django.shortcuts import render

from dictionary.models import Kanji, Reading, Sense, Translation


def index(request):
    search = request.GET.get('search', '')
    kanji_group = []
    if search != '':
        kanji_group = Kanji.objects.filter(keb__contains=search)

    context = {'search': search, 'kanji_group': kanji_group}
    return render(request, 'dictionary/search.html', context)
