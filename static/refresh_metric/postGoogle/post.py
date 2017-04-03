# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import pickle
import sys
import os

def publish(text="Who needs a public API when you can 'hack' google plus to publish using selenium?"):
  current_dir = os.path.dirname(os.path.abspath(__file__))
  driver = webdriver.Chrome(current_dir+'/chromedriver')
  driver.get('https://plus.google.com/')
  cookies = pickle.load(open(current_dir+"/cookies.pkl", "rb"))

  if not cookies:
    print "Es necesario un fichero con las cookies de session"
    print "Visita: http://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver"
    exit(-1)

  for cookie in cookies:
      new_cookie = {}
      new_cookie['name'] = cookie['name']
      new_cookie['value'] = cookie['value']
      driver.add_cookie(new_cookie)

  driver.get('https://plus.google.com/')
  time.sleep(1)

  xpath = ".//*[contains(text(),'¿Tienes algo nuevo que contar?')]"
  textbox = driver.find_element_by_xpath(xpath)

  textbox.click()
  time.sleep(0.8)

  textInput = driver.find_element_by_id('XPxXbf')
  textInput.send_keys(text)

  sendButtonText = "//div[contains(@class, 'O0WRkf') and contains(@class, 'zZhnYe')]"

  #sendButtonText=".//*[contains(text(),'Compartir') and contains(concat(' ', @class, ' '), 'd-k-l')]"

  sendButton = driver.find_element_by_xpath(sendButtonText)

  sendButton.click()
  currentTime = time.time()
  time.sleep(2)
  driver.quit()

  return currentTime

if __name__ == "__main__":
  text = "Who needs a public API when you can 'hack' google plus to publish using selenium?"
  if (len(sys.argv) > 1):
    text = sys.argv[1]

  publish(text)
