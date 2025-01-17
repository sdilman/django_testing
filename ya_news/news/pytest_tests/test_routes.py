from http import HTTPStatus

from pytest import lazy_fixture, mark
from pytest_django.asserts import assertRedirects


pytestmark = mark.django_db


NEWS_HOME_URL = lazy_fixture("news_home_url")
NEWS_URL = lazy_fixture("news_url")
LOGIN_URL = lazy_fixture("login_url")
LOGOUT_URL = lazy_fixture("logout_url")
SIGNUP_URL = lazy_fixture("signup_url")
COMMENT_EDIT_URL = lazy_fixture("comment_edit_url")
COMMENT_EDIT_REDIRECT_URL = lazy_fixture("comment_edit_redirect_url")
COMMENT_DELETE_URL = lazy_fixture("comment_delete_url")
COMMENT_DELETE_REDIRECT_URL = lazy_fixture("comment_delete_redirect_url")


@mark.parametrize(
    "url, test_client, status_code",
    (
        (NEWS_HOME_URL, lazy_fixture("client"), HTTPStatus.OK),
        (NEWS_URL, lazy_fixture("client"), HTTPStatus.OK),
        (LOGIN_URL, lazy_fixture("client"), HTTPStatus.OK),
        (LOGOUT_URL, lazy_fixture("client"), HTTPStatus.OK),
        (SIGNUP_URL, lazy_fixture("client"), HTTPStatus.OK),
        (COMMENT_EDIT_URL, lazy_fixture("author_client"), HTTPStatus.OK),
        (
            COMMENT_EDIT_URL,
            lazy_fixture("reader_client"),
            HTTPStatus.NOT_FOUND
        ),
        (COMMENT_EDIT_URL, lazy_fixture("client"), HTTPStatus.FOUND),
        (COMMENT_DELETE_URL, lazy_fixture("author_client"), HTTPStatus.OK),
        (
            COMMENT_DELETE_URL,
            lazy_fixture("reader_client"),
            HTTPStatus.NOT_FOUND
        ),
        (COMMENT_DELETE_URL, lazy_fixture("client"), HTTPStatus.FOUND),
    ),
)
def test_status_code(url, test_client, status_code):
    assert test_client.get(url).status_code == status_code


@mark.parametrize(
    "url_call, url_redirect",
    (
        (COMMENT_EDIT_URL, COMMENT_EDIT_REDIRECT_URL),
        (COMMENT_DELETE_URL, COMMENT_DELETE_REDIRECT_URL),
    ),
)
def test_redirect_for_anonymous_client(client, url_call, url_redirect):
    assertRedirects(client.get(url_call), url_redirect)
