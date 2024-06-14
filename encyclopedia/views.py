from django.shortcuts import render, redirect
from . import util
import markdown2, random

from django.http import HttpResponse

notFound = "The requested page was not found."

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "header": "All Pages"
    })

def entryPage(request, title):
    try:
        content = markdown2.markdown(util.get_entry(title))
    except TypeError:
        return render(request, "encyclopedia/errorPage.html", {"errorContent":notFound})
    return render(request, "encyclopedia/entryPage.html", {"title":title.capitalize(), "content":content})

def search(request):
    if request.method == 'GET':
        query = request.GET.get("q")
        entry = util.get_entry(query)
        if entry:
            return redirect('entryPage', title=query)
        else:
            matching_entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            if matching_entries:
                return render(request, "encyclopedia/index.html", {"entries": matching_entries, "header": "Search Results"})
            else:
                return render(request, "encyclopedia/errorPage.html", {"errorContent":notFound})
            
def newEntry(request):
    if request.method == 'POST':
        title = request.POST.get("Title").strip().lower()
        if title in [entry.lower() for entry in util.list_entries()]:
            return render(request, "encyclopedia/errorPage.html", {"errorContent":"A page with this title already exists."})
        else:
            fileName = f"entries/{title}.md"
            with open(fileName, 'w') as file:
                file.write(request.POST.get("Content"))
            return redirect('entryPage', title=title)
    return render(request, "encyclopedia/newEntry.html")

def editEntry(request, title):
    entry = util.get_entry(title)
    if entry:
        if request.method == 'POST':
            fileName = f"entries/{title}.md"
            with open(fileName, 'w') as file:
                file.write(request.POST.get("Content"))
            return redirect('entryPage', title=title)
        else:
            return render(request, "encyclopedia/editEntry.html", {"title":title.capitalize(), "content": util.get_entry(title)})
    else:
        return render(request, "encyclopedia/errorPage.html", {"errorContent": notFound})

def randomPage(request):
    title = random.choice(util.list_entries())
    return redirect('entryPage', title=title)