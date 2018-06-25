from . import *


DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['makavaf.al']


# Slack

SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')

SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')

SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN')

SLACK_BOT_USER_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN')
