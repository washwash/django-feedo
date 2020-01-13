# Feedo
Simple RSS reader.


## Explanation
This is a pretty simple backend for RSS readers based on classic Django template backend, because
frontend is not my strong suit.
Of course, it should be done as beautiful SPA with elegant REST API with Django REST,
and probably I will rewrite it in this way someday.

So, we have three main parts:
* [Feeds](#feed)
* [Subscriptions](#subscription)
* [Async operations](#async-operations)

### Feed
Feed is bound with RSS sources and their items or entries.
Each Feed stores information about `source`, `date of updating` and `fail counts`.
Feeds are `updated automatically`, and if try has been unsuccessful, fail count is increased.
After some failed tries Feddo `stops to update` that Feed.

All RSS entries are stored in Item model. Item represents real world RSS item
and is not bound with users' items (Posts).


### Subscription
Every User has its own subscription on some feed.
Subscription is a place where User and Feed are meeting. In other words,
User read the feeds through the subscriptions.
For example, `https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml`
Everyone loves technology, right? 1000000 Users are able to subscribe on NYT and
that means there are only 1 Feed (NYT RSS) and 1000000 Subs for the different Users!
User can delete Sub, but not Feed. Also, we can use Subscription model more widely.

Posts allow User to read the news. User can leave a `comment` or mark Post as `favourite`.
User can see All, `New` and Favourites posts in the different lists.
Post gets a `read` mark if user goes to the post page in Feedo (detail view).
If User adds a subscription to existing feed, all old posts will appear immediately
and will be marked as read.

User can `try to update` inactive Subscription manually.


### Async operations
All automatically updates of feed are executed by Celery and Celery Beat.
The task grabs all active Feeds, tries to get fresh Items.
Then, goes through all Subscriptions and tries to create new Users' Posts.


## Installation
Easy peasy lemon squeezy, but here is the thing - Docker and Docker Compose
should be installed. Pls, check the [Starred](#starred) section.

Okay, now run three commands:
```
git clone https://github.com/washwash/django-feedo.git
cd django-feedo/
docker-compose up
```
_beep beep boop beep boop_

After that, open another terminal tab and run
```
docker ps --format '{{.Names}}'
```
Everything is okay if you can see something like that
```
>docker ps --format '{{.Names}}'
djangofeedo_nginx_1
djangofeedo_celery_1
djangofeedo_application_1
djangofeedo_db_1
djangofeedo_rabbit_1
```

Now, open a browser and get the Feedo on 127.0.0.1!


## Testing
Just build `feedo` and `db` containers and run `test`
```
docker-compose run test
```
Feedo has simple test cases now, which implemented as functions, because it's enough in the moment.
If it will grow - I will rewrite it with TestCase classes and shared methods or helpers.

## Starred:
_or it works on my local machine_
* Python 3.6.8
* Docker 17.12.0-ce
* docker-compose 1.17.0
* Ubuntu 16.04


## License
[MIT](https://github.com/washwash/django-feedo/blob/master/LICENSE)

