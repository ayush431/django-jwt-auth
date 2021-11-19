from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import UserSerializer

# To create new user in the database.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)