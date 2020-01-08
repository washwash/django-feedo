from applications.subscription.models import Subscription
from applications.subscription.service import update_subscriptions
from celery.utils.log import get_task_logger
from applications.async_update.celery import app


logger = get_task_logger(__name__)


@app.task
def update_subscriptions_task():
    subs_for_update = Subscription.objects.all()
    logger.info(f'Subscriptions for update: {subs_for_update}')

    update_subscriptions(subs_for_update)


app.conf.beat_schedule.update({
    'update_subscriptions': {
        'task': 'applications.async_update.tasks.update_subscriptions_task',
        'schedule': 30.0,
    }
})
