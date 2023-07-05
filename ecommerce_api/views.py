from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
import os
from .serializers import *

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 

#Endpoint Utilisateur
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = Utilisateur.objects.all()
    serializer = UtilisateurSerializer(users,many=True)
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserById(request,id):
    try:
        user = Utilisateur.objects.get(id=id)
    except Utilisateur.DoesNotExist:
        return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
    
    return Response(UtilisateurSerializer(user).data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUserById(request,id):
    try:
        user = Utilisateur.objects.get(id=id)
        
    except Utilisateur.DoesNotExist:
        return Response({"message":"User deleted succesfully"},status=status.HTTP_404_NOT_FOUND)
    
    profilePicture = user.profilePicture.path 
    if profilePicture !=  f'{os.getcwd()}/media/uploads/user/user_placeholder.jpeg':
        os.remove(profilePicture)
        
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request,id_utilisateur):
    try:
        utilisateur = Utilisateur.objects.get(id=id_utilisateur)
        serializer = UtilisateurSerializer(utilisateur, data=request.data)
        
        if serializer.is_valid():
            old_profile_picture = utilisateur.profilePicture.path  # Get the old profile picture path
            
            # Check if a new profile picture is provided
            if 'profilePicture' in request.FILES:
                # Delete the old profile picture from the media folder
                if os.path.exists(old_profile_picture) and old_profile_picture != f'{os.getcwd()}/media/uploads/user/user_placeholder.jpeg':
                    os.remove(old_profile_picture)
            
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Utilisateur.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProductsByUser(request,utilisateur_id):
    products = Produit.objects.filter(id_utilisateur=utilisateur_id)
    serializer = ProduitSerializer(products,many=True)
    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProduct(request,id):
    try:
        produit = Produit.objects.get(id_produit=id)
    except Produit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    serializer = ProduitSerializer(produit, data=request.data)
    
    if serializer.is_valid():
        oldImg = produit.pathImg.path  
            
        # Verifier si l'utilisateur a modifier l'image
        if 'pathImg' in request.FILES:
            # Suppression de l'ancienne image dans le répertoire media
            if os.path.exists(oldImg) and oldImg != f'{os.getcwd()}/media/uploads/products/logo.png':
                os.remove(oldImg)
            
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProduct(request):
    serializer = ProduitSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Product created succesfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProductById(request,id):
    try:
        product = Produit.objects.get(id_produit=id)
    except Produit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    img = product.pathImg.path
   
    #Supprimer l'image dans le repertoire media
    if img != f'{os.getcwd()}/media/uploads/products/logo.png':
        os.remove(img)
        
    product.delete()
    return Response({"message":"Product deleted succesfully!"},status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def getCategories(request):
    categories = Produit.objects.values_list('categorie', flat=True).distinct()
    return Response(categories)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPanier(request,id):
    try:
        produits = Panier.objects.get(utilisateur_id=id).produits
        serializer = ProduitSerializer(produits,many=True)
        return Response(serializer.data)
    except Panier.DoesNotExist:
        return Response({'message': 'Le panier de cette utilisateur est introuvable'}, status=404)
    
@api_view(['POST', 'DELETE'])
def addOrRemoveInPanier(request,id_utilisateur, id_produit):
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
@permission_classes([IsAuthenticated])
def getCommande(request, id_utilisateur):
    try:
        utilisateur = Utilisateur.objects.get(id=id_utilisateur)
    except Utilisateur.DoesNotExist:
        return Response({'message': 'Utilisateur inexistant.'}, status=status.HTTP_404_NOT_FOUND)

    commandes = Commande.objects.filter(id_utilisateur=utilisateur)
    commandes_data = []

    for commande in commandes:
        details_commande = DetailCommande.objects.filter(commande=commande)
        produits = []

        for detail_commande in details_commande:
            produit_data = {
                'id_produit': detail_commande.produit.id_produit,
                'nom_produit': detail_commande.produit.nom,
                'quantite': detail_commande.quantite
            }
            produits.append(produit_data)

        commande_data = {
            'id_commande': commande.id_commande,
            'date_commande': commande.date_commande,
            'produits': produits
        }
        commandes_data.append(commande_data)

    return Response(commandes_data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCommande(request, id_utilisateur):
    panier = request.data.get('panier')

    # Vérifier si l'utilisateur existe
    try:
        utilisateur = Utilisateur.objects.get(id=id_utilisateur)
    except Utilisateur.DoesNotExist:
        return Response({'message': 'Utilisateur inexistant.'}, status=status.HTTP_404_NOT_FOUND)

    # Créer une nouvelle commande
    commande = Commande.objects.create(id_utilisateur=utilisateur, status_annulation=False, date_annulation=None)

    for item in panier:
        id_produit = item.get('id_produit')
        quantite = item.get('quantite')

        # Vérifier si le produit existe
        try:
            produit = Produit.objects.get(id=id_produit)
        except Produit.DoesNotExist:
            return Response({'message': f"Produit d'ID {id_produit} inexistant."}, status=status.HTTP_404_NOT_FOUND)

        # Créer un détail de commande pour le produit spécifié
        detail_commande = DetailCommande.objects.create(commande=commande, produit=produit, quantite=quantite)

    return Response({'message': 'Commande passée avec succès.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeProductCommande(request, id_utilisateur, id_produit):
    try:
        utilisateur = Utilisateur.objects.get(id=id_utilisateur)
        produit = Produit.objects.get(id=id_produit)
    except (Utilisateur.DoesNotExist, Produit.DoesNotExist):
        return Response({'message': 'Utilisateur ou produit inexistant.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        commande = Commande.objects.get(id_utilisateur=utilisateur)
    except Commande.DoesNotExist:
        return Response({'message': 'Commande inexistante.'}, status=status.HTTP_404_NOT_FOUND)

    # Supprimer le produit de la commande
    commande.produit.remove(produit)

    # Supprimer le détail de commande correspondant
    detail_commande = DetailCommande.objects.filter(commande=commande, produit=produit).first()
    if detail_commande:
        detail_commande.delete()

    return Response({'message': 'Produit supprimé de la commande avec succès.'}, status=status.HTTP_200_OK)


#endpoint evaluation
@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def evaluateProduct(request, id_utilisateur, id_produit):
    if request.method == 'POST':
        data = request.data.copy()
        data['utilisateur'] = id_utilisateur
        data['produit'] = id_produit
        serializer = EvaluationSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            evaluation = Evaluation.objects.get(utilisateur=id_utilisateur, produit=id_produit)
        except Evaluation.DoesNotExist:
            return Response({"message": "Evaluation not found"}, status=404)

        serializer = EvaluationSerializer(evaluation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEvaluation(request, id_utilisateur, id_produit):
    try:
        evaluation = Evaluation.objects.get(utilisateur_id=id_utilisateur, produit_id=id_produit)
        serializer = EvaluationSerializer(evaluation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Evaluation.DoesNotExist:
        return Response({'message': 'L\'évaluation spécifiée n\'existe pas.'})