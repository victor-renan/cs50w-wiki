import re
from secrets import choice
import markdown2
import random

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from . import util


def search_index(request, item_list, querry):
    regex = re.compile(f".*{querry}", re.IGNORECASE)
    if querry:
        if querry in item_list:
            return render(request, "encyclopedia/entry.html", {
                "entry_title": querry,
                "entry": markdown2.markdown(util.get_entry(querry))
            })
        else:
            item_list = list(filter(regex.match, item_list))
            return render(request, "encyclopedia/index.html", {
                "entries": item_list
            })    

#Index Route (wiki/)
def index(request):
    entries = util.list_entries()
    search = search_index(request, entries, request.GET.get('q'))
    
    if search:
        return search
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "random_entry": random.choice(entries)
        })    

#Entries Route (wiki/<entry_title>)
def entry(request, entry_title):
    entries = util.list_entries()
    search = search_index(request, entries, request.GET.get('q'))

    if search:
        return search
    
    else:
        #Regex for wikipages
        wiki_pattern = re.compile(".*wiki:")
        if wiki_pattern.match(entry_title):
            return wikipage(request, re.sub(wiki_pattern, "", entry_title))
        else:
            return render(request, "encyclopedia/entry.html", {
                "entry_title": entry_title,
                "entry": markdown2.markdown(util.get_entry(entry_title))
            })


def wikipage(request, page):
    #pages from "encyclopedia/templates/encyclopedia/"
    wiki_pages = {
        "create_new_page": create_new_page(request)
    }
    if page in wiki_pages:
        return wiki_pages[page]
    else:
        return HttpResponse(f'The page \"{page}\" does not exist.')


def create_new_page(request):
    existing_page_error = None

    if request.method == "POST":
        entry_title = request.POST['entry_title'].strip()
        entry_content = request.POST['entry_content'].strip()

        entries = util.list_entries()

        if entry_title in entries:
            existing_page_error = f'The page "{entry_title}" already exists'
        else:
            util.save_entry(entry_title, entry_content)
            return HttpResponseRedirect(reverse('index'))


    return render(request, "encyclopedia/create_new_page.html", {
        "existing_page_error": existing_page_error
    })


def wikioption(request, entry_title, wikioption):
    wiki_options = {
        "edit_page": edit_page(request, entry_title)
    }
    if wikioption in wiki_options:
        return wiki_options[wikioption]
    else:
        return HttpResponse(f'The wiki do not have an option with the name "{wikioption}".')


def edit_page(request, entry_title):
    if request.method == "POST":
        entry_content = request.POST['entry_content']
        entry_content = entry_content.replace("\n", "")

        util.save_entry(entry_title, entry_content)
        return HttpResponseRedirect(reverse('entry', args={entry_title}))

    return render(request, "encyclopedia/edit_page.html", {
        "entry_title": entry_title,
        "entry_content": util.get_entry(entry_title)
    })