# tests.py
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from item.models.item_model import Item
import threading

class DatabaseLockTestCase(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.item = Item.objects.create(name="Test Item")
        self.client = APIClient()

    def update_item(self):
        url = reverse('update_item', kwargs={'item_id': self.item.item_id})
        response = self.client.post(url)
        return response

    def test_concurrent_updates(self):
        # url = reverse('update_item', kwargs={'item_id': self.item.item_id})

        # Create threads to simulate concurrent access
        thread1 = threading.Thread(target=self.update_item)
        thread2 = threading.Thread(target=self.update_item)

        # Start threads
        thread1.start()
        thread2.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()

        # Refresh the item from the database
        self.item.refresh_from_db()

        # Check the item's count to ensure it was incremented correctly
        self.assertEqual(self.item.hsn_code, 1)

