from django.urls import path
from .views import ItemListCreateAPIView, ItemDetailAPIView

urlpatterns = [
    path('items/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailAPIView.as_view(), name='item-detail'),
]
