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
    return render(request, "partieweb/donnees.html", {"liste": liste, "id":id})

def deletedonnee(request, id):
    suppr = models.donnees.objects.get(pk=id)
    idcapteur = suppr.capteur_id
    suppr.delete()
    liste = models.donnees.objects.filter(capteur_id=idcapteur)
    return render(request, "partieweb/donnees.html", {"liste": liste})

def deleteall(request, id):
    suppr = models.donnees.objects.filter(capteur_id=id)
    suppr.delete()
    return render(request, "partieweb/donnees.html")
def ajoutdonnees(data): # id, piece, date, heure, temp
    date = data[2].split("/")
    date = f"{date[2]}-{date[1]}-{date[0]}"
    heure =  data[3].split("-")
    heure = f"{heure[0]}:{heure[1]}:{heure[2]}"
    timestamp = f"{date} {heure}"
    if models.capteur.objects.filter(pk=data[0]).exists():
        capteur = models.capteur.objects.get(pk=data[0])
    else:
        capteur = models.capteur.objects.create(id=data[0], nom=f'Capteur {data[1]} {data[0][0]}{data[0][1]}{data[0][2]}', piece=data[1], emplacement='Inconnu')
    donnees = models.donnees.objects.create(capteur=capteur, timestamp=timestamp, temp=data[4])
    return "ok"