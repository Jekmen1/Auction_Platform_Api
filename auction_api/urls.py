from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, ProductListCreateAPIView, ProductDetailAPIView, BidCreateAPIView
urlpatterns = [
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:product_id>/bids/', BidCreateAPIView.as_view(), name='bid-create'),
]