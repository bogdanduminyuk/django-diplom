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

