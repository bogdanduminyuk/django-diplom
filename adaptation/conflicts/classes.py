from selenium import webdriver

from adaptation.core.functions import is_url, file_to_url


class SeleniumPhantomJSDriver:
    """Class is interface for Selenium"""
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def execute_script(self, url, script):
        """
        Executes Javascript code in URL

        :param url: URL where to execute
        :param script: string of JS-code
        :return: script result
        """
        if not is_url(url):
            url = file_to_url(url)

        self.driver.get(url)

        result = self.driver.execute_script(script)

        if 'callPhantom' in result:
            result.remove('callPhantom')

        return result

    def __del__(self):
        self.driver.quit()


class ConflictChecker:
    """Global class to check conflicts"""
    def __init__(self):
        self.driver = SeleniumPhantomJSDriver()

    def check(self, src_path, scripts, urls_to_check):
        """
        Realizes checking conflicts.

        :param src_path: path to input file
        :param scripts: dict of scripts to execute on page
        :param urls_to_check: dict of URLs which compare with
        :return: dict of intersection
        """
        theme = {}
        engines = {}
        intersection = {}

        for key, script in scripts.items():
            theme[key] = self.driver.execute_script(src_path, script)

        for engine, url in urls_to_check.items():
            engines[engine] = {}

            for key, script in scripts.items():
                engines[engine][key] = self.driver.execute_script(url, script)

        for engine, data in engines.items():
            intersection[engine] = {}

            for engine_param, engine_value in data.items():
                for theme_param, theme_value in theme.items():
                    intersection[engine][engine_param] = list(set(engine_value) & set(theme_value))

        return intersection
