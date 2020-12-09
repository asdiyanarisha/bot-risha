from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pickle
import argparse
from lib.util import log

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            f'Chrome/44.0.2403.157 Safari/537.36')
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = None

logger = log.get_logger("bot_tinder")


def driver_init():
    global driver
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = "180.250.12.10:80"
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1024, 1024)
    driver.set_page_load_timeout(300)


def login(no_hp):
    time.sleep(2)
    driver.find_element_by_css_selector("button.button").click()
    time.sleep(3)
    driver.find_element_by_css_selector("button[aria-label='Masuk dengan nomor telepon']").click()
    time.sleep(3)
    driver.find_element_by_xpath("//input[@name='phone_number']").send_keys(no_hp)
    time.sleep(2)
    # driver.find_element_by_xpath("//button[@type='button']").click()
    driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/button").click()
    conf = input("Mendapat Kode OTP ? [Y/N]")
    if conf.strip() == "Y":
        otp = input("Masukan Kode OTP ")
        send_otp(otp)
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/button").click()
    else:
        send_otp("823382")
        time.sleep(3)
        logger.info("Send Random OTP")
        driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/button").click()
        time.sleep(2)
        resend_otp = input("Kirim Ulang ? [Y/N]")
        if resend_otp.strip() == "Y":
            logger.info("Send Kirim Ulang")
            driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[1]/div[2]/button").click()
        otp = input("Masukan Kode OTP ")
        send_otp(otp)
        time.sleep(3)
        driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/button").click()
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div/div/div[3]/button[1]").click()
    logger.info("Click Pop Up 1")
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div/div/div[3]/button[1]").click()
    logger.info("Click Pop Up 2")

    # pickle.dump(driver.get_cookies(), open("cookies/pickle_tinder.pkl", "wb"))


def check_modal():
    try:
        logger.info("Check Modal")
        check_modal_swipe = driver.find_element_by_xpath("//*[@id='modal-manager']/div/div")
        if check_modal_swipe:
            logger.info(check_modal_swipe.text)
            if "Get notifications" in str(check_modal_swipe.text):
                driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
            if "Send a Super Like" in str(check_modal_swipe.text):
                driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/button[2]").click()
                time.sleep(1)
            if "Home Screen" in str(check_modal_swipe.text):
                driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div[2]/button[2]").click()
                time.sleep(1)
    except Exception as e:
        logger.error("Check Modal")
        time.sleep(1)


def swipe_right(count):
    match = 0
    logger.info("Please Wait For 10 Sec")
    time.sleep(10)
    i = 0
    while True:
        time.sleep(1)
        try:
            logger.info("Start Swipe Right")
            driver.find_element_by_xpath("//*[@id='content']/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button").click()
        except Exception as e:
            logger.error(e)
            time.sleep(1)
        try:
            time.sleep(1)
            logger.info("Check Match")
            check_match_swipe = driver.find_element_by_xpath("//*[@id='modal-manager-canvas']/div/div")
            if check_match_swipe:
                match += 1
                logger.info(check_match_swipe.text)
                driver.find_element_by_xpath("//*[@id='modal-manager-canvas']/div/div/div[1]/div/div[4]/button").click()
        except Exception as e:
            logger.error(e)
            time.sleep(1)
        check_modal()
        i += 1
        if i == int(count):
            break
    logger.info("Finish Swipe Right")
    logger.info("Jumlah Termatch : {}".format(match))


def send_otp(otp):
    i = 1
    for num in otp.strip():
        if i == 1:
            driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/div[3]/input").send_keys(num)
        else:
            driver.find_element_by_xpath("//div[@id='modal-manager']/div/div/div/div[3]/input[{}]".format(i)).send_keys(num)
        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitter Crawler")
    parser.add_argument("-p", "--phone", type=str, help="increase output verbosity")
    parser.add_argument("-c", "--count", type=str, help="increase output verbosity")

    args = parser.parse_args()

    # conf = ConfigFactory.parse_file("config.conf")

    driver_init()
    driver.get("https://tinder.com/?lang=id")
    time.sleep(2)
    logger.info("Accept Cookies Info")
    driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div/div/div[1]/button").click()
    time.sleep(1)

    # dikomen mungkin nanti dibutuhkan
    if os.path.exists("cookies/pickle_tinder.pkl"):
        cookies = pickle.load(open("cookies/pickle_tinder.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        logger.info("Using cookies")
    else:
        login(args.phone)

    driver.get("https://tinder.com/app/recs")
    check_modal()
    swipe_right(args.count)

