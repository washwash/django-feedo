from celery.utils.log import get_task_logger

from applications.async_update.celery import app
from applications.feed.service import (
    update_feeds, get_feeds_for_update
)
from applications.subscription.service import (
    update_subscriptions,
    get_subscriptions_for_update
)


logger = get_task_logger(__name__)


@app.task
def update_subscriptions_task():
    feeds_for_update = get_feeds_for_update()
    logger.info(f'Feeds for update: {feeds_for_update}')
    update_feeds(feeds_for_update)

    subs_for_update = get_subscriptions_for_update()
    logger.info(f'Subscriptions for update: {subs_for_update}')
    update_subscriptions(subs_for_update)


app.conf.beat_schedule.update({
    'update_subscriptions': {
        'task': 'applications.async_update.tasks.update_subscriptions_task',
        'schedule': 60.0,
    }
})
