from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


COMMENT_TEXT = 'Новый текст'
UPDATED_COMMENT_TEXT = 'Обновлённый комментарий'
UPDATE_COMMENT_REQUEST_DATA = {'text': UPDATED_COMMENT_TEXT}
NEWS_TEXT_MASK = 'Какой-то текст, {}, еще текст'


pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
    client, news_url
):
    client.post(news_url, data={'text': COMMENT_TEXT})
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author, author_client, news_url, comments_url, news
):
    response = author_client.post(news_url, {'text': COMMENT_TEXT})
    assertRedirects(response, comments_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    "request_data", [
        {'text': NEWS_TEXT_MASK.format(bad_word)} for bad_word in BAD_WORDS
    ]
)
def test_user_cant_use_bad_words(author_client, news_url, request_data):
    for bad_word in BAD_WORDS:
        response = author_client.post(
            news_url, request_data
        )
        assertFormError(response, 'form', 'text', errors=WARNING)
        assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, comment, comments_url
):
    response = author_client.post(
        reverse('news:edit', args=(comment.id,)),
        data=UPDATE_COMMENT_REQUEST_DATA
    )
    assertRedirects(response, comments_url)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == UPDATE_COMMENT_REQUEST_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment
):
    response = reader_client.post(
        reverse('news:edit', args=(comment.id,)),
        data=UPDATE_COMMENT_REQUEST_DATA
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment == comment


def test_author_can_delete_comment(
    author_client, comment, comments_url
):
    response = author_client.post(
        reverse('news:delete', args=(comment.id,))
    )
    assertRedirects(response, comments_url)
    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_user_cant_delete_comment_of_another_user(
    reader_client, comment
):
    response = reader_client.post(
        reverse('news:delete', args=(comment.id,))
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment == comment