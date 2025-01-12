from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    "name, args",
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    )
)
@pytest.mark.django_db
def test_pages_availability(client, name, args):
    url = reverse(name, args=None if not args else (args.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "name, args",
    (
        ('news:edit', pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('comment'))
    )
)
@pytest.mark.parametrize(
    "user_client, status",
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND)
    )
)
def test_availability_for_comment_edit_and_delete(
    name, args, user_client, status
):
    url = reverse(name, args=(args.id,))
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize("name", ('news:edit', 'news:delete'))
def test_redirect_for_anonymous_client(client, name, comment):
    url = reverse(name, args=(comment.id,))
    assertRedirects(client.get(url), f'{reverse("users:login")}?next={url}')
