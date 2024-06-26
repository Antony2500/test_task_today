import pytest
import sys
import os
from pathlib import Path
from sqlalchemy import select

from app.models.user import User as DB_User


# Тест для регистрации пользователя
async def test_signup(client, test_session):
    signup_data = {
        "email": "testuser@example.com",
        "password": "testpassword",
        "username": "testuser"
    }

    response = client.post("/auth/signup", json=signup_data)

    assert response.status_code == 200

    json_response = response.json()
    assert "access_token" in json_response
    assert "refresh_token" in json_response

    user = await test_session.scalar(
        select(DB_User).filter(DB_User.email == "testuser@example.com")
    )
    assert user.email is not None


async def test_signup_unavailable_username(client):
    signup_data = {
        "email": "testuser@example.com",
        "password": "testpassword",
        "username": "xxx"
    }

    response = client.post("/auth/signup", json=signup_data)

    assert response.status_code == 422  # Или другой соответствующий статус ошибки


async def test_signup_existed_username(client, register_user):
    signup_data = {
        "email": "testuser2@example.com",
        "password": "testpassword",
        "username": "testuser"
    }

    response = client.post("/auth/signup", json=signup_data)

    assert response.status_code == 400

    json_response = response.json()
    assert "Username already exists" in json_response["detail"]


async def test_signup_existed_email(client, register_user):
    signup_data = {
        "email": "testuser@example.com",
        "password": "testpassword",
        "username": "testuser2"
    }

    response = client.post("/auth/signup", json=signup_data)

    assert response.status_code == 400

    json_response = response.json()
    assert "Email already exists" in json_response["detail"]
