from rest_framework.permissions import IsAdminUser,AllowAny
from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet

class ProductAPIview(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
