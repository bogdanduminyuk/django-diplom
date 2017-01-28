"""
Base settings for my project.
"""

# relative path to file with user options
USER_CONFIG = './user.ini'

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
