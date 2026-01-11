"""
    Este url empieza aqui -> https://domain/
    puerto 443 por defecto
"""
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import EmailTokenObtainPairView

# from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from . import views



urlpatterns = [
    path("", views.index),
    path('admin/', admin.site.urls),
    path("students/", include("estudiantes.urls")),
    path("api/token/", EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name='token_refresh')
    

    
]