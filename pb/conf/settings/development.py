from . import *

DEBUG = True

SECRET_KEY = 'such secret'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Slack

SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')

SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')

SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN')

SLACK_BOT_USER_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN')
