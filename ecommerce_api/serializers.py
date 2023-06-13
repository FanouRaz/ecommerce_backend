from rest_framework import serializers

from .models import *

class UtilisateurSerializer(serializers.Serializer):
    class Meta:
        model = Utilisateur
        fields = "__all__"

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