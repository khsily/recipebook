from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

driver = webdriver.Chrome()
driver.get("https://www.google.com/imghp?hl=ko")
elem = driver.find_element_by_name("q")
name = '양파'
elem.send_keys(name)
elem.send_keys(Keys.RETURN)
iamges = driver.find_elements_by_css_selector(".wXeWr.islib.nfEiy")
count = 0
for i in iamges:
    i.click()
    # time.sleep(3)
    dd = driver.find_element_by_xpath("//div[contains(@jsname, 'CGzTgf')]/c-wiz/div/div/div/div[2]/div/a/img").get_attribute('src')
    print(dd)
    urllib.request.urlretrieve(dd, "data/{}_{}.jpg".format(name, count))
    count += 1
# assert "Python" in driver.title
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()