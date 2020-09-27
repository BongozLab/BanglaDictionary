import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import  Proxy,ProxyType
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from dictscraper.proxy import ProxyInfo



class Browser:
    # logger = logging.getLogger('django.project.requests')
    selenium_retries = 0

    def __init__(self,proxyUse):
        self.proxyUse = proxyUse
        if self.proxyUse == 1:
            # self.ProxyPort= "202.65.171.67:8080"
            self.ProxyPort = ProxyInfo().getProxy()

    def get_option(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()

        options = FirefoxOptions()
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--headless")
        # options.add_argument('ignore-certificate-errors')
        # options.add_argument('--disable—gpu')
        # options.add_argument(f'user—agent={user_agent}')
        # return options
    #
    def get_proxy(self):
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": self.ProxyPort,
            "ftpProxy": self.ProxyPort,
            "sslProxy": self.ProxyPort
        }
        return firefox_capabilities


    def getBrowser(self):
        try:
            # Logger('browser').INFO('Request for new browser')
            dir_path = os.path.dirname(os.path.realpath(__file__))
            BROWSER_EXE = 'C:\Program Files\Mozilla Firefox\firebox.exe'
            GECKODRIVER = dir_path + '\geckodriver.exe'
            print(GECKODRIVER)
            FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)
            # service = webdriver.firefox.service.Service('geckodriver', port=1234)
            # Logger('browser').INFO('Firefox exe path: '+ BROWSER_EXE)
            # Logger('browser').INFO('GECKODRIVER Path: ' + GECKODRIVER)
            PROFILE = webdriver.FirefoxProfile()
            PROFILE.set_preference("dom.webnotifications.enabled", False)
            PROFILE.set_preference("app.update.enabled", False)
            PROFILE.set_preference("browser.link.open_newwindow", 3)
            PROFILE.set_preference("browser.link.open_newwindow.restriction", 2)
            PROFILE.set_preference("browser.cache.disk.enable", False)
            PROFILE.set_preference("browser.cache.memory.enable", False)
            PROFILE.set_preference("browser.cache.offline.enable", False)
            PROFILE.set_preference("network.http.use-cache", False)
            # PROFILE.set_preference("network.proxy.type", 1)
            # PROFILE.set_preference("network.proxy.http", "proxy.server.address")
            # PROFILE.set_preference("network.proxy.http_port", "port_number")
            PROFILE.update_preferences()

            options = self.get_option()
            if self.proxyUse == 1:
                capabilities =  self.get_proxy()
                browser = webdriver.Firefox(executable_path=GECKODRIVER, firefox_binary=FIREFOX_BINARY,
                                        firefox_profile=PROFILE,options=options ,desired_capabilities=capabilities)
                # Logger('browser').INFO('Get new browser')
                return browser
            else:
                browser = webdriver.Firefox(executable_path=GECKODRIVER, firefox_binary=FIREFOX_BINARY,
                                            firefox_profile=PROFILE,
                                            options=options,)
                # Logger('browser').INFO('Get new browser')
                return browser
        except Exception as e:
            print("Error in getting browser: ", e)
            # Logger('browser').ERROR("Error in getting Browser: " + str(e))