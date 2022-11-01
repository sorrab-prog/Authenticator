from django.contrib import admin
from django.urls import path, include
from django.utils.html import format_html
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

admin.site.site_header =  'Authenticator'
admin.site.index_title = "Authenticator Admin Home"
admin.site.site_title = "Authenticator"
