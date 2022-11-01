from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    token_code = serializers.CharField(max_length=255, required = False)
    is_active = serializers.BooleanField(default = False, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'token_code', 'is_active')
        
        # If get method is implemented later, it won't see the password
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        # As long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        
        email = validated_data.pop('email', None)
        # Check if password is empty
        if password is not None:
            instance.set_password(password)
        # Check if User exists
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already exists")
        instance.save()
        return instance
    
class ConfirmationUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    about = serializers.CharField(style={'base_template': 'textarea.html'}, max_length=500, required=True)
    age = serializers.IntegerField(required=True)
    phone = serializers.CharField(max_length=255, required=True)
    token_code = serializers.CharField(max_length=255, required=True)
    is_active = serializers.BooleanField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('name', 'about', 'age', 'phone', 'token_code', 'is_active')
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        name = validated_data.pop('name', None)
        # Check if User exists
        if CustomUser.objects.filter(name=name).exists():
            raise serializers.ValidationError("Name already exists")
        instance.save()
        return instance
        
class TokenUserSerializer(serializers.ModelSerializer):
    token_code = serializers.CharField(max_length=255, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['token_code']

# Get all users information
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'about', 'start_date', 'age', 'phone', 'is_active')

# Send confirmation code to the user change his password
class SendConfirmationCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required= True)
    token_code = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'token_code') 

# Allow the change of the user password
class ChangePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    token_code = serializers.CharField(max_length=255, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'token_code')
        # If get method is implemented later, it won't see the password
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # As long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance