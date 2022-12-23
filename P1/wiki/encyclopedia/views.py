# Paused after completing Index Page - Continue from Search - https://cs50.harvard.edu/web/2020/projects/1/wiki/

from django import forms
from django.shortcuts import render, redirect
from markdown2 import Markdown
from random import choice

from . import util


markdowner = Markdown()

# Convert from Markdown to HTML
def md_to_html(title):
    details = util.get_entry(title)
    if not details:
        return None
    else:
        return markdowner.convert(details)

# Home Page with list of all Wiki Entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

# Individual Page
def page(request, title):
    details = md_to_html(title)

    if not details:
        return render(request, "encyclopedia/empty.html")

    return render(request, "encyclopedia/wikipage.html", {
        "title": title,
        "page": details
    })

# Search Bar to look for substrings / full pages
def search(request):
    # This route is used by the Random Page option to redirect to the page route with a random title.
    if request.method == "GET":
        entries = util.list_entries()
        entry = choice(entries)
        return redirect(page, title=entry)

    # This route is used when inputting a search query
    elif request.method == "POST":
        entries = util.list_entries()
        search_page = request.POST['q']
        details = md_to_html(search_page)
        if details:
            return render(request, "encyclopedia/wikipage.html", {
            "title": search_page,
            "page": details
        })
            
        else:
            newlist = []
            for entry in entries:
                if search_page.lower() in entry.lower():
                    newlist.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": newlist
                })

# Route to edit / create new pages - Enabled by flags from newpage.html and edit.html for different functionality           
def new_page(request):
    if request.method == "POST":
        entries = util.list_entries()
        title = request.POST['page_title']
        flag = request.POST['page_flag']
        details = request.POST['page_details']
        # Flagged for edit allows overwriting existing wiki pages
        if flag == "edit":
            util.save_entry(title, details)
            return redirect(page, title=title)
        
        # If arriving from the newpage.html page, prevent overwriting an article
        for entry in entries:
            if title in entry:
                return render(request, "encyclopedia/error.html")
        
    return render(request, "encyclopedia/newpage.html")

# Route to edit page where markdown is already present in a textarea box
def edit_page(request, title):
    if request.method == "POST":
        details = request.POST['page_title']
        content = util.get_entry(details)
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "page": content
    })