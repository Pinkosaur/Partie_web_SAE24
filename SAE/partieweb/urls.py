from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ajout/', views.ajout),
    path('traitement', views.traitement),
    path('affiche/<str:id>/', views.affiche),
    path('update/<str:id>/', views.update),
    path('updatetraitement/<str:id>/', views.updatetraitement),
    path('delete/<str:id>/', views.delete),
    path('donnees/<str:id>/', views.donnees),
    path('donnees_filtrees/<str:id>/', views.donnees_filtrees),
    path('deletedonnee/<int:id>/', views.deletedonnee),
    path('deletedonnee_2/<int:id>/', views.deletedonnee_2),
    path('ajoutdonnees/<str:id>/', views.ajoutdonnees),
    path('deleteall/<str:id>/', views.deleteall),
    path('donnees_all/', views.donnees_all),
    path('donnees_all_filtrees/', views.donnees_all_filtrees),
 ]