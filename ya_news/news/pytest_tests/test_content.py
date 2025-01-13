from django.urls import reverse
from django.utils import timezone
import pytest

from news.forms import CommentForm
from news.models import Comment, News
from yanews import settings


pytestmark = pytest.mark.django_db


def test_news_count(client, news_collection):
    response = client.get(reverse('news:home'))
    assert response.context['object_list'].count(
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_collection):
    response = client.get(reverse('news:home'))
    news_in_context = [
        news.date for news in response.context['object_list']
    ]
    assert news_in_context == sorted(news_in_context, reverse=True)


def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    comment_timestamps = [
        comment.created for comment in news.comment_set.all()
    ]
    assert comment_timestamps == sorted(comment_timestamps)


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
