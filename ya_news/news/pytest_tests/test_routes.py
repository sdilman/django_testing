from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


NEWS_HOME_URL = pytest.lazy_fixture('news_home_url')
NEWS_URL = pytest.lazy_fixture('news_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
COMMENT_EDIT_REDIRECT_URL = pytest.lazy_fixture('comment_edit_redirect_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
COMMENT_DELETE_REDIRECT_URL = pytest.lazy_fixture(
    'comment_delete_redirect_url'
)


@pytest.mark.parametrize(
    "url, test_client, status_code",
    (
        (
            NEWS_HOME_URL,
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            NEWS_URL,
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            LOGIN_URL,
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            LOGOUT_URL,
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            SIGNUP_URL,
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            COMMENT_EDIT_URL,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            COMMENT_EDIT_URL,
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            COMMENT_DELETE_URL,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            COMMENT_DELETE_URL,
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND
        ),
    )
)
def test_status_code(url, test_client, status_code):
    response = test_client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "url_call, url_redirect",
    (
        (COMMENT_EDIT_URL, COMMENT_EDIT_REDIRECT_URL),
        (COMMENT_DELETE_URL, COMMENT_DELETE_REDIRECT_URL)
    )
)
def test_redirect_for_anonymous_client(client, url_call, url_redirect):
    assertRedirects(client.get(url_call), url_redirect)
