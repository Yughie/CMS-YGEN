from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from cms.models import BaseContent, ContentStatus, IndustryType, RealEstateDetails


class HealthCheckTests(APITestCase):
	def test_health_check_is_public(self) -> None:
		url = reverse("health-check")

		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["status"], "ok")
		self.assertEqual(response.data["service"], "cms-ygen-backend")


class ContentListTests(APITestCase):
	def test_content_list_is_public_for_single_admin_setup(self) -> None:
		url = reverse("content-list")

		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)

	def test_content_list_returns_results_without_authentication(self) -> None:
		user = get_user_model().objects.create_user(
			username="owner",
			password="pass1234",
		)
		BaseContent.objects.create(
			title="Listing 1",
			slug="listing-1",
			industry=IndustryType.REAL_ESTATE,
			status=ContentStatus.DRAFT,
			owner=user,
		)
		url = reverse("content-list")

		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["slug"], "listing-1")

	def test_content_list_includes_real_estate_details(self) -> None:
		content = BaseContent.objects.create(
			title="Villa",
			slug="villa",
			industry=IndustryType.REAL_ESTATE,
			status=ContentStatus.DRAFT,
		)
		RealEstateDetails.objects.create(
			content=content,
			listing_price=950000,
			currency="USD",
			bedrooms=5,
			bathrooms=3.5,
			area_sqft=4200,
			address_line="12 Palm Avenue",
		)
		url = reverse("content-list")

		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)
		real_estate_details = response.data[0]["real_estate_details"]
		self.assertIsNotNone(real_estate_details)
		self.assertEqual(real_estate_details["bedrooms"], 5)
		self.assertEqual(real_estate_details["currency"], "USD")
