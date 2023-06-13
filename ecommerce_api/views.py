from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

def index(request):
    return HttpResponse("API Ecommerce")

@api_view(['GET'])
def getUsers(request):
    users = Utilisateur.objects.all()
    serializer = UtilisateurSerializer(users,many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
def getUserById(request,id):
    user = Utilisateur.objects.get(id_utilisateur=id)
    serializer = UtilisateurSerializer(user)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUserById(request,id):
    try:
        user = Utilisateur.objects.get(id_utilisateur=id)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def updateUser(request,id):
    try:
        user = Utilisateur.objects.get(id_utilisateur=id)
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
    data["id_utilisateur"] = 0
    
    newUser = Utilisateur(
        nom_utilisateur = data["nom_utilisateur"],
        prenom_utilisateur = data["prenom_utilisateur"],
        email = data["email"],
        password = data["password"]
    )
    
    serializer = UtilisateurSerializer(newUser,data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(f"Utilisateur créer avec succès", status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)