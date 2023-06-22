from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 

@api_view(["GET"])
def index(request):
    return Response("API Ecommerce")
    
#Endpoint Utilisateur
@api_view(['GET'])
def getUsers(request):
    users = Utilisateur.objects.all()
    serializer = UtilisateurSerializer(users,many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
def getUserById(request,id):
    user = Utilisateur.objects.get(id=id)
    serializer = UtilisateurSerializer(user)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUserById(request,id):
    try:
        user = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def updateUser(request,id):
    try:
        user = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UtilisateurSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createUser(request): 
    data = request.data
    
    newUser = Utilisateur(
        nom_utilisateur = data["nom_utilisateur"],
        prenom_utilisateur = data["prenom_utilisateur"],
        email = data["email"],
        password = make_password(data["password"])
    )
    
    serializer = UtilisateurSerializer(newUser,data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User created succesfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Endpoint Produit
@api_view(["GET"])
def getProducts(request):
    products = Produit.objects.all()
    serializer = ProduitSerializer(products,many=True)
    return Response(serializer.data)

#Endpoint Produit
@api_view(["GET"])
def getProductById(request,id):
    product = Produit.objects.get(id_produit=id)
    serializer = ProduitSerializer(product)
    return Response(serializer.data)
    
@api_view(["GET"])
def getProductByCategory(request,category):
    products = Produit.objects.filter(categorie=category)
    serializer = ProduitSerializer(products,many=True)
    return Response(serializer.data)

@api_view(["PUT"])
def updateProduct(request,id):
    try:
        produit = Produit.objects.get(id_produit=id)
    except Produit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProduitSerializer(produit, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createProduct(request):
    serializer = ProduitSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Product created succesfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteProductById(request,id):
    try:
        product = Produit.objects.get(id_produit=id)
    except Produit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response({"message":"Product deleted succesfully!"},status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def getCategories(request):
    categories = Produit.objects.values_list('categorie', flat=True).distinct()
    return Response(categories)

#Endpoint Panier
@api_view(["GET"])
def getPanier(request,id):
    try:
        produits = Panier.objects.get(utilisateur_id=id).produits
        serializer = ProduitSerializer(produits,many=True)
        return Response(serializer.data)
    except Panier.DoesNotExist:
        return Response({'message': 'Le panier de cette utilisateur est introuvable'}, status=404)
    
@api_view(['POST', 'DELETE'])
def addOrRemoveInPanier(request, id_utilisateur, id_produit):
    try:
        panier = Panier.objects.get(utilisateur_id=id_utilisateur)
        produit = Produit.objects.get(id_produit=id_produit)

        if request.method == 'POST':
            panier.produits.add(produit)
        elif request.method == 'DELETE':
            panier.produits.remove(produit)

        serializer = PanierSerializer(panier)
        return Response(serializer.data)

    except (Panier.DoesNotExist, Produit.DoesNotExist):
        return Response({'message': 'User or product not found'}, status=404)

#Endpoint Commande    
@api_view(["GET"])
def getCommande(request,id):
    try:
        commandes = Commande.objects.get(id_utilisateur=id).produit
        serializer = ProduitSerializer(commandes,many=True)
        return Response(serializer.data)
    except Commande.DoesNotExist:
        return Response({'message': 'Les commandes de cette utilisateur est introuvable'}, status=404)
    
@api_view(['POST', 'DELETE'])
def addOrRemoveCommande(request, utilisateur_id, produit_id):
    try:
        commande = Commande.objects.get(id_utilisateur=utilisateur_id)
    except Commande.DoesNotExist:
        return Response({"message": "Commande non trouvée"}, status=404)

    if request.method == 'POST':
        try:
            commande.produit.add(produit_id)
        except Exception as e:
            return Response({"message": str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            commande.produit.remove(produit_id)
        except Exception as e:
            return Response({"message": str(e)}, status=400)

    serializer = CommandeSerializer(commande)
    return Response(serializer.data)

#endpoint evaluation
@api_view(['POST', 'PUT'])
def evaluate_product(request, utilisateur_id, produit_id):
    if request.method == 'POST':
        data = request.data
        data['utilisateur'] = utilisateur_id
        data['produit'] = produit_id
        serializer = EvaluationSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            evaluation = Evaluation.objects.get(utilisateur=utilisateur_id, produit=produit_id)
        except Evaluation.DoesNotExist:
            return Response({"message": "Evaluation not found"}, status=404)

        serializer = EvaluationSerializer(evaluation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)