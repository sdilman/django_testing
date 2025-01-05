from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.fixture()
def news_url(news_id_args):
    return reverse('news:detail', args=news_id_args)


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, news_url, comment_form_data
):
    client.post(news_url, data=comment_form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author, author_client, news_url, news, comment_form_data
):
    response = author_client.post(news_url, comment_form_data)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_url):
    response = author_client.post(
        news_url,
        {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    author_client, comment, news_url, comment_id_args
):
    new_comment_text = 'Обновлённый комментарий'
    response = author_client.post(
        reverse('news:edit', args=comment_id_args),
        data={'text': new_comment_text}
    )
    assertRedirects(response, news_url + '#comments')
    comment.refresh_from_db()
    assert comment.text == new_comment_text


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment, comment_id_args
):
    comment_text = comment.text
    new_comment_text = 'Обновлённый комментарий'
    response = reader_client.post(
        reverse('news:edit', args=comment_id_args),
        data={'text': new_comment_text}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
