from . import *


DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['pizzabot.makavaf.al']


# Slack

SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')

SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')

SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN')

SLACK_BOT_USER_TOKEN = os.environ.get('SLACK_BOT_USER_TOKEN')


# Rollbar

ROLLBAR_ACCESS_TOKEN = os.environ.get("ROLLBAR_ACCESS_TOKEN")

if ROLLBAR_ACCESS_TOKEN:
    ROLLBAR = {
        'access_token': ROLLBAR_ACCESS_TOKEN,
        'environment': 'production',
        'branch': 'master',
        'root': PROJECT_ROOT,
    }

    MIDDLEWARE += ['rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404']

    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'rollbar.contrib.django_rest_framework.post_exception_handler'
else:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("'ROLLBAR_ACCESS_TOKEN' must be set")
