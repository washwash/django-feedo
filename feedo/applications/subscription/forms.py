from django import forms
from django.contrib.auth import get_user_model

from applications.feed.models import Feed
from applications.subscription.models import Subscription, Post


class SubscriptionCreationForm(forms.ModelForm):
    source = forms.URLField(
        required=True
    )
    feed = forms.ModelChoiceField(
        Feed.objects,
        required=False
    )
    user = forms.ModelChoiceField(
        get_user_model().objects.all(),
        required=True
    )

    def clean_feed(self):
        feed, _ = Feed.objects.get_or_create(
            source=self.data['source']
        )
        return feed

    class Meta:
        model = Subscription
        fields = ('user', 'feed', )


class PostUpdateForm(forms.ModelForm):
    is_favourite = forms.BooleanField(
        required=False
    )
    comment = forms.CharField(
        required=False
    )

    class Meta:
        model = Post
        fields = ('comment', 'is_favourite')


class PostIsFavouriteForm(forms.ModelForm):
    is_favourite = forms.BooleanField(
        required=False
    )

    class Meta:
        model = Post
        fields = ('is_favourite', )
