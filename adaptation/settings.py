"""
Here I keep all settings about adaptation.

How we adapt, what to adapt and what to do.
"""
import os

from django.conf import settings

# TODO: finish joomla
# TODO: add selectors (common)

STATIC_CMS_ROOT = os.path.join(settings.BASE_DIR, 'adaptation', '{package}', 'static')

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
    },

    "FILES": {
        "footer.php": "{footer}",
        "header.php": "{header}",
        "index.php": "{wp_index}",
        "style.css": "{content}",
    },
}


# joomla definition
JOOMLA = {
    "PREPARATION": {
        "STYLES": {
            "format_name": "head_styles",
            "template": "$doc->addStyleSheet($template_url . '/{stylesheet}');",
            "has_rel": "stylesheet"
        },

        "TAGS_ATTACHMENT": [
            {
                "attribute": "src",
                "tags": ["script", "img"],
                "template": "<?php echo $template_url;?>/{old_path}",
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
        "component.php": "{content}",
        "error.php": "{content}",
        "index.php": "{content}",
        "templateDetails.xml": "{content}",
    },

    "XML_DESCRIPTION": {
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


