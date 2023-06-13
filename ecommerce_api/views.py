from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

def index(request):
    return HttpResponse("API Ecommerce")

@api_view(['GET'])
def getUsers(request):
    users = Utilisateur.objects.all()
    serializer = UtilisateurSerializer(users)
    print(serializer.data)
    return Response(serializer.data)
