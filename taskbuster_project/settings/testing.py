# -*- coding: utf-8 -*-

# remember to editd
# $VIRTUAL_ENV/bin/postactivate and
# $VIRTUAL_ENV/bin/predeactivate
# for each enviroment

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# for google app testing database doesn’t have a 
# Google App defined
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

#  This will allow us to create fixtures from this testing
# database anytime we want to.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}