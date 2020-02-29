from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("search", views.search, name='search'),
    path("definition", views.definition, name='definition'),
    path("examples", views.get_examples, name='examples'),
]
