from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Student


class StudentAPITests(APITestCase):
    def test_student_crud(self):
        list_url = reverse("student-list")
        payload = {"name": "Ayesha Khan", "email": "ayesha@example.com", "age": 20}

        create_response = self.client.post(list_url, payload, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        student_id = create_response.data["id"]

        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        detail_url = reverse("student-detail", args=[student_id])
        retrieve_response = self.client.get(detail_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data["email"], payload["email"])

        update_response = self.client.put(
            detail_url,
            {"name": "Ayesha Khan", "email": "ayesha@example.com", "age": 21},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["age"], 21)

        partial_update_response = self.client.patch(
            detail_url, {"name": "Ayesha Ahmed"}, format="json"
        )
        self.assertEqual(partial_update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(partial_update_response.data["name"], "Ayesha Ahmed")

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=student_id).exists())

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            reverse("student-list"),
            {"name": "Invalid Email", "email": "not-an-email", "age": 20},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_invalid_age_is_rejected(self):
        response = self.client.post(
            reverse("student-list"),
            {"name": "Invalid Age", "email": "age@example.com", "age": 0},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", response.data)
