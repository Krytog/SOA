import pytest
import requests
import random
import string
import datetime
from os import environ
import time


def get_random_string(length):
    output = ""
    for _ in range(length):
        output += random.choice(string.ascii_letters)
    return output


def get_random_login_and_password():
    password = get_random_string(20)
    login = get_random_string(10)
    now = datetime.datetime.now()
    login += now.isoformat()
    return login, password


def get_registered_user_token():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_SIGNUP)
    response = requests.post(url, json=body)
    assert response.status_code == 200

    url = get_complete_url(URL_LOGIN)
    response = requests.post(url, json=body)
    assert response.status_code == 200
    assert response.json().get('token')
    auth_token = response.json().get('token')
    return auth_token


def get_post():
    token = get_registered_user_token()
    url = get_complete_url(URL_POST_CREATE)
    body = {
        "content": "This is a post, nothing special"
    }
    response = requests.post(url, headers={'Auth': token}, json=body)
    assert response.status_code == 200
    return response.json().get("id"), token


HOST = environ.get("TARGET_HOST")
PORT = environ.get("TARGET_PORT")

URL_SIGNUP = "/api/signup"
URL_LOGIN = "/api/login"
URL_POST_CREATE = "/api/content/create_post"
URL_POST_GET = "/api/content/get"
URL_POST_VIEW = "/api/statistics/view"
URL_POST_LIKE = "/api/statistics/like"
URL_GET_VIEWS = "/api/statistics/views"
URL_GET_LIKES = "/api/statistics/likes"


def get_complete_url(raw_url):
    return "http://" + HOST + ":" + PORT + raw_url


def wait_for_http(url):
    retries = 10
    exception = None
    while retries > 0:
        try:
            requests.get(url)
            return
        except requests.exceptions.ConnectionError as e:
            exception = e
            print(f'Got ConnectionError for url {url}: {e} , retrying')
            retries -= 1
            time.sleep(2)
    raise exception


def test_reachable_url():
    wait_for_http(get_complete_url(""))
    assert True


def test_create_post_correct():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_SIGNUP)
    response = requests.post(url, json=body)
    assert response.status_code == 200

    url = get_complete_url(URL_LOGIN)
    response = requests.post(url, json=body)
    assert response.status_code == 200
    assert response.json().get('token')
    auth_token = response.json().get('token')

    url = get_complete_url(URL_POST_CREATE)
    body = {
        "content": "Kek"
    }
    response = requests.post(url, headers={'Auth': auth_token}, json=body)
    assert response.status_code == 200


def test_create_post():
    token = get_registered_user_token()
    url = get_complete_url(URL_POST_CREATE)
    body = {
        "content": "This is a post, nothing special"
    }
    response = requests.post(url, headers={'Auth': token}, json=body)
    assert response.status_code == 200


def test_view_post():
    post_id, user_token = get_post()
    url = get_complete_url(URL_POST_VIEW)
    body = {
        "id": post_id
    }
    response = requests.put(url, headers={'Auth': user_token}, json=body)
    print(response.json(), flush=True)
    assert response.status_code == 200


def test_like_post():
    post_id, user_token = get_post()
    url = get_complete_url(URL_POST_LIKE)
    body = {
        "id": post_id
    }
    response = requests.put(url, headers={'Auth': user_token}, json=body)
    print(response.json(), flush=True)
    assert response.status_code == 200


def test_view_nonexisting_post():
    post_id, user_token = get_post()
    url = get_complete_url(URL_POST_VIEW)
    body = {
        "id": 91828384991
    }
    response = requests.put(url, headers={'Auth': user_token}, json=body)
    assert response.status_code == 404

def test_get_views():
    post_id, user_token = get_post()
    url = get_complete_url(URL_POST_LIKE)
    body = {
        "id": post_id
    }
    response = requests.put(url, headers={'Auth': user_token}, json=body)
    print(response.json(), flush=True)
    assert response.status_code == 200
    url = get_complete_url(URL_GET_VIEWS)
    url += ('/' + str(post_id))
    response = requests.get(url, headers={'Auth': user_token})
    print(response.json(), flush=True)
    assert response.status_code == 200

