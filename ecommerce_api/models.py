from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom_utilisateur, prenom_utilisateur, password=None):
        if not email:
            raise ValueError("L'email est obligatoire.")

        user = self.model(
            email=self.normalize_email(email),
            nom_utilisateur=nom_utilisateur,
            prenom_utilisateur=prenom_utilisateur,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom_utilisateur, prenom_utilisateur, password=None):
        user = self.create_user(email, nom_utilisateur, prenom_utilisateur, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    nom_utilisateur = models.CharField(max_length=50)
    prenom_utilisateur = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=30, default="simple_utilisateur")
    profilePicture = models.ImageField(upload_to="uploads/user/", default="uploads/user/user_placeholder.jpeg")
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_utilisateur', 'prenom_utilisateur']

    objects = UtilisateurManager()

    def get_full_name(self):
        return f"{self.prenom_utilisateur} {self.nom_utilisateur}"

    def get_short_name(self):
        return self.prenom_utilisateur

    def __str__(self):
        return self.email

class Produit(models.Model):
    id_produit = models.AutoField(primary_key=True)
    id_utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    quantite_stock = models.IntegerField()
    seuil_minimal = models.IntegerField()
    categorie = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.CharField(max_length=200,null=True)
    prix = models.IntegerField()
    pathImg = models.ImageField(upload_to="uploads/products/",default="uploads/products/logo.png")
    
class Panier(models.Model):
    id_panier = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit,blank=True)

class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    produit = models.ManyToManyField(Produit,blank=True)
    date_commande = models.DateField(auto_now_add=True)
    date_livraison = models.DateField()
    status_annulation = models.BooleanField()
    date_annulation = models.DateField()
    
class DetailCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

class Notification(models.Model):
    id_notification = models.AutoField(primary_key=True)
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_notification = models.DateField()        
    message = models.CharField(max_length=100)
    
class Evaluation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE,null=True)
    note = models.IntegerField()
    commentaire = models.TextField(blank=True)

    class Meta:
        unique_together = ['utilisateur', 'produit']
    

class Livraison(models.Model):
    id_livraison = models.AutoField(primary_key=True)
    id_commande = models.OneToOneField(Commande, on_delete = models.CASCADE)
    lieu = models.CharField(max_length=100)
    
class Achat(models.Model):
    id_achat = models.AutoField(primary_key=True)
    commande = models.OneToOneField(Commande, on_delete = models.CASCADE)

class Session(models.Model):
    id_session = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    date_connexion = models.DateField()
    date_deconnexion = models.DateField()   

class Payement(models.Model):
    id_payement = models.AutoField(primary_key=True)
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    montant = models.IntegerField()
    