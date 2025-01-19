from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


COMMENT_REQUEST_DATA = {'text': 'Какой-то текст'}
BAD_WORDS_REQUEST_DATA = [
    {'text': f'Какой-то текст, {bad_word}, еще текст'}
    for bad_word in BAD_WORDS
]


pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
    client, news_url
):
    client.post(news_url, COMMENT_REQUEST_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author, author_client, news_url, comments_url, news
):
    response = author_client.post(news_url, COMMENT_REQUEST_DATA)
    assertRedirects(response, comments_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_REQUEST_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    "request_data", BAD_WORDS_REQUEST_DATA
)
def test_user_cant_use_bad_words(author_client, news_url, request_data):
    response = author_client.post(news_url, request_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, comment, comments_url, comment_edit_url
):
    response = author_client.post(
        comment_edit_url,
        data=COMMENT_REQUEST_DATA
    )
    assertRedirects(response, comments_url)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == COMMENT_REQUEST_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment, comment_edit_url
):
    response = reader_client.post(
        comment_edit_url,
        data=COMMENT_REQUEST_DATA
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == comment.text
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_author_can_delete_comment(
    author_client, comment, comments_url, comment_delete_url
):
    response = author_client.post(comment_delete_url)
    assertRedirects(response, comments_url)
    assert not Comment.objects.filter(pk=comment.pk).exists()
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    reader_client, comment, comment_delete_url
):
    response = reader_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.pk).exists()
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == comment.text
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news
