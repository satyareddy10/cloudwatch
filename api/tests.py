from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item

class ItemAPITests(APITestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Laptop",
            description="Work laptop",
            price="999.99",
            is_available=True
        )
        self.list_create_url = reverse('item-list-create')
        self.detail_url = reverse('item-detail', kwargs={'pk': self.item.pk})

    def test_create_item(self):
        data = {
            "name": "Smartphone",
            "description": "Android phone",
            "price": "499.50",
            "is_available": True
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(response.data['name'], "Smartphone")

    def test_list_items(self):
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.item.name)

    def test_retrieve_item(self):
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_update_item(self):
        data = {
            "name": "Laptop Pro",
            "description": "Updated description",
            "price": "1299.99",
            "is_available": False
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Laptop Pro")
        self.assertEqual(str(self.item.price), "1299.99")
        self.assertFalse(self.item.is_available)

    def test_partial_update_item(self):
        data = {
            "price": "899.99"
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Laptop") # unchanged
        self.assertEqual(str(self.item.price), "899.99")

    def test_delete_item(self):
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_retrieve_nonexistent_item(self):
        nonexistent_url = reverse('item-detail', kwargs={'pk': 9999})
        response = self.client.get(nonexistent_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

