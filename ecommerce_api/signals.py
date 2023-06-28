from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Utilisateur, Panier

#Crée un panier lorsqu'on crée un nouvel utilisateur
@receiver(post_save, sender=Utilisateur)
def createPanier(sender, instance, created, **kwargs):
    if created:
        Panier.objects.create(utilisateur=instance)