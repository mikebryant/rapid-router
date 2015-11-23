import os
from selenium import webdriver

SAUCE_URL = "https://%s:%s@ondemand.saucelabs.com/wd/hub" % (
    os.environ.get('SAUCE_USERNAME', ''),
    os.environ.get('SAUCE_ACCESS_KEY', ''),
)


def generate_selenium_capabilities(base_name):
    caps = getattr(webdriver.DesiredCapabilities, base_name).copy()
    caps['build'] = caps['tunnel-identifier'] = os.environ.get('TRAVIS_JOB_NUMBER', '')
    return caps

SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.Firefox,
        'args': (),
        'kwargs': {},
    },
    'remote': {
        'callable': webdriver.Remote,
        'args': (),
        'kwargs': {
            'command_executor': SAUCE_URL, 
            'desired_capabilities': generate_selenium_capabilities(
                os.environ.get(
                    'SELENIUM_REMOTE_DRIVER',
                    'FIREFOX',
                ),
            ),
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
INSTALLED_APPS = ['game']
PIPELINE_ENABLED = False
ROOT_URLCONF = 'django_autoconfig.autourlconf'
STATIC_ROOT = '.tests_static/'

from django_autoconfig.autoconfig import configure_settings
configure_settings(globals())
