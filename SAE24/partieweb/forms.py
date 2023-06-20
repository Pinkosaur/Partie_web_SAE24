from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models

class capteurform(ModelForm):
    class Meta:
        model = models.capteur
        fields = ("nom", "piece", "emplacement")
        labels = {
            'nom': _('Nom du capteur '),
            'piece': _('Pièce '),
            'emplacement': _('Emplacement du capteur '),
        }