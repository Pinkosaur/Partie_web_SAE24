from django.shortcuts import render
from .forms import capteurform
from . import models
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    liste = models.capteur.objects.all()
    return render(request, "partieweb/index.html", {"liste":liste})

def ajout(request):
    form = capteurform()
    return render(request, "partieweb/ajout.html", {"form":form})

def traitement(request):
    form = capteurform(request.POST)
    if form.is_valid():
        capteur = form.save()
        return render(request, "partieweb/affiche.html", {"capteur":capteur})
    else:
        return render(request, "partieweb/ajout.html", {"form":form})

def affiche(request, id):
    capteur = models.capteur.get(pk = id)
    return render(request, "partieweb/affiche.html", {'capteur':capteur})

def update(request, id):
    capteur = models.capteur.objects.get(pk=id)
    form = capteurform(capteur.dic())
    return render(request, "partieweb/update.html", {"form":form, "id":id})

def updatetraitement(request, id):
    form = capteurform(request.POST)
    saveid = id
    if form.is_valid():
        capteur = form.save(commit = False)
        capteur.id = saveid
        capteur.save()
        return HttpResponseRedirect("/partieweb/")
    else:
        return render(request, "partieweb/update.html", {"form": form})

def delete(request, id):
    suppr = models.capteur.objects.get(pk=id)
    suppr.delete()
    return HttpResponseRedirect("/partieweb/")

def donnees(request, id):
    liste = models.donnees.objects.filter(capteur_id=id)
    return render(request, "partieweb/donnees.html", {"liste": liste})

def deletedonnee(request, id):
    suppr = models.donnees.objects.get(pk=id)
    idcapteur = suppr.capteur_id
    suppr.delete()
    HttpResponseRedirect(f"/partieweb/donnees/{idcapteur}/")

def ajoutdonnees(data):
    data = data.split(',')
    id = data[0].split('=')[1]
    piece = data[1].split('=')[1]
    date = data[2].split('=')[1]
    heure = data[3].split('=')[1]
    temp = data[4].split('=')[1]
    if models.capteur.objects.filter(piece=piece).exists():
        capteur = models.capteur.objects.get(piece=piece)
    else:
        capteur = models.capteur.objects.create(id=id, nom='Nouveau capteur', piece=piece, emplacement='Inconnu')
    donnees = models.donnees.objects.create(capteur=capteur, piece=piece, date=date, heure=heure, temp=temp)
    return "ok"