"""
Here I keep all settings about adaptation.

How we adapt, what to adapt and what to do.
"""
import os

from django.conf import settings


STATIC_CMS_ROOT = os.path.join(settings.BASE_DIR, 'adaptation', 'plugins', '{package}', 'static')
TEMPLATES_ROOT = os.path.join(STATIC_CMS_ROOT, 'tpl')
JS_SCRIPT = os.path.join(settings.BASE_DIR, 'adaptation', 'conflicts', 'get_functions.txt')

CMS = ['WordPress', 'Joomla']


# definition of page parts

PAGE_PARTS = {
    "header": {
        "SELECTOR": "#page-header",
    },

    "footer": {
        "SELECTOR": "#page-footer",
    },

    "body": {
        "SELECTOR": "body"
    },

    "nav": {
        "SELECTOR": "#page-nav"
    }
}

PAGE_ELEMENTS = ["a", "link", "script", "img"]


# Wordpress definition
WORDPRESS = {
    "PREPARATION": {
        "TAGS_ATTACHMENT": [
            {
                "attribute": "src",
                "tags": ["script", "img"],
                "template": "<?php echo get_template_directory_uri();?>/{old_path}",
            },
            {
                "attribute": "href",
                "tags": ["link"],
                "template": "<?php echo get_template_directory_uri();?>/{old_path}"
            },
        ],

        "REPLACEMENT": [
            {
                "page-part": "nav",
                "params": "['menu'=>'{menu_name}', 'menu_class'=>'{menu_class}', 'menu_id'=>'{menu_id}']",
                "template": "<?php echo wp_nav_menu({params}); ?>"
            },
        ],
    },

    "FILES": {
        "footer.php": "{footer}",
        "header.php": "{header}",
        "index.php": "{wp_index}",
        "style.css": "{content}",
        "page.php": "{page.php.tpl}"
    },
}


# joomla definition
JOOMLA = {
    "PREPARATION": {
        "STYLES": {
            "format_name": "head_styles",
            "template": "$doc->addStyleSheet($template_url . '/{}');",
            "has_rel": "stylesheet"
        },

        "SCRIPTS": {
            "format_name": "head_scripts",
            "template": "$doc->addScript($template_url . '/{}');"
        },

        "TAGS_ATTACHMENT": [
            {
                "parent": "body",
                "tags": ["img", "script"],
                "template": "<?php echo $template_url;?>/{old_path}",
            },
        ],

        "REPLACEMENT": [
            {
                "page-part": "nav",
                "template": "<jdoc:include type=\"modules\" id=\"page-nav\"/>"
            },
        ],
    },

    "FILES": {
        # with dirs
        "css/index.html": "<!DOCTYPE html><title></title>",
        "images/index.html": "<!DOCTYPE html><title></title>",

        "js/index.html": "<!DOCTYPE html><title></title>",

        "language/{language}/{language}.tpl_{name}.ini": "",
        "language/{language}/{language}.tpl_{name}.sys.ini": 'TPL_WHITESQUARE_XML_DESCRIPTION="{xml_description}"',

        # clear files
        "component.php": "",
        "error.php": "",
        "index.php": "",
    },

    "XML_DESCRIPTION": {
        "path": "templateDetails.xml",
        "base": {
            "name": "extension",
            "attributes": {"version": "1.0", "type": "template", "client": "site"}
        },

        "tags": {
            "description": {"text": "TPL_WHITESQUARE_XML_DESCRIPTION"},
            "files": "",
            "positions": "",
            "languages": {"attributes": {"folder": "language"}},
        },

        "form_data": {
            "excluded": ["form", "file"]
        }
    }
}


