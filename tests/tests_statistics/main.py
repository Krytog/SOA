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
URL_POST_GET = "/api/content/get_post"
URL_POST_VIEW = "/api/statistics/view"
URL_POST_LIKE = "/api/statistics/like"
URL_GET_VIEWS = "/api/statistics/views"
URL_GET_LIKES = "/api/statistics/likes"
URL_STATISTICS = "/api/statistics/aboutpost"
URL_TOP_USERS = "/api/statistics/top_users"
URL_TOP_POSTS = "/api/statistics/top_posts"


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


def test_get_post_statistics():
    post_id, user_token = get_post()
    likes_count = 5
    views_count = 10
    for _ in range(likes_count):
        user_token = get_registered_user_token()
        url = get_complete_url(URL_POST_LIKE)
        body = {
            "id": post_id
        }
        response = requests.put(url, headers={'Auth': user_token}, json=body)
        assert response.status_code == 200
    for _ in range(views_count):
        user_token = get_registered_user_token()
        url = get_complete_url(URL_POST_VIEW)
        body = {
            "id": post_id
        }
        response = requests.put(url, headers={'Auth': user_token}, json=body)
        assert response.status_code == 200
    url = get_complete_url(URL_STATISTICS)
    url += ('/' + str(post_id))
    time.sleep(15)  # time for kafka and clickhouse to handle event
    response = requests.get(url, headers={'Auth': user_token})
    assert response.status_code == 200
    assert response.json().get("views") == views_count
    assert response.json().get("likes") == likes_count


def create_post_by(auth_token):
    url = get_complete_url(URL_POST_CREATE)
    body = {
        "content": "This is a post, nothing special"
    }
    response = requests.post(url, headers={'Auth': auth_token}, json=body)
    return response.json().get("id")


def like_post(post_id):
    user_token = get_registered_user_token()
    url = get_complete_url(URL_POST_LIKE)
    body = {
        "id": post_id
    }
    response = requests.put(url, headers={'Auth': user_token}, json=body)
    assert response.status_code == 200


def get_user_with_likes(count):
    login, password = get_random_login_and_password()
    url = get_complete_url(URL_SIGNUP)
    body = {"login": login, "password": password}
    response = requests.post(url, json=body)
    assert response.status_code == 200
    url = get_complete_url(URL_LOGIN)
    body = {"login": login, "password": password}
    response = requests.post(url, json=body)
    assert response.status_code == 200
    assert response.json().get('token')
    auth_token = response.json().get('token')

    post_id = create_post_by(auth_token)

    for _ in range(count):
        like_post(post_id)
    return login


def test_get_top_users():
    user_token = get_registered_user_token()
    url = get_complete_url(URL_TOP_USERS)
    response = requests.get(url, headers={'Auth': user_token})
    assert response.status_code == 200

    prev_max_likes = 1
    if len(response.json()) > 0:
        prev_max_likes = response.json()[0]["likes"] + 1

    likes = [2 * prev_max_likes, int(1.5 * prev_max_likes), prev_max_likes]
    logins = []
    for i in range(3):
        logins.append(get_user_with_likes(likes[i]))
    time.sleep(10)

    response = requests.get(url, headers={'Auth': user_token})
    for i in range(3):
        assert response.json()[i]["login"] == logins[i]
        assert response.json()[i]["likes"] == likes[i]


def get_post_and_author_login():
    login, password = get_random_login_and_password()
    url = get_complete_url(URL_SIGNUP)
    body = {"login": login, "password": password}
    response = requests.post(url, json=body)
    assert response.status_code == 200
    url = get_complete_url(URL_LOGIN)
    body = {"login": login, "password": password}
    response = requests.post(url, json=body)
    assert response.status_code == 200
    assert response.json().get('token')
    auth_token = response.json().get('token')

    post_id = create_post_by(auth_token)
    return post_id, login


def test_get_top_posts_likes():
    url = get_complete_url(URL_TOP_POSTS)
    url += '?sorted_by_likes=true'

    user_token = get_registered_user_token()
    response = requests.get(url, headers={'Auth': user_token})
    assert response.status_code == 200

    prev_max_likes = 1
    if len(response.json()) > 0:
        prev_max_likes = response.json()[0]["likes"] + 1

    posts = []
    logins = []
    for i in range(5):
        post, login = get_post_and_author_login()
        posts.append(post)
        logins.append(login)

    for i in range(5):
        for _ in range(prev_max_likes + i):
            like_post(posts[i])
    
    time.sleep(10)
    response = requests.get(url, headers={'Auth': user_token})
    assert response.status_code == 200

    for i in range(5):
        assert response.json()[i]["author"] == logins[i]
        assert response.json()[i]["likes"] == prev_max_likes + 4 - i
        assert response.json()[i]["post_id"] == posts[i]

def test_get_top_posts_views():
    url = get_complete_url(URL_TOP_POSTS)
    url += '?sorted_by_likes=false'

    user_token = get_registered_user_token()
    response = requests.get(url, headers={'Auth': user_token})
    assert response.status_code == 200

    prev_max_views = 1
    if len(response.json()) > 0:
        prev_max_views = response.json()[0]["views"] + 1

    posts = []
    logins = []
    for i in range(5):
        post, login = get_post_and_author_login()
        posts.append(post)
        logins.append(login)

    for i in range(5):
        for _ in range(prev_max_views + i):
            user_token = get_registered_user_token()
            url = get_complete_url(URL_POST_LIKE)
            body = {
                "id": posts[i]
            }
            response = requests.put(url, headers={'Auth': user_token}, json=body)
            assert response.status_code == 200
    
    time.sleep(10)
    response = requests.get(url, headers={'Auth': user_token})
    assert response.status_code == 200

    for i in range(5):
        assert response.json()[i]["author"] == logins[i]
        assert response.json()[i]["views"] == prev_max_views + 4 - i
        assert response.json()[i]["post_id"] == posts[i]
