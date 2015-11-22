from selenium import webdriver

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
INSTALLED_APPS = ['game']
PIPELINE_ENABLED = False
ROOT_URLCONF = 'django_autoconfig.autourlconf'
STATIC_ROOT='.tests_static/'

SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.Firefox,
        'args': (),
        'kwargs': {},
    }
}

from django_autoconfig.autoconfig import configure_settings
configure_settings(globals())
