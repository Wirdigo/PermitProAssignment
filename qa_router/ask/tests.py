from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .services import determine_source


class DetermineSourceTests(TestCase):

    def test_geo_question_english(self):
        self.assertEqual(determine_source("What is the soil type?"), "geo")

    def test_geo_question_dutch(self):
        self.assertEqual(determine_source("Wat is de bodemkaart?"), "geo")

    def test_regulation_question_english(self):
        self.assertEqual(determine_source("What are the building regulations?"), "regulation")

    def test_regulation_question_dutch(self):
        self.assertEqual(determine_source("Wat zijn de voorschriften?"), "regulation")

    def test_unknown_question(self):
        self.assertEqual(determine_source("Hello, how are you?"), "unknown")

    def test_mixed_question_regulation_wins(self):
        question = "Is building allowed according to regulation?"
        self.assertEqual(determine_source(question), "regulation")

    def test_case_insensitive(self):
        self.assertEqual(determine_source("SOIL TYPE"), "geo")
        self.assertEqual(determine_source("REGULATION"), "regulation")


class AskAPITests(APITestCase):
    def test_valid_geo_question(self):
        response = self.client.post('/api/ask/', {'question': 'What is the soil type?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('answer', response.data)
        self.assertIn('source', response.data)
        self.assertEqual(response.data['source'], 'geo')

    def test_valid_regulation_question(self):
        response = self.client.post('/api/ask/', {'question': 'What are the building regulations?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['source'], 'regulation')

    def test_unknown_question(self):
        response = self.client.post('/api/ask/', {'question': 'Hello there'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['source'], 'unknown')

    def test_missing_question_field(self):
        response = self.client.post('/api/ask/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_question(self):
        response = self.client.post('/api/ask/', {'question': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_method_get(self):
        response = self.client.get('/api/ask/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)