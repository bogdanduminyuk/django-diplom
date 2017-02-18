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


# Wordpress definition

WORDPRESS = {
    "PREPARATION": {
        "TEMPLATE_STRUCTURE": {
            "css/style.css": "{content}",

            "images/index.html": "<!DOCTYPE html><title></title>",

            "js/index.html": "<!DOCTYPE html><title></title>",

            "footer.php": "{content}",
            "header.php": "{content}",
            "index.php": "{content}",
            "style.php": "{content}",
        },

        "RELATIVES": {
            "get_template_directory_uri()": {
                'href': ['link'],
                'src': ['script', 'img'],
            },
        }
    },

    'INDEX': {
        'HEADER': {
            'SELECTOR': '#page-header',
            'FILE': 'header.php',
            'METHOD_CALL': 'get_header()',
        },

        'FOOTER': {
            'SELECTOR': '#page-footer',
            'FILE': 'footer.php',
            'METHOD_CALL': 'get_footer()',
        },
    },

    'STYLE': {
        'SELECTOR': False,
        'FILE': 'style.css',
        'METHOD_CALL': False,
        'CONTENT': "/*Theme Name: {0}\nAuthor: {1}\nDescription: {2}\nVersion: {3}\nLicense: {4}\nTags: {5}\n{6}\n*/\n\n{7}",
    },
}

JOOMLA = {
    # key - description key, value - CMS folder name
    "DIR_NAMES": {
        "images": "images",
        "css": "css",
        "js": "js",
    },

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

