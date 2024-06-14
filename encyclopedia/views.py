from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import util
import markdown2, random

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
            
def newPage(request):
    if request.method == 'POST':
        title = request.POST.get("Title").strip().lower()
        if title in [entry.lower() for entry in util.list_entries()]:
            return render(request, "encyclopedia/errorPage.html", {"errorContent":"A page with this title already exists."})
        else:
            title = request.POST.get("Title").strip().capitalize()
            fileName = f"entries/{title}.md"
            default_storage.save(fileName, ContentFile(request.POST.get("Content")))
            return redirect('entryPage', title=title)
    return render(request, "encyclopedia/newPage.html")

def editPage(request, title):
    entry = util.get_entry(title)
    if entry:
        if request.method == 'POST':
            fileName = f"entries/{title}.md"
            with open(fileName, 'w') as file:
                file.write(request.POST.get("Content"))
            return redirect('entryPage', title=title)
        else:
            return render(request, "encyclopedia/editPage.html", {"title":title.capitalize(), "content": util.get_entry(title)})
    else:
        return render(request, "encyclopedia/errorPage.html", {"errorContent": notFound})

def randomPage(request):
    title = random.choice(util.list_entries())
    return redirect('entryPage', title=title)