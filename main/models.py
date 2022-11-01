from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


# This class will create an user to access the website and to the JWT
class CustomAccountManager(BaseUserManager):

    # Defining a method to create super user via terminal
    def create_superuser(self, email, username, name, password, **other_fields):

        # Automatically a super user is staff, superuser and active
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # Error if super user isn't a staff
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
            
        # Error if super user isn't marked as True
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, name, password, **other_fields)

    # Defining method to create user via admin or API
    def create_user(self, email, username, name, password, **other_fields):

        # Making the field e-mail mandatory
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          name=name, **other_fields)
        # Encrypting password into admin
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='E-mail Address', unique=True)
    name = models.CharField(verbose_name = 'Complete Name', max_length=150, blank=True, unique= True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(verbose_name='About', max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    age = models.IntegerField(default = 0, verbose_name = "Age")
    phone = models.CharField(max_length=255, blank = True, null = True)
    token_code = models.CharField(max_length=255, blank = True, null = True)

    # Defining it's methods from CustomAccountManager class
    objects = CustomAccountManager()

    # The username will be the e-mail because, the e-mail is already unique
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name