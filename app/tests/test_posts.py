from http import HTTPStatus
import requests
from app.tests.test_functions import create_user_payload, create_post_payload, ENDPOINT


def test_post_create():
    user_payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=user_payload)
    assert create_response.status_code == HTTPStatus.CREATED
    user_id = create_response.json()["id"]
    post_payload = create_post_payload(user_id)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    assert create_response.status_code == HTTPStatus.CREATED
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert len(get_response.json()['posts']) == 1

    post_data = create_response.json()
    assert post_data["author_id"] == post_payload['author_id']
    assert post_data["text"] == post_payload['text']

    post_id = post_data['id']
    get_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()['author_id'] == post_payload['author_id']
    assert get_response.json()['text'] == post_payload['text']
    assert len(get_response.json()['reactions']) == 0

    delete_response = requests.delete(f"{ENDPOINT}/posts/{post_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()['author_id'] == post_payload['author_id']
    assert delete_response.json()['text'] == post_payload['text']
    assert len(delete_response.json()['reactions']) == 0
    assert delete_response.json()["status"] == "deleted"

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_post_create_wrong_author_id():
    post_payload = create_post_payload(-1)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_post_wrong_id():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    user_id = create_response.json()['id']
    assert create_response.status_code == HTTPStatus.CREATED
    post_payload = create_post_payload(user_id)
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    assert create_response.status_code == HTTPStatus.CREATED
    get_response = requests.get(f"{ENDPOINT}/posts/-1")
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    delete_response = requests.delete(f"{ENDPOINT}/posts/{create_response.json()['id']}")
    assert delete_response.status_code == HTTPStatus.OK
    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_post_reaction():
    users = []
    for _ in range(2):
        user_payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=user_payload)
        assert create_response.status_code == HTTPStatus.CREATED
        users.append(create_response.json()['id'])
    post_payload = create_post_payload(users[0])
    create_response = requests.post(f"{ENDPOINT}/posts/create", json=post_payload)
    assert create_response.status_code == HTTPStatus.CREATED
    post_id = create_response.json()['id']
    reaction_payload = {"user_id": users[1],
                        "reaction": "string"}
    create_response = requests.post(f"{ENDPOINT}/posts/{post_id}/reaction", json=reaction_payload)
    assert create_response.status_code == HTTPStatus.OK

    get_response = requests.get(f"{ENDPOINT}/posts/{post_id}")
    assert len(get_response.json()['reactions']) == 1
    get_response = requests.get(f"{ENDPOINT}/users/{users[1]}")
    assert get_response.json()['total_reactions'] == 1
    delete_response = requests.delete(f"{ENDPOINT}/posts/{post_id}")
    assert delete_response.status_code == HTTPStatus.OK
    for user_id in users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
