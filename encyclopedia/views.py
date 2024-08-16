from django.shortcuts import render, redirect
from django.http import Http404
import random
import markdown2

from . import util

import markdown2

def convert_markdown_to_html(markdown_content):

    html_content = markdown2.markdown(markdown_content)
    return html_content



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


def create(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        
        util.save_entry(title, content)
        
        return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        updated_content = request.POST.get("content")
        util.save_entry(title, updated_content)
        return redirect('entry', title=title)
    
    content = util.get_entry(title)
    if content is None:
        raise Http404("The requested page was not found.")
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
    
def random_page(request):
    entries = util.list_entries()

    random_entry = random.choice(entries)

    return redirect('entry', title=random_entry) 