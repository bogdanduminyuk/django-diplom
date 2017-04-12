"""
Base settings for my project.
"""

# SELECTORS is dict of css-selectors that system use to parsing content blocks
SELECTORS = {
    'header': '#page-header',
    'footer': '#page-footer',
    'logo': '#page-logo',
    'menu': '#page-menu',
    'content': '#page-content',
    'nav': '#page-nav',
    'aside': '#page-aside',
    'left': '#page-left',
    'right': '#page-right',
}

TAGS = {
    "a": {
        "attribute": "href",
    },

    "link": {
        "attribute": "href",
    },

    "script": {
        "attribute": "src",
    },

    "img": {
        "attribute": "src",
    },
}



