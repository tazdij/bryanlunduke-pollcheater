import math
import sys, os, getopt
import csv
import platform
import random
import time
from pprint import pprint
import base64
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


random.seed()

def GenerateProxyAuthToken(username, password):
    token = username + ':' + password
    return base64.b64encode(token.encode('utf-8')).decode('utf-8')

def ElemSendKeysRand(elem, msg):
    #pprint.pprint(elem)
    for letter in msg:
        #print('top of loop')
        time.sleep(random.uniform(0.1, 0.3))
        elem.send_keys(letter)




def setup_driver_path(system_name):
    path = os.path.dirname(os.path.abspath(__file__))
    if system_name == 'Darwin':
        os.environ["PATH"] += ":" + os.path.join(path, 'drivers', 'darwin')
    elif system_name == 'Windows':
        #TODO: Add 32 & 64 bit distinction
        os.environ["PATH"] += ";" + os.path.join(path, 'drivers', 'windows')

def create_driver(user, password, ip, port):
    path = os.path.dirname(os.path.abspath(__file__))

    setup_driver_path(platform.system())

    proxyAddrIP = ip
    proxyAddrPort = port
    proxyAddr = proxyAddrIP + ':' + proxyAddrPort
    auth_token = GenerateProxyAuthToken(user, password)

    proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxyAddr,
            'ftpProxy': proxyAddr,
            'sslProxy': proxyAddr,
            'noProxy': '',
        })

    # webdriver.DesiredCapabilities.FIREFOX['proxy']={
    #     "httpProxy": proxyAddr,
    #     "ftpProxy": proxyAddr,
    #     "sslProxy": proxyAddr,
    #     "noProxy": None,
    #     "proxyType": "MANUAL",
    #     "autodetect": False
    # }

    fp = webdriver.FirefoxProfile()

    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.http", proxyAddrIP)
    fp.set_preference("network.proxy.http_port", int(proxyAddrPort))

    #fp.add_extension(os.path.join(path, "extensions", "firefox", "proxyauth.xpi"))
    fp.add_extension(os.path.join(os.path.dirname(__file__), "extensions", "firefox", "proxyauth.xpi"))
    #fp.add_extension(os.path.join(os.path.dirname(__file__), "extensions", "firefox", "firebug.xpi"))
    #fp.add_extension(os.path.join(os.path.dirname(__file__), "extensions", "firefox", "firexpath.xpi"))
    fp.set_preference("extensions.proxyauth.authtoken", auth_token)

    driver = webdriver.Firefox(fp, proxy=proxy)

    return driver

def close_driver(driver):
    driver.close()
    driver = None

if __name__ == "__main__":

    # Read in proxy list
    #proxies = csv.DictReader(open("./proxies.csv", "r", encoding='utf-8'))

    driver = create_driver()

    while True:
        # Go to page
        driver.get('http://www.polljunkie.com/poll/fjospo/you-put-linux-on-that')

        # Get the needed elements from the page
        el_person = driver.find_element_by_id('opt410206')
        el_subscribe = driver.find_element_by_id('opt410208')
        el_submit = driver.fin_element_by_id('submitit')

        el_person.click()
        el_subscribe.click()
        el_submit.click()

        # Sleep for a random time
        time.sleep(random.uniform(5.0, 8.0))


    close_driver(driver)
