"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.utils import unittest
from django.test.client import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """
        Check index page is available or not.
        """
        response = self.client.get('/trs/')
        self.assertEqual(response.status_code, 200)
