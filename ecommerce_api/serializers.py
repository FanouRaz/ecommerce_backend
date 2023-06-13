from rest_framework import serializers

from .models import Utilisateur,Panier,Produit,Payement,Livraison,Achat,Notification,Evaluation,Commande,Session

class UtilisateurSerializer(serializers.ModelSerializer):
   class Meta:
       model = Utilisateur
       exclude = ['password']
           
class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'
    
class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'
    """ produits = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(), many=True)

    def create(self, validated_data):
        produits_data = validated_data.pop('produits')
        panier = Panier.objects.create(**validated_data)
        panier.produits.set(produits_data)
        return panier

    def update(self, instance, validated_data):
        instance.utilisateur = validated_data.get('utilisateur', instance.utilisateur)
        instance.quantite = validated_data.get('quantite', instance.quantite)
        produits_data = validated_data.get('produits', [])
        instance.produits.set(produits_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = {
            'id_panier': instance.id_panier,
            'utilisateur': instance.utilisateur.id,
            'produits': [produit.id for produit in instance.produits.all()],
            'quantite': instance.quantite
        }
        
        return representation
 """
       
class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class LivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livraison
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class PayementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payement
        fields = '__all__'
                
class AchatSerializer(serializers.Serializer):
    class Meta:
        model = Achat
        fields = '__all__'
        
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__' 