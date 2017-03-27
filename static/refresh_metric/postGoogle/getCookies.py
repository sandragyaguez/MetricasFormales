# -*- coding: utf-8 -*-

from selenium import webdriver
import time, pickle

driver = webdriver.Chrome('./chromedriver')
print "Chrome browser will be opened."
driver.get("http://www.plus.google.com")
mode=raw_input('Press enter when you have registered.')

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
driver.quit()