from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import ProductAPIview   

app_name = "store"
router = DefaultRouter()
router.register(r'products',ProductAPIview,basename='products')

urlpatterns = [
    path("", views.home , name="home"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name= "register"),
    path("logout/", views.logout_user, name="logout"),
    path('api/',include(router.urls)),
]
