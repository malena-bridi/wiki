from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entryPage, name="entryPage"),
    path("search/", views.search, name="search"),
    path("newPage/", views.newPage, name="newPage"),
    path("wiki/<str:title>/edit/", views.editPage, name="editPage"),
    path("random/", views.randomPage, name="random")
]