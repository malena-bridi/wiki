from django.shortcuts import render
import markdown2
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request, title):
    return render(request, "encyclopedia/entryPage.html", {"title":title.capitalize})