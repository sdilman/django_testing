from http import HTTPStatus

from django.urls import reverse
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
COMMENT_DELETE_REDIRECT_URL = pytest.lazy_fixture('comment_delete_redirect_url')


@pytest.mark.parametrize(
    "url", [NEWS_HOME_URL, NEWS_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL]
)
def test_pages_availability(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "url", [COMMENT_EDIT_URL, COMMENT_DELETE_URL]
)
@pytest.mark.parametrize(
    "user_client, status",
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND)
    )
)
def test_availability_for_comment_edit_and_delete(
    url, user_client, status
):
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    "url_call, url_redirect", 
    (
        (COMMENT_EDIT_URL, COMMENT_EDIT_REDIRECT_URL),
        (COMMENT_DELETE_URL, COMMENT_DELETE_REDIRECT_URL)
    )
)
def test_redirect_for_anonymous_client(client, url_call, url_redirect):
    assertRedirects(client.get(url_call), url_redirect)
