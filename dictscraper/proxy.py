from pprint import pprint
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class ProxyInfo(object):

    def __init__(self):
        self.ua= UserAgent # From here we generate a random user agent
        self.proxies = []  # Will contain proxies [ip, port]


    # Retrieve a random index proxy (we need the index to delete it if not working)
    def random_proxy(self):
      return random.randint(0, len(self.proxies) - 1)

    def getRandomUserAgent(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent
    # Main function
    def getProxy(self):
        user_agent = self.getRandomUserAgent()
        # Our code here
        # Retrieve latest proxies
        proxies_req = Request('https://www.proxynova.com/proxy-server-list/country-bd/')
        proxies_req.add_header('User-Agent', user_agent)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')

        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='tbl_proxy_list')
        # pprint(proxies_table)
        proxies_arr=[]
        # Save proxies in the array
        max_speed = -9999
        proxy_site = ''
        for row in proxies_table.tbody.find_all('tr'):
            # ip =row.find_all('td')[0].text
            # print(row.find_all('td')[0].text.strip()[16:-3], row.find_all('td')[1].text.strip(), row.find_all('td')[3].text.strip()[:-3])
            try:
                speed = row.find_all('td')[3].text.strip()
                speed = int(speed[:-3])
                if (speed > max_speed):
                    max_speed = speed
                    proxies_arr.append({
                        'site': row.find_all('td')[0].text.strip()[16:-3] + ':' + row.find_all('td')[1].text.strip(),
                        'speed': int(row.find_all('td')[3].text.strip()[:-3])
                    })
                # speed = row.find_all('td')[3].text.strip()
                # speed = int(speed[:-3])
                # if(speed> max_speed):
                #     max_speed = speed
                #     proxy_site = row.find_all('td')[0].text.strip()[16:-3] + ':' + row.find_all('td')[1].text.strip()
            except:
                pass
            # proxies_arr.append({
            #     'ip': row.find_all('td')[0].text.strip()[16:-3],
            #     'port': row.find_all('td')[1].text.strip(),
            #     'speed': row.find_all('td')[3].text.strip()[:-3]
            # })
        print(proxies_arr)
        rand_idx = random.randint(0, len(proxies_arr))
        print(rand_idx)
        return proxies_arr[rand_idx]['site']
        # print('proxy sites')
        # print(proxies_arr)
        #
        # proxy_index = self.random_proxy()
        # proxy = self.proxies[proxy_index]
        #
        # for n in range(1, 100):
        #     req = Request('http://icanhazip.com')
        #     req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        #
        #     # Every 10 requests, generate a new proxy
        #     if n % 10 == 0:
        #         proxy_index = self.random_proxy()
        #         proxy = self.proxies[proxy_index]
        #
        #     # Make the call
        #     try:
        #         my_ip = urlopen(req).read().decode('utf8')
        #         print("Proxy is detected: "+proxy['ip']+":"+proxy['port'])
        #         return proxy['ip']+":"+proxy['port']
        #     except:  # If error, delete this proxy and find another one
        #         del self.proxies[proxy_index]
        #         print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
        #         proxy_index = self.random_proxy()
        #         proxy = self.proxies[proxy_index]

if __name__ == '__main__':
    print(ProxyInfo().getProxy())