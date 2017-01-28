"""
Here I keep all settings about adaptation.

How we adapt, what to adapt and what to do.
"""

# Common definitions

COMMON_REQUIRES_FILES = [
    'description.ini',
]

REQUIRED_DESCRIPTION_KEYS = [
    'css',
    'index.html',
]


# Wordpress definition

WORDPRESS = {
    
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

    'STYLE': {
        'SELECTOR': False,
        'FILE': 'style.css',
        'METHOD_CALL': False,
    },
    
}

