import os
import traceback
from datetime import datetime
from contextlib import contextmanager

import requests


@contextmanager
def pushwhendone(title='process', token=None):
    if not token:
        try:
            token = os.environ['PUSHBULLET_ACCESS_TOKEN']
        except KeyError:
            raise Exception('Access token not provided or set')

    headers = {
        'Access-Token': token
    }

    start_time = datetime.now()

    start_push = {
        'body': 'Started %s at %s' % (title, start_time),
        'title': 'Started %s at %s' % (title, start_time),
        'type': 'note'
    }
    response = requests.post(
        'https://api.pushbullet.com/v2/pushes',
        json=start_push,
        headers=headers
    )
    response.raise_for_status()

    try:
        yield
    except:
        end_time = datetime.now()

        end_push = {
            'body': traceback.format_exc(),
            'title': 'Error in %s, stopped at %s' % (title, end_time),
            'type': 'note'
        }

        response = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            json=end_push,
            headers=headers
        )
        response.raise_for_status()
        raise
    else:
        end_time = datetime.now()

        end_push = {
            'body': 'Finished %s at %s\nStart Time: %s\nTime Taken: %s' % (title, end_time, start_time, (end_time-start_time)),
            'title': 'Finished %s at %s' % (title, end_time),
            'type': 'note'
        }

        response = requests.post(
            'https://api.pushbullet.com/v2/pushes',
            json=end_push,
            headers=headers
        )
        response.raise_for_status()
