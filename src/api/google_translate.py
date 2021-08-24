from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


def get_google_translation(french_sentence):
    # This example requires Selenium WebDriver 3.13 or newer
    with webdriver.Chrome() as driver:
        try:
            # driver = webdriver.Chrome()
            url = rf"https://translate.google.com/?sl=de&tl=en&text={french_sentence}&op=translate"
            driver.implicitly_wait(10)  # seconds
            driver.get(url)
            output_selector = "body > c-wiz.zQTmif.SSPGKf.RvYhPd.BIdYQ.aL9XFd:nth-child(5) > div.T4LgNb:nth-child(1) > div.WFnNle:nth-child(2) > c-wiz.MOkH4e.BSw7K.iYelWb.LUoOL > div.OlSOob:nth-child(2) > c-wiz.QsA0jb > div.ccvoYb:nth-child(2) > div.AxqVh:nth-child(2) > div.OPPzxe:nth-child(2) > c-wiz.P6w8m.BDJ8fb:nth-child(2) > div.dePhmb:nth-child(6) > div.eyKpYb > div.J0lOec:nth-child(1) > span.VIiyi:nth-child(1) > span.JLqJ4b.ChMk0b > span:nth-child(1)"
            # input_selector = "((((//c-wiz/div)[2]/c-wiz//div)[2]/c-wiz/div)[1]/div)[2]/"
            # input_selector
            result = driver.find_element_by_css_selector(output_selector)
            # time.sleep(5)
            return result.text
        except:
            return "Google translation is unavialable at the moment. Please try later"
