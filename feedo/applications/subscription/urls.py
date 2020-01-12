from django.urls import path

from .views import (
    subscriptions_list,
    subscriptions_detail,
    subscriptions_update_feed,
    subscriptions_delete,
    subscriptions_create,

    post_detail,
    post_update,
    post_list,
    post_list_new,
    post_favourites
)

urlpatterns = [
    path(
        '',
        subscriptions_list,
        name='subscription_list_view'
    ),
    path(
        '<pk>/detail/',
        subscriptions_detail,
        name='subscription_detail_view'
    ),
    path(
        '<pk>/update/feed/',
        subscriptions_update_feed,
        name='subscription_update_feed_view'
    ),
    path(
        '<pk>/delete/',
        subscriptions_delete,
        name='subscription_delete_view'
    ),
    path(
        'create/',
        subscriptions_create,
        name='subscription_create_view'
    ),

    path(
        'posts/',
        post_list,
        name='post_list_view'
    ),
    path(
        'posts/<pk>/detail/',
        post_detail,
        name='post_detail_view'
    ),
    path(
        'posts/<pk>/update/',
        post_update,
        name='post_update_view'
    ),
    path(
        'posts/favourites/',
        post_favourites,
        name='post_favourites_view'
    ),
    path(
        'posts/new/',
        post_list_new,
        name='post_new_view'
    )
]
