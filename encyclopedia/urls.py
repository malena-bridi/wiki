from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entryPage, name="entryPage"),
    path("search/", views.search, name="search"),
    path("newEntry/", views.newEntry, name="newEntry"),
    path("wiki/<str:title>/edit/", views.editEntry, name="editEntry"),
    path("random/", views.randomPage, name="random")
]