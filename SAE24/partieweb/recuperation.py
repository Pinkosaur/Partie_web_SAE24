import os, json
from . import views
from django.http import HttpResponseRedirect
def recuperation(data):
    repertoire = 'partieweb/messages/'
    for file in os.listdir(repertoire):
        with open(os.path.join(repertoire, file), 'r') as f:
            data = json.load(f)
        views.ajoutdonnees(data)
        os.remove(os.path.join(repertoire, file))
    return HttpResponseRedirect("/partieweb/")
