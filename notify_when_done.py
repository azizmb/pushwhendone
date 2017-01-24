import os
import traceback
import uuid

from datetime import datetime
from contextlib import contextmanager

import pynotify
import requests


@contextmanager
def notify(title='process', token=None):
    title = '%s (%s)' % (title, str(uuid.uuid4())[:8])

    if not token:
        try:
            token = os.environ['PUSHBULLET_ACCESS_TOKEN']
        except KeyError:
            raise Exception('Access token not provided or set')

    headers = {
        'Access-Token': token
    }

    start_time = datetime.now()

    pynotify.init(title)

    start_title = '[%s] Started at %s' % (title, start_time)
    start_body = 'Started at %s' % (start_time)

    start_push = {
        'body': start_body,
        'title': start_title,
        'type': 'note'
    }
    response = requests.post(
        'https://api.pushbullet.com/v2/pushes',
        json=start_push,
        headers=headers
    )
    response.raise_for_status()

    notification = pynotify.Notification(start_title, start_body)
    notification.show()

    try:
        yield
    except:
        end_time = datetime.now()
        error_body = traceback.format_exc()
        error_title = '[%s] Error, stopped at %s' % (title, end_time)
        error_push = {
            'body': traceback.format_exc(),
            'title': end_title,
            'type': 'note'
        }

        response = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            json=error_push,
            headers=headers
        )

        response.raise_for_status()

        notification = pynotify.Notification(error_title, error_body)
        notification.show()

        raise
    else:
        end_time = datetime.now()

        end_body = 'Finished %s\nStart Time: %s\nTime Taken: %s' % (end_time, start_time, (end_time-start_time))
        end_title = '[%s] Finished at %s' % (title, end_time)
        end_push = {
            'body': end_body,
            'title': end_title,
            'type': 'note'
        }

        response = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            json=end_push,
            headers=headers
        )
        response.raise_for_status()

        notification = pynotify.Notification(end_title, end_body)
        notification.show()
