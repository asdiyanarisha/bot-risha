import argparse
from pyhocon import ConfigFactory
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
from lib.util import log
import time
import pickle
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            f'Chrome/44.0.2403.157 Safari/537.36')
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = None

logger = log.get_logger("bot_ig_like")


def driver_init():
    global driver
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = "180.250.12.10:80"
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # prox.add_to_capabilities(capabilities)
    #
    # driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(900, 740)
    driver.set_page_load_timeout(300)


def login():
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys("akuncoba295")
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys("Risha090595")
    driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button").click()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()

    pickle.dump(driver.get_cookies(), open("cookies/pickle.pkl", "wb"))


def send_otp(otp):
    i = 1
    for num in otp.strip():
        if i == 1:
            driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/div[3]/input").send_keys(num)
        else:
            driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/div[3]/input[{}]".format(i)).send_keys(num)
        i += 1


def process_like_comment(data, message, comment=True):
    url = "https://www.instagram.com" + data['href']
    logger.info("Open Post Url " + url)
    driver.get(url)
    time.sleep(1)
    status_like = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[1]"
                                               "/span[1]/button")
    like = BeautifulSoup(status_like.get_attribute("innerHTML"), 'html.parser')
    is_like = like.select_one("div > span > svg")['aria-label']
    if is_like == "Like":
        status_like.click()
        logger.info("Done Liked Post Url " + url)
        if comment:
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[1]/span[2]/"
                                         "button").click()
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[3]/div/form/"
                                         "textarea").send_keys(message)
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div[3]/section[3]/div/form/"
                                         "button").click()
            logger.info("Done Comment Post Url " + url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitter Crawler")
    parser.add_argument("-u", "--users", type=str, help="increase output verbosity")
    parser.add_argument("-m", "--message", type=str, help="increase output verbosity")

    args = parser.parse_args()

    conf = ConfigFactory.parse_file("config.conf")

    driver_init()

    driver.get("https://www.instagram.com/")

    # dikomen mungkin nanti dibutuhkan
    if os.path.exists("cookies/pickle.pkl"):
        cookies = pickle.load(open("cookies/pickle.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        logger.info("Using cookies")
    else:
        login()

    for account in args.users.split(","):
        logger.info("Open Instagram Account " + account)
        driver.get("https://www.instagram.com/{}/".format(account))
        source = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[3]/article/div[1]/div/div[1]")
        content = BeautifulSoup(source.get_attribute("innerHTML"), 'html.parser')
        links = content.select('div > a')
        for link in links:
            process_like_comment(link, str(args.message))

    driver.quit()
