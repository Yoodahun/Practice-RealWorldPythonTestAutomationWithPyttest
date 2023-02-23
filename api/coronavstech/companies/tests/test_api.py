import json
import os
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company


## using unittest
@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        client = Client()
        companies_url = reverse("companies-list")
        response = client.get(companies_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        client = Client()
        amazon = Company.objects.create(name="Amazon")
        companies_url = reverse("companies-list")
        response = client.get(companies_url)
        response_content = json.loads(response.content)[0]
        print(response_content.get("name"))
        print(response_content["name"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), "Amazon")
