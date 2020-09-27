from dictscraper.browser import Browser
import time
from selenium import webdriver
from bs4 import BeautifulSoup

class dictionaryScraper:
    def __init__(self):
        print("Initiated")
        # self.driver = Browser(0).getBrowser()
        self.browser = webdriver.Firefox()

    def __del__(self):
        self.browser.close()

    def get_url(self, tab):
        try:
            self.browser.get('https://accessibledictionary.gov.bd/bengali-to-bengali/?alp='+ tab)
            # time.sleep(10)
        except Exception as e:
            print("get url error: ", e)

    def get_source_page(self):
        try:
            page_source = self.browser.page_source
            return page_source
        except Exception as e:
            print('Parsing error: ', e)

    def parse_data(self, page_source):
        try:
            soup = BeautifulSoup(page_source, "html.parser")
            # print(soup)
            artical = soup.find('article',  {'class': 'dicDisplay'})
            # print(artical)
            li_list = artical.find_all('li')
            # print(li_list)
            for li in li_list:
                print(li)
                main_word = li.find('span', {'class': 'separator'}).text
                ems = li.find_all('em')
                print(main_word)
                print(ems)
                print(li.text)
            return
        except Exception as e:
            print('Parsing error: ', e)

if __name__ == '__main__':
    scraper = dictionaryScraper()
    scraper.get_url('অ')
    source = scraper.get_source_page()
    scraper.parse_data(source)
    del scraper