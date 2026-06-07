from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Item
from .serializers import ItemSerializer
from .services import S3Service

import logging
logger = logging.getLogger("api")

class ItemListCreateAPIView(APIView):
    """
    List all items or create a new item.
    """
    def get(self, request, format=None):
        logger.info("Employee API called", extra={
            "app": "hrms",
            "user": request.user.id if request.user.is_authenticated else "anonymous"
        })

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response({
            "success": True,
            "message": "kiran items retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        image_file = request.FILES.get('image') or request.data.get('image')
        if image_file and not isinstance(image_file, str):
            image_url = S3Service.upload_file(image_file)
            data['image'] = image_url

        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailAPIView(APIView):
    """
    Retrieve, update or delete an item instance.
    """
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        image_file = request.FILES.get('image') or request.data.get('image')
        if image_file and not isinstance(image_file, str):
            image_url = S3Service.upload_file(image_file)
            data['image'] = image_url

        serializer = ItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        item = self.get_object(pk)
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        image_file = request.FILES.get('image') or request.data.get('image')
        if image_file and not isinstance(image_file, str):
            image_url = S3Service.upload_file(image_file)
            data['image'] = image_url

        serializer = ItemSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

