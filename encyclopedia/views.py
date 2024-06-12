from django.shortcuts import render
import markdown2
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryPage(request, title):
    try:
        content = markdown2.markdown(util.get_entry(title))
    except TypeError:
        content = "<h1>Error</h1><p>The requested page was not found.</p>"
    return render(request, "encyclopedia/entryPage.html", {"title":title.capitalize(), "content":content})