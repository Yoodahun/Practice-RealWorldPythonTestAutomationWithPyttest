import json
import logging

import pytest
from django.urls import reverse

from api.coronavstech.companies.models import Company

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)

    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succeed(client) -> None:
    amazon = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    print(response_content.get("name"))
    print(response_content["name"])

    assert response.status_code == 200
    assert response_content.get("name") == "Amazon"


def test_create_company_without_arguments_should_fail(client):
    response = client.post(path=companies_url)

    assert response.status_code == 400
    assert json.loads(response.content)["name"][0] == "This field is required."


@pytest.mark.django_db
def test_create_existing_company_should_fail(client):
    amazon = Company.objects.create(name="Amazon")
    response = client.post(path=companies_url, data={"name": "Amazon"})

    assert response.status_code == 400
    assert (
        json.loads(response.content)["name"][0]
        == "company with this name already exists."
    )


def test_create_company_with_only_name_all_fields_should_be_default(client):
    response = client.post(path=companies_url, data={"name": "test company name"})
    assert response.status_code == 201
    assert json.loads(response.content)["name"] == "test company name"
    assert json.loads(response.content)["status"] == "Hiring"
    assert json.loads(response.content)["application_link"] == ""


def test_create_company_with_layoffs_status_should_succeed(client):
    response = client.post(
        path=companies_url, data={"name": "test company name", "status": "Layoffs"}
    )

    assert response.status_code == 201
    assert json.loads(response.content)["name"] == "test company name"
    assert json.loads(response.content)["status"] == "Layoffs"


def test_create_company_with_wrong_status_should_fail(client):
    response = client.post(
        path=companies_url, data={"name": "test company name", "status": "Wrong Status"}
    )
    assert response.status_code == 400
    assert "Wrong Status" in str(response.content)


@pytest.mark.xfail
def test_should_be_ok_if_fails():
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped():
    assert 1 == 2


def test_raise_covid19_exception_should_pass():
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


def raise_covid19_exception():
    raise ValueError("CoronaVirus Exception")


def function_that_logs_something():
    logger = logging.getLogger("CORONA_LOGS")
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text
