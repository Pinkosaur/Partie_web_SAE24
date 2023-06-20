from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('ajout/', views.ajout),
    path('traitement', views.traitement),
    path('affiche/<int:id>/', views.affiche),
    path('update/<int:id>/', views.update),
    path('updatetraitement<int:id>/', views.updatetraitement),
    path('delete/<int:id>/', views.delete),
    ]