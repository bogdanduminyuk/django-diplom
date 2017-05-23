from selenium import webdriver

from core.functions import is_url, file_to_url


class SeleniumPhantomJSDriver:
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def execute_script(self, url, script):
        if not is_url(url):
            url = file_to_url(url)

        self.driver.get(url)

        result = self.driver.execute_script(script)

        if 'callPhantom' in result:
            result.remove('callPhantom')

        return result

    def __del__(self):
        self.driver.quit()
