from http import HTTPStatus
import requests
from app.tests.test_functions import create_user_payload, ENDPOINT


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    user_data = create_response.json()
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]

    user_id = user_data["id"]
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["status"] == "deleted"


def test_user_create_wrong_email():
    payload = create_user_payload()
    payload["email"] = "Ivantest.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_wrong_id():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    user_data = create_response.json()
    user_id = user_data["id"]
    get_response = requests.get(f"{ENDPOINT}/users/-1")
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_get_users_leaderboard():
    n = 3
    users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.CREATED
        users.append(create_response.json()["id"])
    payload_list = {"type": "list", "sort": "asc"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload_list)
    leaderboard = get_response.json()["users"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == n

    payload_graph = {"type": "graph"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload_graph)
    assert get_response.text == '<img src= "/static/users_leaderboard.png">'

    for user_id in users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
