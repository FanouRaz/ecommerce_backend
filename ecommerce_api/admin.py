from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Produit)
admin.site.register(Notification)
admin.site.register(Commande)
admin.site.register(Panier)
admin.site.register(Livraison)
admin.site.register(Evaluation)
admin.site.register(Session)
admin.site.register(Payement)
admin.site.register(Achat)