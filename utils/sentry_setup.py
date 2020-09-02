import os
import logging
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


def setup_sentry(dsn, app_env, release=None, **kwargs):
    if dsn:
        print("init_sentry: {}, {}, {}".format(dsn, app_env, release))
    else:
        print("SENTRY_DSN not set, sentry is not configured")
        return

    debug = True if os.environ.get("SENTRY_DEBUG") else False

    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.WARN),
            CeleryIntegration(),
        ],
        environment=app_env,
        release=release,
        debug=debug,
        **kwargs
    )
    # ignore_logger('weasyprint')
