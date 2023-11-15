from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_form_with_existing_template():
    test_data = {
        "email_address": "almaz@gmail.com",
        "phone_number": "+7 999 123 12 12"
    }
    expected_content = {"name": "Contact Details"}

    response = client.post("/get_form", json=test_data)
    assert response.status_code == 200
    assert response.json() == expected_content


def test_get_form_with_wrong_field_types():
    test_data = {
        "email_address": "Just some weird text",
        "phone_number": "Your phone could be there, mate"
    }
    expected_content = {
        "email_address": "text",
        "phone_number": "text"
    }

    response = client.post("/get_form", json=test_data)
    assert response.status_code == 200
    assert response.json() == expected_content


def test_get_form_without_existing_template():
    test_data = {
        "user_name": "JohnDoe",
        "phone_number": "+7 999 123 12 12",
        "date_of_birth": "2023-11-15",
        "email": "johndoe@test.com"
    }
    expected_content = {
        "user_name": "text",
        "phone_number": "phone",
        "date_of_birth": "date",
        "email": "email"
    }

    response = client.post("/get_form", json=test_data)
    assert response.status_code == 200
    assert response.json() == expected_content
