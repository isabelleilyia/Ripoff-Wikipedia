from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse

from . import util
from django import forms
from random import randint

import markdown2

query = ""
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def results(request):
    global query
    entries = util.list_entries()
    searchResults = []
    for i in range(len(entries)):
        if query.lower() in entries[i].lower():
            searchResults.append(entries[i])
    
    return render(request, "encyclopedia/results.html", {
        "results": searchResults
    })

def page(request, name):
    if request.method== "POST":
        global query
        found = False
        query=request.POST.get('q')
        entries=util.list_entries()
        for i in range(len(entries)):
            entries[i] = entries[i].lower()
            if query.lower() == entries[i]:
                name = query
                found = True
        if not found:
            return redirect(reverse(results))
    page = util.get_entry(name)
    
    if page:
        page = markdown2.markdown(page)
        return render(request, "encyclopedia/page.html", {
            "title": name,
            "text": page
        })
        
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "The requested page was not found."
        })

def create_page(request):
    if request.method=="GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST.get('title')
        body = request.POST.get('content')
        entries=util.list_entries()
        for i in range(len(entries)):
            entries[i] = entries[i].lower()
            if title.lower() == entries[i]:
                return render(request,"encyclopedia/error.html", {
                    "error": "A Wiki page with this title already exists!"
                })
        util.save_entry(title,body)
        return redirect(f"/wiki/{title}")

def edit_page(request):
    if request.method=="GET":
        title = request.GET.get('title')
        entries=util.list_entries()
        for i in range(len(entries)):
            entries[i] = entries[i].lower()
            if title.lower() == entries[i]:       
                return render(request, "encyclopedia/edit.html", {
                    "content": util.get_entry(title),
                    "title": title
                })
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title,content)
        return redirect(f"/wiki/{title}")

def random_entry(request):
    entries=util.list_entries()
    num = randint(0, len(entries)-1)
    title = entries[num]
    page = util.get_entry(title)
    page = markdown2.markdown(page)
    if page:
        return redirect(f"/wiki/{title}")

def wiki(request):
    return redirect("/wiki")