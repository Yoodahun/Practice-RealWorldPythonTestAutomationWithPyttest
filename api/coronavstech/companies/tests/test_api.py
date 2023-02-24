import json
import logging
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company


@pytest.mark.django_db
class BasicComapnyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


## using unittest
class TestGetCompanies(BasicComapnyAPITestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        amazon = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        print(response_content.get("name"))
        print(response_content["name"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), "Amazon")


class TestPostCompanies(BasicComapnyAPITestCase):
    def test_create_company_without_arguments_should_fail(self):
        response = self.client.post(path=self.companies_url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["name"][0], "This field is required.")

    def test_create_existing_company_should_fail(self):
        amazon = Company.objects.create(name="Amazon")
        response = self.client.post(path=self.companies_url, data={"name": "Amazon"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["name"][0], "company with this name already exists.")

    def test_create_company_with_only_name_all_fields_should_be_default(self):
        response = self.client.post(path=self.companies_url, data={"name": "test company name"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)["name"], "test company name")
        self.assertEqual(json.loads(response.content)["status"], "Hiring")
        self.assertEqual(json.loads(response.content)["application_link"], "")

    def test_create_company_with_layoffs_status_should_succeed(self):
        response = self.client.post(path=self.companies_url, data={"name": "test company name", "status": "Layoffs"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content)["name"], "test company name")
        self.assertEqual(json.loads(response.content)["status"], "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self):
        response = self.client.post(path=self.companies_url,
                                    data={"name": "test company name", "status": "Wrong Status"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Wrong Status", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self):
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self):
        self.assertEqual(1, 2)

    def test_raise_covid19_exception_should_pass(self):
        with pytest.raises(ValueError) as e:
            self.raise_covid19_exception()
        self.assertEqual("CoronaVirus Exception", str(e.value))

    def raise_covid19_exception(self):
        raise ValueError("CoronaVirus Exception")

    # def function_that_logs_something(self):
    #     self.logger = logging.getLogger("CORONA_LOGS")
    #     try:
    #         raise ValueError("CoronaVirus Exception")
    #     except ValueError as e:
    #         self.logger.warning(f"I am logging {str(e)}")
    #
    # def test_logged_warning_level(self, caplog) -> None:
    #     self.function_that_logs_something()
    #     assert "I am logging CoronaVirus Exception" in caplog.text
