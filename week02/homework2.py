from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    
    browser.get('https://shimo.im')
    time.sleep(1)
    
    browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button').click()
    time.sleep(1)

    browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('test@qq.com')
    browser.find_element_by_xpath('//input[@name="password"]').send_keys('123456')
    time.sleep(1)
    browser.find_element_by_xpath('//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()
    