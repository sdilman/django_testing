from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    "name, args",
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    )
)
@pytest.mark.django_db
def test_pages_availability(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "name, args",
    (
        ('news:edit', pytest.lazy_fixture('comment_id_args')),
        ('news:delete', pytest.lazy_fixture('comment_id_args'))
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
    url = reverse(name, args=args)
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize("name", ('news:edit', 'news:delete'))
def test_redirect_for_anonymous_client(client, name, comment_id_args):
    url = reverse(name, args=comment_id_args)
    assertRedirects(client.get(url), f'{reverse("users:login")}?next={url}')
