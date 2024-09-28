from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
import logging
from .models import Item
from .serializers import ItemSerializer

logger = logging.getLogger(__name__)

class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item created: {serializer.data['name']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Item creation failed")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        cache_key = f'item_{item_id}'
        item = cache.get(cache_key)

        if not item:
            item = get_object_or_404(Item, id=item_id)
            cache.set(cache_key, item)
            logger.info(f"Item cached: {item.name}")

        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item updated: {serializer.data['name']}")
            return Response(serializer.data)
        logger.error("Item update failed")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        logger.info(f"Item deleted: {item.name}")
        cache.delete(f'item_{item_id}')
        return Response(status=status.HTTP_204_NO_CONTENT)

