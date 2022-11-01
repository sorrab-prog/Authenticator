from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CustomUserSerializer, ConfirmationUserSerializer, TokenUserSerializer, UserSerializer, ChangePasswordSerializer, SendConfirmationCodeSerializer
from rest_framework.permissions import AllowAny
import jwt, datetime
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.conf import settings
from django.core.mail import EmailMessage
import random
import string

# This class will create a new User
class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    
    # Overriding post method to external users do not see the get method
    def post(self, request, format='json'):
        # Defining the token_code before it get post to send it after in the e-mail confirmation
        request.data['token_code'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # Send token_code to the user to confirm his e-mail
                message_email = EmailMessage(
                'Please confirm your email_adress',
                "Follow below your confirmation code:\n"+user.token_code,
                settings.EMAIL_HOST_USER,
                [request.data['email']]
                )
                message_email.fail_silently = False
                message_email.send()
                # Transform Data from serializer in JSON
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data ['password']
        
        # With the email we will find the user
        # E-mail is unique and we will only get the first and unique user that appear with that email
        user = CustomUser.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        # This function is providade by Django and compare the passwords even if its hasheds
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        # JWT Token Configurations
        payload = {
            'id': user.id,
            # Token Time Expiration
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # Date that token was created
            'iat': datetime.datetime.utcnow()
        }
        
        # Creating JWT Token
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        # Setting the return of the JWT token via cookies
        # This returned token will be used to log-in our user
        response = Response()
        
        # HTTPONLY is True because we don't want to the frontend to access this token
        # The only purpose of this token is be sent to the backend
        response.set_cookie(key='jwt', value = token, httponly=True)
        
        response.data = {
            'Message': "Token successfully created"
        }
        
        return response

# ADD new informations to the just created user 
class UserView(APIView):
    def get(self, request, format='json'):
        # Getting the token from the cookies
        token = request.COOKIES.get('jwt')
        
        # IF the token is not set
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        # Decoding the jwt token
        try:
            payload = jwt.decode(token, 'secret', algorithms = ["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired Token")
        
        # Filtering the user through the cookies   
        user = CustomUser.objects.filter(id=payload['id']).first()
        
        # Serializing the user to the JSON Object
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
    def post(self, request, format='json'):
        # Getting the token from the cookies
        token = request.COOKIES.get('jwt')
        
        # IF the token is not set
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        # Decoding the jwt token
        try:
            payload = jwt.decode(token, 'secret', algorithms = ["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired Token")
        
        # Filtering the user through the cookies   
        user = CustomUser.objects.filter(id=payload['id']).first()

        # Posting in the user filtered
        serializer = ConfirmationUserSerializer(user, data=request.data)
        if serializer.is_valid():
            name = request.data['name']
            if CustomUser.objects.filter(name=name).exists():
                # If the token code isn't correct, it generates another token, but don't send if via e-mail, to the user click in re-send code and insert the correct token
                user.token_code = ''.join(random.choice(string.printable) for i in range(10))
                user.save()
                raise ValidationError("Name already exists")
            else:
                if request.data['token_code'] == user.token_code: 
                    user.is_active = True
                    serializer.save()
                    user.token_code = ''.join(random.choice(string.printable) for i in range(10))
                    user.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    # If the token code isn't correct, it generates another token, but don't send if via e-mail, to the user click in re-send code and insert the correct token
                    user.token_code = ''.join(random.choice(string.printable) for i in range(10))
                    user.save()
                    raise AuthenticationFailed("Invalid code")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
    
        # Removing the cookie to logout
        response = Response()
        response.delete_cookie('jwt')
        response.data = { 
            'message': 'success'
        }
        
        return response

# Create new confirmation token
class CreateTokenView(APIView):
    def post(self, request, format='json'):
        # Getting the token from the cookies
        jwt_token = request.COOKIES.get('jwt')
        
        # IF the token is not set
        if not jwt_token:
            raise AuthenticationFailed("Unauthenticated")
        
        # Decoding the jwt token
        try:
            payload = jwt.decode(jwt_token, 'secret', algorithms = ["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired Token")
        
        # Filtering the user through the cookies   
        user = CustomUser.objects.filter(id=payload['id']).first()
        
        serializer = TokenUserSerializer(user, data = request.data)
        serializer.is_valid(raise_exception = True)
        if serializer.is_valid():
            serializer.save()
            # Send token_code to the user to confirm his e-mail
            message_email = EmailMessage(
                'Please confirm your email_adress',
                'Follow below your confirmation code:\n\n'+user.token_code,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            message_email.fail_silently = False
            message_email.send()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            data = {
                'error':"Unknown error occurred, please contact the administrator"
            }
            return data

# Send confirmation code to the user
class SendConfirmationCodeView(APIView):
    def post(self, request, format='json'):
        email = request.data['email']
        user = CustomUser.objects.filter(email = email).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        
        serializer = SendConfirmationCodeSerializer(user, data = request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            confirmation_code = EmailMessage(
                'Change Password Confirmation Code',
                'Follow bellow your confirmation code to change your password:\n\n' + user.token_code,
                settings.EMAIL_HOST_USER,
                [email]
            )
            confirmation_code.fail_silently = False
            confirmation_code.send()
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        else:
            data = {
                'error':'Unknown error occurred, please contact the administrator'
            }
            return data

# Allow the change of the user password    
class ChangePasswordView(APIView):
    def post(self, request, format='json'):
        email = request.data['email']
        password = request.data['password']
                
        # With the email we will find the user
        # E-mail is unique and we will only get the first and unique user that appear with that email
        user = CustomUser.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User not found!")
        
        serializer = ChangePasswordSerializer(user, data = request.data)
        if serializer.is_valid():
            if request.data['token_code'] == user.token_code:
                user.set_password(password) 
                user.token_code = ''.join(random.choice(string.printable) for i in range(10))
                user.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                # If the token code isn't correct, it generates another token, but don't send if via e-mail, to the user click in re-send code and insert the correct token
                user.token_code = ''.join(random.choice(string.printable) for i in range(10))
                user.save()
                raise AuthenticationFailed("Invalid code")
        else:
            data = {
                'error':"Unknown error occurred, please contact the administrator"
            }
            return data