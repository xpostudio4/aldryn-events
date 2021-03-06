#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import imp

from distutils.version import LooseVersion
from cms import __version__ as cms_string_version

cms_version = LooseVersion(cms_string_version)


def noop_gettext(s):
    return s

gettext = noop_gettext


HELPER_SETTINGS = {
    'TIME_ZONE': 'UTC',
    'INSTALLED_APPS': [
        'aldryn_apphook_reload',  # for tests
        'aldryn_apphooks_config',
        'aldryn_common',
        'aldryn_reversion',
        'aldryn_translation_tools',
        'reversion',
        'appconf',
        'bootstrap3',
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'extended_choices',
        'filer',
        'mptt',
        'parler',
        'sortedm2m',
        'standard_form',
    ],
    'CMS_PERMISSION': True,
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
    ),
    'PARLER_LANGUAGES': {
        1: [
            {
                'code': u'en',
                'fallbacks': [u'de'],
                'hide_untranslated': False
            },
            {
                'code': u'de',
                'fallbacks': [u'en'],
                'hide_untranslated': False
            }
        ],
        'default': {
            'code': u'en',
            'fallbacks': [u'en'],
            'hide_untranslated': False}
    },
    'PARLER_ENABLE_CACHING': False,
    'CMS_LANGUAGES': {
        'default': {
            'public': True,
            'hide_untranslated': False,
            'fallbacks': ['en']

        },
        1: [
            {
                'public': True,
                'code': 'en',
                'fallbacks': [u'de'],
                'hide_untranslated': False,
                'name': gettext('en'),
                'redirect_on_fallback': True,
            },
            {
                'public': True,
                'code': 'de',
                'fallbacks': [u'en'],
                'hide_untranslated': False,
                'name': gettext('de'),
                'redirect_on_fallback': True,
            },
        ],
    },
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
    'DEBUG': True,
    # 'TEMPLATE_DEBUG': True,
    'ALDRYN_EVENTS_USER_REGISTRATION_EMAIL': True,
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    },
    'MIDDLEWARE_CLASSES': [
        # NOTE: This will actually be removed below in CMS<3.2 installs.
        'cms.middleware.utils.ApphookReloadMiddleware',
        'django.middleware.http.ConditionalGetMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware'
    ]
}

# tablib does not supports py2.6/django1.6
try:
    imp.find_module('django_tablib')
    HELPER_SETTINGS['INSTALLED_APPS'].append('django_tablib')
except ImportError:
    pass


# If using CMS 3.2+, use the CMS middleware for ApphookReloading, otherwise,
# use aldryn_apphook_reload's.
if cms_version < LooseVersion('3.2.0'):
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'].remove(
        'cms.middleware.utils.ApphookReloadMiddleware')
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'].insert(
        0, 'aldryn_apphook_reload.middleware.ApphookReloadMiddleware')


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_events', extra_args=[])

if __name__ == "__main__":
    run()
