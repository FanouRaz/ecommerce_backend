from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *

class UtilisateurSerializer(serializers.ModelSerializer):
   class Meta:
       model = Utilisateur
       exclude = ['password','is_active','is_staff']
           
class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'
    
class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'
       
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
        

""" class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Validate the input data
        self.user = Utilisateur.objects.filter(email=attrs['email']).first()
        if self.user and self.user.check_password(attrs['password']):
            data = super().validate(attrs)
            
            data['id_utilisateur'] = self.user.id_utilisateur
            data['nom_utilisateur'] = self.user.nom_utilisateur
            data['prenom_utilisateur'] = self.user.prenom_utilisateur
            
            # Add any other custom data you want to include
            return data
        else:
            # If the user does not exist or the password is invalid, raise an error
            raise serializers.ValidationError("Unable to log in with provided credentials.")
"""
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            utilisateur = Utilisateur.objects.filter(email=email).first()

            if utilisateur and utilisateur.check_password(password):
                token_data = {
                    'id_utilisateur': utilisateur.id,
                    'nom_utilisateur': utilisateur.nom_utilisateur,
                    'prenom_utilisateur': utilisateur.prenom_utilisateur,
                    'role':utilisateur.role
                }

                # Génération manuelle du jeton d'accès
                refresh_token = RefreshToken.for_user(utilisateur)
                token_data['access'] = str(refresh_token.access_token)
                token_data['refresh'] = str(refresh_token)

                return token_data

        raise serializers.ValidationError("Unable to log in with provided credentials.")
