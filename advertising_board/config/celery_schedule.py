from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'weekly_notifier': {
        'task': 'subscription.tasks.NotificationUserNewAds',
        'schedule': crontab(day_of_week='monday', hour=0, minute=0),
        'kwargs': {
            'delta': {'days': 7}
        }
    },

    'monthly_notifier': {
        'task': 'subscription.tasks.NotificationUserNewAds',
        'schedule': crontab(day_of_month='1', hour='00', minute='00'),
        'kwargs': {
            'delta': {'days': 31}
        }
    },
}


'''
'every_30_seconds': {
        'task': 'subscription.tasks.NotificationUserNewAds',
        'schedule': 30,
        'kwargs': {
            'delta': {'days': 6}
        }
    },
'''
