from django.shortcuts import render
from .forms import capteurform, capteurformupdate
from . import models
from django.http import HttpResponseRedirect
import random, pandas as pd, matplotlib.pyplot as plt, datetime
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
    capteur = models.capteur.objects.get(pk = id)
    return render(request, "partieweb/affiche.html", {'capteur':capteur})

def update(request, id):
    capteur = models.capteur.objects.get(pk=id)
    form = capteurformupdate(capteur.dic())
    temp = models.capteur.objects.get(pk=id)
    temp.nom = f"{capteur.nom[0:10]} mise à jour échouée {random.randint(0, 99)}"
    temp.save()
    return render(request, "partieweb/update.html", {"form":form, "id":id})

def updatetraitement(request, id):
    form = capteurformupdate(request.POST)
    saveid = id
    piece = models.capteur.objects.get(pk=id).piece
    if form.is_valid():
        capteur = form.save(commit = False)
        capteur.id = saveid
        capteur.piece = piece
        capteur.save()
        return HttpResponseRedirect("/partieweb/")
    else:
        return HttpResponseRedirect(f"/partieweb/update/{saveid}/")

def delete(request, id):
    suppr = models.capteur.objects.get(pk=id)
    suppr.delete()
    suppr2 = models.donnees.objects.filter(capteur_id=id)
    suppr2.delete()
    return HttpResponseRedirect("/partieweb/")

def donnees_all(request):
    qs = models.donnees.objects.all()
    return render(request, 'partieweb/donnees_all.html', {'queryset':qs})
def donnees_all_filtrees(request):
    qs = models.donnees.objects.all()
    nom_query = request.GET.get('name')
    date_min_query = request.GET.get('date_min')
    date_max_query = request.GET.get('date_max')
    id_query = request.GET.get('id')
    if nom_query != '' and nom_query is not None:
        if models.capteur.objects.filter(nom__icontains=nom_query).exists():
            qs=qs.filter(capteur=models.capteur.objects.get(nom__icontains=nom_query))
        else:
            nom_query += " (n'existe pas, filtre ignoré)"
    if date_min_query != '' and date_min_query is not None:
        qs = qs.filter(timestamp__gte=date_min_query)
    if date_max_query != '' and date_max_query is not None:
        qs = qs.filter(timestamp__lte=date_max_query)
    if id_query != '' and id_query is not None:
        qs = qs.filter(capteur_id=id_query)
    context = {
        'queryset':qs,
        'nom_query':nom_query,
        'date_min_query':date_min_query,
        'date_max_query':date_max_query,
        'id_query':id_query,
    }
    return render(request, 'partieweb/donnees_all.html', context)

def donnees(request, id):
    qs = models.donnees.objects.filter(capteur_id=id).order_by("timestamp")
    return render(request, "partieweb/donnees.html", {'queryset': qs, 'id':id})

def donnees_filtrees(request, id):
    qs = models.donnees.objects.filter(capteur_id=id).order_by("timestamp")
    date_min_query = request.GET.get('date_min')
    date_max_query = request.GET.get('date_max')
    if date_min_query != '' and date_min_query is not None:
        qs = qs.filter(timestamp__gte=date_min_query)
    if date_max_query != '' and date_max_query is not None:
        qs = qs.filter(timestamp__lte=date_max_query)
    context = {
        'queryset': qs,
        'date_min_query': date_min_query,
        'date_max_query': date_max_query,
        'id':id,
    }
    return render(request, "partieweb/donnees.html", context)

def deletedonnee(request, id):
    suppr = models.donnees.objects.get(pk=id)
    idcapteur = suppr.capteur_id
    suppr.delete()
    return HttpResponseRedirect(f"/partieweb/donnees/{idcapteur}/")

def deletedonnee_2(request, id):
    suppr = models.donnees.objects.get(pk=id)
    suppr.delete()
    return HttpResponseRedirect(f"/partieweb/donnees_all/")


def deleteall(request, id):
    if id != "0":
        suppr = models.donnees.objects.filter(capteur_id=id)
        suppr.delete()
        return HttpResponseRedirect(f"/partieweb/donnees/{id}/")
    else:
        suppr = models.donnees.objects.all()
        suppr.delete()
        return HttpResponseRedirect("/partieweb/donnees_all/")

def ajoutdonnees(request, id): # id, piece, date, heure, temp
    donnees = models.temp.objects.all()
    for data in donnees:
        data = str(data).split("(")[1].replace(")", "").split("_")
        heure =  data[3].split(".")
        heure = f"{heure[0]}:{heure[1]}:{heure[2]}"
        timestamp = f"{data[2]} {heure}"
        if models.capteur.objects.filter(pk=data[0]).exists(  ):
            capteur = models.capteur.objects.get(pk=data[0])
        else:
            capteur = models.capteur.objects.create(id=data[0], nom=f'Capteur {data[1]} {data[0][0]}{data[0][1]}{data[0][2]}', piece=data[1], emplacement='Non spécifié')
        donnees = models.donnees.objects.create(capteur=capteur, timestamp=timestamp, temp=data[4])
    models.temp.objects.all().delete()
    if id == "0":
        return HttpResponseRedirect("/partieweb/")
    elif id == "1":
        return HttpResponseRedirect(f"/partieweb/donnees_all/")
    else:
        return HttpResponseRedirect(f"/partieweb/donnees/{id}/")

