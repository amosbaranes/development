from celery import Celery
app = Celery(
  broker='amqp://user:password@localhost:5672',
  include=['tasks'])

app.conf.beat_schedule = {
  'refresh': {
    'task': 'refresh',
    'schedule': 300.0,
    'args': ([
      'https://www.theguardian.com',
      'https://www.nytimes.com'
    ],),
}