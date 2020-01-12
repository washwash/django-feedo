from django.contrib.auth import get_user_model
from django.urls import reverse


HTTP_200_OK = 200
HTTP_302_REDIRECT = 302

User = get_user_model()


def test_registration_positive(client, db):
    assert not User.objects.exists()

    url = reverse('authentication:sign_up')
    data = {
        'username': 'user',
        'password1': 'pwd',
        'password2': 'pwd'
    }

    response = client.post(url, data)
    assert response.status_code == HTTP_302_REDIRECT
    assert response.url == reverse('index:index')

    assert User.objects.count() == 1
    assert User.objects.first().username == 'user'


def test_registration_mismatched_passwords(client, db):
    assert not User.objects.exists()

    url = reverse('authentication:sign_up')
    data = {
        'username': 'user',
        'password1': 'pwd',
        'password2': 'PDW'
    }

    response = client.post(url, data)
    assert response.status_code == HTTP_200_OK
    assert (
        'The two password fields didn&#39;t match' in
        str(response.content)
    )
    assert User.objects.count() == 0


def test_registration_existed_user(user, client):
    url = reverse('authentication:sign_up')
    data = {
        'username': 'user',
        'password1': 'pwd',
        'password2': 'pwd'
    }

    response = client.post(url, data)
    assert response.status_code == HTTP_200_OK
    assert (
        'A user with that username already exists.' in
        str(response.content)
    )
    assert User.objects.count() == 1


def test_login_positive(user, client):
    url = reverse('authentication:sign_in')
    data = {
        'username': 'user',
        'password': 'password'
    }
    response = client.post(url, data)
    assert response.status_code == HTTP_302_REDIRECT
    assert response.url == reverse('index:index')


def test_login_negative(user, client):
    url = reverse('authentication:sign_in')
    data = {
        'username': 'user',
        'password': 'WRONG PWD'
    }
    response = client.post(url, data)
    assert response.status_code == HTTP_200_OK
    assert (
        'Please enter a correct username and password.' in
        str(response.content)
    )


def test_logout(user_logged_client, client):
    url = reverse('authentication:sign_out')
    response = client.get(url)
    assert response.status_code == HTTP_302_REDIRECT

    response = client.get(reverse('index:index'))
    assert 'Have an account? Sign in!' in str(response.content)
