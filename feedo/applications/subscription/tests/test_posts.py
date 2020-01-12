from django.urls import reverse

from applications.subscription.models import Post
from applications.subscription.tests.factories import PostFactory


HTTP_200_OK = 200
HTTP_302_REDIRECT = 302
HTTP_404_NOT_FOUND = 404


def test_post_list(user_logged_client, user):
    for _ in range(3):
        PostFactory()

    for _ in range(3):
        PostFactory(user=user)

    url = reverse('subscription:post_list_view')
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_200_OK
    assert (
        set(response.context_data['object_list']) ==
        set(Post.objects.filter(user=user))
    )


def test_post_detail(user_logged_client, user):
    post_out_of_view = PostFactory()
    post_in_view = PostFactory(user=user)

    url = reverse(
        'subscription:post_detail_view',
        kwargs={'pk': post_in_view.pk}
    )
    response = user_logged_client.get(url)

    assert (
        set([response.context_data['object'], ]) ==
        set(Post.objects.filter(user=user))
    )

    url = reverse(
        'subscription:subscription_detail_view',
        kwargs={'pk': post_out_of_view.pk}
    )
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND


def test_post_mark_as_read(user_logged_client, user):
    post = PostFactory(user=user, is_read=False)
    assert not post.is_read

    url = reverse('subscription:post_detail_view', kwargs={'pk': post.pk})
    user_logged_client.get(url)

    post.refresh_from_db()
    assert post.is_read


def test_post_update(user_logged_client, user):
    post = PostFactory(
        user=user,
        is_favourite=False,
        comment=''
    )
    assert not post.is_favourite
    assert post.comment == ''

    url = reverse('subscription:post_update_view', kwargs={'pk': post.pk})
    data = {
        'is_favourite': True,
        'comment': 'COMMENT'
    }
    response = user_logged_client.post(url, data, follow=True)
    assert response.status_code == HTTP_200_OK

    post.refresh_from_db()
    assert post.is_favourite == data['is_favourite']
    assert post.comment == data['comment']

    assert response.context_data['object'].is_favourite == data['is_favourite']
    assert response.context_data['object'].comment == data['comment']


def test_post_new(user_logged_client, user):
    for _ in range(2):
        PostFactory(user=user, is_read=True)

    for _ in range(3):
        PostFactory(user=user, is_read=False)

    url = reverse('subscription:post_new_view')
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.context_data['object_list'].count() == 3
    assert (
        set(response.context_data['object_list']) ==
        set(Post.objects.filter(user=user, is_read=False))
    )


def test_post_favourites(user_logged_client, user):
    for _ in range(3):
        PostFactory(user=user, is_favourite=False)

    for _ in range(2):
        PostFactory(user=user, is_favourite=True)

    url = reverse('subscription:post_favourites_view')
    response = user_logged_client.get(url)
    assert response.status_code == HTTP_200_OK
    assert response.context_data['object_list'].count() == 2
    assert (
        set(response.context_data['object_list']) ==
        set(Post.objects.filter(user=user, is_favourite=True))
    )
