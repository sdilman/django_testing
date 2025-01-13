from datetime import datetime, timedelta
import pytest

from django.urls import reverse
from django.utils import timezone

from news.forms import CommentForm
from news.models import News, Comment
from yanews import settings


pytestmark = pytest.mark.django_db


@pytest.fixture
def news_collection():
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_collection(news, author):
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.mark.usefixtures('news_collection')
def test_news_count(client):
    response = client.get(reverse('news:home'))
    assert response.context['object_list'].count(
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('news_collection')
def test_news_order(client):
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
