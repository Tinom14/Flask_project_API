from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Ivan" + str(uuid4()),
        "last_name": "Ivanov" + str(uuid4()),
        "email": "Ivan" + str(uuid4()) + "@test.ru",
    }


def create_post_payload(author_id):
    return {
        "author_id": author_id,
        "text": "hello"
    }
