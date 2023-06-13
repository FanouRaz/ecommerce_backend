from rest_framework import serializers

from .models import Utilisateur,Panier,Produit,Payement,Livraison,Achat,Notification,Evaluation,Commande,Session

class UtilisateurSerializer(serializers.Serializer):
    id_utilisateur = serializers.IntegerField()
    nom_utilisateur = serializers.CharField(max_length=50)
    prenom_utilisateur = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)
    role = serializers.CharField(max_length=30)
    #password = serializers.CharField(max_length=100)
   
    def create(self, validated_data):
        return Utilisateur.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nom_utilisateur = validated_data.get('nom_utilisateur', instance.nom_utilisateur)
        instance.prenom_utilisateur = validated_data.get('prenom_utilisateur', instance.prenom_utilisateur)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        #instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
    
class ProduitSerializer(serializers.Serializer):
    class Meta:
        model = Produit
        fields = '__all__'
    
class PanierSerializer(serializers.Serializer):
    class Meta:
        model = Panier
        fields = '__all__'
        
class CommandeSerializer(serializers.Serializer):
    class Meta:
        model = Commande
        fields = '__all__'

class LivraisonSerializer(serializers.Serializer):
    class Meta:
        model = Livraison
        fields = '__all__'

class NotificationSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = '__all__'

class EvaluationSerializer(serializers.Serializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class PayementSerializer(serializers.Serializer):
    class Meta:
        model = Payement
        fields = '__all__'
                
class AchatSerializer(serializers.Serializer):
    class Meta:
        model = Achat
        fields = '__all__'
        
class SessionSerializer(serializers.Serializer):
    class Meta:
        model = Session
        fields = '__all__' 