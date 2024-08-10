from huey import crontab
from huey.contrib.djhuey import db_periodic_task



@db_periodic_task(crontab(minute='*/5'))
def echo_task():
    print('echo')
