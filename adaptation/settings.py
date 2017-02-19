"""
Here I keep all settings about adaptation.

How we adapt, what to adapt and what to do.
"""
import os

from django.conf import settings


# Common definitions

DESCRIPTION_FILE = 'description.json'

COMMON_REQUIRES_FILES = [
    DESCRIPTION_FILE,
]

REQUIRED_DESCRIPTION_KEYS = [
    'images',
    'css',
    'index',
]

STATIC_CMS_ROOT = os.path.join(settings.BASE_DIR, 'adaptation', '{form}', 'static')


# Handled CMS

CMS = ['WordPress', 'Joomla']


# definition of page parts

PAGE_PARTS = {
    "header": {
        "SELECTOR": "#page-header",
    },

    "footer": {
        "SELECTOR": "#page-footer",
    },
}


# Wordpress definition

WORDPRESS = {
    "PREPARATION": {

        "METHODS": {
            "get_template_directory_uri()": {
                # attr : tags of attr
                "href": ['link'],
                "src": ["script", "img"]
            },
        },
    },

    "FILES": {
        "footer.php": "{content}",
        "header.php": "{content}",
        "index.php": "{content}",
        "style.php": "{content}",
    },
}


# joomla definition

JOOMLA = {
    "FILES": {
        # with dirs
        "css/index.html": "<!DOCTYPE html><title></title>",
        "images/index.html": "<!DOCTYPE html><title></title>",

        "js/index.html": "<!DOCTYPE html><title></title>",

        "language/{language}/{language}.tpl_{name}.ini": "",
        "language/{language}/{language}.tpl_{name}.sys.ini": 'TPL_WHITESQUARE_XML_DESCRIPTION="{xml_description}"',

        # clear files
        "component.php": "{content}",
        "error.php": "{content}",
        "index.php": "{content}",
        "templateDetails.xml": "{content}",
    },
}

