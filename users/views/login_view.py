
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from ..models import User
import jwt, datetime    

#if email and password is correct set the jwt token in cookies and return the token as response.

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password ')

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode("utf-8")

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data   = {
            'jwt':token
        }
        return response
        
#if user is logged in then he get all the details.

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed({"message":"You are not authenticated"})
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"message":"You are not authenticated"})
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
#to delete set cookies
class logoutView(APIView):
    def get(self, request):

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"success"
        }
        return response