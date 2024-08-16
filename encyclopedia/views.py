from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request,"encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


def search(request):
    query = request.GET.get('q', '').lower()
    if query:
        all_entries = util.list_entries()

        for entry in all_entries:
            if query == entry.lower():
                return redirect('entry', title=entry)
            
        matching_entries = [entry for entry in all_entries if query in entry.lower()]

        return render(request, "encyclopedia/search.html", {
            "entries": matching_entries,
            "query": query
        })
    
    return render(request, "encyclopedia/search.html", {
        "entries": [],
        "query": query
    })