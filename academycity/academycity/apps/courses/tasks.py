from celery import task
from ..core import email


@task
def asy_email_message(semail, subject=None, body=None):
    email.email_message(semail, subject=subject, body=body)
    return 'ok'

