from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


COMMENT_TEXT = 'Новый текст'
NEWS_TEXT = 'Какой-то текст, {}, еще текст'


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


def test_user_cant_use_bad_words(author_client, news_url):
    for bad_word in BAD_WORDS:
        response = author_client.post(
            news_url, {'text': NEWS_TEXT.format(bad_word)}
        )
        assertFormError(response, 'form', 'text', errors=WARNING)
        assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, comment, news_url, comments_url
):
    new_comment_text = 'Обновлённый комментарий'
    response = author_client.post(
        reverse('news:edit', args=(comment.id,)),
        data={'text': new_comment_text}
    )
    assertRedirects(response, comments_url)
    comment.refresh_from_db()
    assert comment.text == new_comment_text


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment
):
    comment_text = comment.text
    new_comment_text = 'Обновлённый комментарий'
    response = reader_client.post(
        reverse('news:edit', args=(comment.id,)),
        data={'text': new_comment_text}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
