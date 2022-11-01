from django.urls import path
from .views import CustomUserCreate, LoginView, UserView, LogoutView, CreateTokenView, ChangePasswordView, SendConfirmationCodeView

urlpatterns = [
    # Register user
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    # Log-in user
    path('login/', LoginView.as_view(), name="login"),
    # Add more informations to the just created user  and confirm the user
    path('user/', UserView.as_view(), name="user"),
    # Log-out and delete JWT token
    path('logout/', LogoutView.as_view(), name="logout"),
    # Create another token code
    path('createToken/', CreateTokenView.as_view(), name="create_token"),
    # Send the confirmation code to change the password
    path('sendConfirmationCode/', SendConfirmationCodeView.as_view(), name="send_confirmation_code"),
    # Change User Password
    path('changePassword/', ChangePasswordView.as_view(), name="change_password"),
]