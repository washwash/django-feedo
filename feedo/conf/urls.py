from django.urls import path, include


urlpatterns = [
    path(
        '',
        include(
            ('applications.index.urls', 'index'),
            namespace='index'
        )
    ),
    path(
        'accounts/',
        include(
            ('applications.authentication.urls', 'authentication'),
            namespace='authentication'
        )
    ),
    path(
        'subscriptions/',
        include(
            ('applications.subscription.urls', 'subscription'),
            namespace='subscription'
        )
    ),
]
