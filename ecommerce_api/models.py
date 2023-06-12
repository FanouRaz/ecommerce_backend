from django.db import models

# Create your models here.
class Utilisateur(models.Model):
    id_utilisateur = models.IntegerField(primary_key=True)
    nom_utilisateur = models.CharField(max_length=50)
    prenom_utilisateur = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.TextChoices("admin","simple utilisateur")
    
class Produit(models.Model):
    id_produit = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=100)
    quantite_stock = models.IntegerField()
    seuil_minimal = models.IntegerField()
    categorie = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    prix = models.IntegerField()

class Panier(models.Model):
    id_panier = models.IntegerField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit)
    quantite = models.IntegerField()

class Commande(models.Model):
    id_commande = models.IntegerField(primary_key=True)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    produit = models.ManyToManyField(Produit)
    date_commande = models.DateField()
    date_livraison = models.DateField()
    status_annulation = models.BooleanField()
    date_annulation = models.DateField()
    quantite = models.IntegerField()

class Notification(models.Model):
    id_notification = models.IntegerField(primary_key=True)
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_notification = models.DateField()        
    message = models.CharField(max_length=100)
    
class Evaluation(models.Model):
    id_evaluation = models.IntegerField(primary_key=True)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit)
    note = models.IntegerField()
    

class Livraison(models.Model):
    id_livraison = models.IntegerField(primary_key=True)
    id_commande = models.OneToOneField(Commande, on_delete = models.CASCADE)
    lieu = models.CharField(max_length=100)
    
class Achat(models.Model):
    id_achat = models.IntegerField(primary_key=True)
    commande = models.OneToOneField(Commande, on_delete = models.CASCADE)

class Session(models.Model):
    id_session = models.IntegerField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    date_connexion = models.DateField()
    date_deconnexion = models.DateField()   

class Payement(models.Model):
    id_payement = models.IntegerField(primary_key=True)
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    montant = models.IntegerField()
    