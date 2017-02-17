"""
Here I keep all settings about adaptation.

How we adapt, what to adapt and what to do.
"""

# Common definitions

DESCRIPTION_FILE = 'description.json'

COMMON_REQUIRES_FILES = [
    DESCRIPTION_FILE,
]

REQUIRED_DESCRIPTION_KEYS = [
    'css',
    'index',
]

# Handled CMS

CMS = ['WordPress', 'Joomla']


# Wordpress definition

WORDPRESS = {
    "PREPARATION": {
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
    "PREPARATION": {
        "TEMPLATE_STRUCTURE": {
            "css": {
                "template.css": "{content}",
                "index.html": "<!DOCTYPE html><title></title>"
            },

            "images": {
                "index.html": "<!DOCTYPE html><title></title>"
            },

            "language": {
                "{language}": {
                    "{language}.tpl_{theme_name}.ini": "{}",
                    "{language}.tpl_{theme_name}.sys.ini": "TPL_WHITESQUARE_XML_DESCRIPTION=\"{xml_description}\"",
                }
            },

            "files": {
                "component.php": "{content}",
                "error.php": "{content}",
                "index.php": "{content}",
                "templateDetails.xml": "{content}"
            },
        }
    },
}

