import json

from adaptation import settings as adapt_settings
from diplom import settings as global_settings


class ConflictSettings:
    SECTION = "CONFLICTS"

    @staticmethod
    def get_script():
        with open(adapt_settings.JS_SCRIPT, "r", encoding="utf-8") as js_script:
            return js_script.read()

    @staticmethod
    def get_user_cfg():
        with open(global_settings.USER_CONFIG, 'r', encoding='utf-8') as cfg:
            parsed = json.loads(cfg.read())
            return parsed[ConflictSettings.SECTION]
