from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models

class capteurform(ModelForm):
    class Meta:
        model = models.capteur
        fields = ("id", "nom", "piece", "emplacement")
        labels = {
            'id': _('Identifiant du capteur (12 caractères alphanumériques) :'),
            'nom': _('Nom du capteur '),
            'piece': _('Pièce '),
            'emplacement': _('Emplacement du capteur '),
        }

class capteurformupdate(ModelForm):
    class Meta:
        model = models.capteur
        fields = ("nom", "piece", "emplacement")
        labels = {
            'nom': _('Nom du capteur '),
            'piece': _('Pièce '),
            'emplacement': _('Emplacement du capteur '),
        }