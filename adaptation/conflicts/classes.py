from selenium import webdriver


class SeleniumPhantomJSDriver:
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def execute_script(self, url, script):
        self.driver.get(url)
        result = self.driver.execute_script(script)

        if 'callPhantom' in result:
            result.remove('callPhantom')

        return result

    def __del__(self):
        self.driver.quit()
