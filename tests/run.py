# -*- coding: utf-8 -*-


from django.conf import settings

import sys
import os

if 'DB_USER' not in os.environ:
    db_user = 'testuser'
else:
    db_user = os.environ['DB_USER']

if 'DB_NAME' not in os.environ:
    db_name = 'django_postgresql_test'
else:
    db_name = os.environ['DB_NAME']

if 'DB_PORT' not in os.environ:
    db_port = '5432'
else:
    db_port = os.environ['DB_PORT']

if 'DB_DRIVER' in os.environ:
    db_driver = os.environ['DB_DRIVER']
else:
    db_driver = 'django_orm.backends.postgresql_psycopg2'


test_settings = {
    'DATABASES': {
        'default': {
            'ENGINE': db_driver,
            'USER': db_user,
            'NAME': db_name,
            'HOST': '',
            'PORT': db_port,
        }
    },
    #'INSTALLED_APPS': [
    #    'tests.hstore_app',
    #    'tests.unaccent_app',
    #    'tests.fts_app',
    #    'tests.pgcomplex_app',
    #],
    'ROOT_URLCONF': 'tests.test_app.urls',
    'LOGGING': {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console':{ 'level':'DEBUG', 'class':'logging.StreamHandler'}
        },
        'loggers': {
            'django': {
                'handlers':['null'],
                'propagate': False,
                'level':'INFO',
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            }
        }
    }
}

if __name__ == '__main__':
    test_args = sys.argv[1:]
    if not test_args:
        if "postgresql" in db_driver:
            test_settings['INSTALLED_APPS'] = [
                'tests.hstore_app',
                'tests.unaccent_app',
                'tests.fts_app',
                'tests.pgcomplex_app',
            ]
            test_args = ['hstore_app', 'unaccent_app', 'fts_app', 'pgcomplex_app',]

        elif "mysql" in db_driver:
            test_settings['INSTALLED_APPS'] = [
                'tests.unaccent_app',
            ]
            test_args = ['unaccent_app']

    current_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    sys.path.insert(0, current_path)
    if not settings.configured:
        settings.configure(**test_settings)

    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=2, interactive=True, failfast=False)
    failures = runner.run_tests(test_args)
    sys.exit(failures)
