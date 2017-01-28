"""
Base settings for my project.
"""

# relative path to file with user options
USER_CONFIG = './user.ini'

# max size of files that can be uploaded. It is equaled 20 Mb.
MAX_UPLOAD_FILE_SIZE = 20971520

CONTENT_TYPES = ['application/octet-stream']


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



