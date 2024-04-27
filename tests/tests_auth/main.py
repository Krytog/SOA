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


HOST = environ.get("TARGET_HOST")
PORT = environ.get("TARGET_PORT")

URL_SIGNUP = "/api/signup"
URL_LOGIN = "/api/login"
URL_UPDATE = "/api/update"
URL_ABOUT = "/api/about"


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


def test_user_register():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_SIGNUP)
    response = requests.post(url, json=body)
    assert response.status_code == 200


def test_user_register_twice():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_SIGNUP)
    response = requests.post(url, json=body)
    assert response.status_code == 200
    response = requests.post(url, json=body)
    assert response.status_code == 409


def test_login_unregistered_user():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_LOGIN)
    response = requests.post(url, json=body)
    assert response.status_code == 403


def test_login_incorrect_password():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_SIGNUP)
    response = requests.post(url, json=body)
    assert response.status_code == 200
    url = get_complete_url(URL_LOGIN)
    body = {"login": login, "password": get_random_string(15)}
    response = requests.post(url, json=body)
    assert response.status_code == 403


def test_login_correct():
    login, password = get_random_login_and_password()
    body = {"login": login, "password": password}
    url = get_complete_url(URL_SIGNUP)
    response = requests.post(url, json=body)
    assert response.status_code == 200
    url = get_complete_url(URL_LOGIN)
    response = requests.post(url, json=body)
    assert response.status_code == 200
    assert response.json().get('token')


def test_update_correct():
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

    url = get_complete_url(URL_UPDATE)
    body = {
        "name": "Roflonimo",
        "surname": "Baklazhanenko", 
        "bio": "young tomato", 
        "birthdate": "05.06.1989", 
        "phone": "+123456789", 
        "email": datetime.datetime.now().isoformat() + "roflik@gmail.com"
    }
    response = requests.put(url, headers={'Auth': auth_token}, json=body)
    assert response.status_code == 200

    url = get_complete_url(URL_ABOUT)
    url += ("/" + login)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json().get('name') == body["name"]
    assert response.json().get('surname') == body["surname"]
    assert response.json().get('bio') == body["bio"]
    assert response.json().get('birthdate') == body["birthdate"]
    assert response.json().get('phone') == body["phone"]
    assert response.json().get('email') == body["email"]


def test_update_no_auth():
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

    url = get_complete_url(URL_UPDATE)
    body = {
        "name": "Roflonimo",
        "surname": "Baklazhanenko", 
        "bio": "young tomato", 
        "birthdate": "05.06.1989", 
        "phone": "+123456789", 
        "email": datetime.datetime.now().isoformat() + "roflik@gmail.com"
    }
    response = requests.put(url, json=body)
    assert response.status_code == 403


def test_update_incorret_token():
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

    url = get_complete_url(URL_UPDATE)
    body = {
        "name": "Roflonimo",
        "surname": "Baklazhanenko", 
        "bio": "young tomato", 
        "birthdate": "05.06.1989", 
        "phone": "+123456789", 
        "email": datetime.datetime.now().isoformat() + "roflik@gmail.com"
    }
    response = requests.put(url, headers={'Auth': get_random_string(25)}, json=body)
    assert response.status_code == 403
