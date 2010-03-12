# -*- coding: utf-8 -*-
import os
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

#CACHE_BACKEND = 'locmem:///'

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'cms.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

MEDIA_ROOT = STATIC_ROOT = os.path.join(PROJECT_DIR,'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'media', 'static')
STATIC_URL = MEDIA_URL + 'static/'

# Absolute path to the directory that holds pages media.
PAGES_MEDIA_ROOT = os.path.join(STATIC_ROOT, 'pages', 'media', 'pages')
# Absolute path to the directory that holds media.
ADMIN_MEDIA_PREFIX = '/admin_media/'

#FIXTURE_DIRS = [os.path.join(PROJECT_DIR, 'fixtures')]

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*xq7m@)*f2awoj!spa0(jibsrz9%c0d=e(g)v*!17y(vx0ue_3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "pages.context_processors.media",
    #"staticfiles.context_processors.static_url",
)

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'myproject.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'templates'),
)

#CACHE_BACKEND = "locmem:///?timeout=300&max_entries=6000"

#PAGE_CONTENT_CACHE_DURATION = 300

INSTALLED_APPS = (
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.markup',
    'tagging',
    'pages',
    'mptt',
    'tinymce',
    'staticfiles',
    'filebrowser',
    'google_analytics',
    'django_markup',
)

INSTALLED_APPS += (
    'myproject.news',
    'sorl.thumbnail',
    'myproject.events',
    'myproject.links',
    'myproject.sermons',
    'myproject.utils',
    'myproject.pictures',
    'dpress',
)

EVENTS_MONTH_IN_LIST = 3

PAGE_TINYMCE = True

# Default language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s

# languages you want to translate into the CMS.
PAGE_LANGUAGES = (
    ('en-us', gettext_noop('US English')),
)
languages = list(PAGE_LANGUAGES)
LANGUAGES = languages

DEFAULT_PAGE_TEMPLATE = 'pages/index.html'

PAGE_TEMPLATES = (
    ('pages/nice.html', 'nice one'),
    ('pages/cool.html', 'cool one'),
    ('pages/editor.html', 'raw editor'),
    ('pages/home.html', 'Home Page'),
)

PAGE_SANITIZE_USER_INPUT = True

PAGE_CONNECTED_MODELS = [{
        'model':'pictures.models.GalleryPage',
        'form':'pictures.forms.GalleryPageForm',
        'options':{
                    'extra': 1,
                    'max_num': 1,
                  },
},]

URCHIN_ID = 'sdasdasdad'

FILEBROWSER_URL_FILEBROWSER_MEDIA = MEDIA_URL + 'filebrowser/'
FILEBROWSER_URL_WWW = MEDIA_URL + 'uploads/'

PREFIX_URL = ''#dpress/

FILEBROWSER_URL_ADMIN = '/%sadmin/filebrowser/' % PREFIX_URL
FILEBROWSER_URL_HOME = '/%sadmin/' % PREFIX_URL

SYNTAXHIGHLIGHTER_JS_URL = MEDIA_URL + 'syntaxhighlighter/'

TEMPLATE_DIRS += (
       os.path.join(PROJECT_DIR,'templates','diy_sample'),
              os.path.join(PROJECT_DIR,'templates','default'),
              )

BLOG_CONFIG = {'title': u'DPress',
        'sub_title': u'Blog Sub Title',
                        'blog_simple_descn': u'Blog Simple Descn',
                                                'End': ''}

