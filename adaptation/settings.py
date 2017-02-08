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


# styles template for str.format

STYLES = """/*
Theme Name: {0}
Author: {1}
Description: {2}
Version: {3}
License: {4}
Tags: {5}

{6}
*/

{7}
"""

