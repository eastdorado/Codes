#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Project: PyCharm
# @File    : driverTest.py
# @Author  : tiger
# @Email   : shdorado@126.com
# @Time    : 2020/6/16 13:08
# 淘宝秒杀脚本，扫码登录版  账号密码登录版

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

# deckodreiver
chromedriver_path = r'C:\Program Files (x86)\Tencent\QQBrowser\QQBrowser.exe'
# chromedriver_path = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python36\chromedriver.exe"  #
# 谷歌chromedriver完整路径
options = webdriver.ChromeOptions()  # 配置 chrome 启动属性
options.add_experimental_option("excludeSwitches", ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(driver, 10)  # 超时时长为10s


# 登录
def login():
    driver.get("https://cart.taobao.com/cart.htm")
    time.sleep(20)
    sel = wait.until(EC.presence_of_element_located((By.ID, 'J_SelectAll2')))
    sel.click()


# 下单
def buy(buytime):
    i = 0
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if now > buytime:
            # driver.refresh()  # 刷新页面
            try:
                jss = wait.until(EC.presence_of_element_located((By.ID, 'J_Go')))
                jss.click()
                try:
                    tjdd = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                    tjdd.click()
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"抢购成功，请尽快付款" + now)
                    break
                except:
                    i = i + 1
                    try:
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"再次尝试提交订单" + now)
                        driver.refresh()  # 刷新页面
                        tjdd = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                        tjdd.click()
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"抢购成功，请尽快付款" + now)
                    except:
                        try:
                            i = i + 1
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"再次尝试提交订单" + now)
                            driver.refresh()  # 刷新页面
                            tjdd = wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                            tjdd.click()
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"抢购成功，请尽快付款" + now)
                        except:
                            i = i + 1
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"再次尝试提交订单" + now)
                            driver.refresh()  # 刷新页面
                            tjdd = wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                            tjdd.click()
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"抢购成功，请尽快付款" + now)
            except:
                driver.get("https://cart.taobao.com/cart.htm")
                sel = wait.until(EC.presence_of_element_located((By.ID, 'J_SelectAll2')))
                sel.click()
                jss = wait.until(EC.presence_of_element_located((By.ID, 'J_Go')))
                jss.click()
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"再次尝试提交订单" + now)
                i = i + 1
                try:
                    tjdd = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                    tjdd.click()
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"抢购成功，请尽快付款" + now)
                    break
                except:
                    i = i + 1
                    try:
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"再次尝试提交订单" + now)
                        driver.refresh()  # 刷新页面
                        tjdd = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                        tjdd.click()
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"抢购成功，请尽快付款" + now)
                        break
                    except:
                        driver.get("https://cart.taobao.com/cart.htm")
                        sel = wait.until(EC.presence_of_element_located((By.ID, 'J_SelectAll2')))
                        sel.click()
                        jss = wait.until(EC.presence_of_element_located((By.ID, 'J_Go')))
                        jss.click()
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"再次尝试提交订单" + now)
                        i = i + 1
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"再次尝试提交订单" + now)
                        driver.refresh()  # 刷新页面
                        tjdd = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a[@class="go-btn"]')))
                        tjdd.click()
                        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"抢购成功，请尽快付款" + now)
                        break

        if i > 10:
            print(f">>>已经尝试第{i}次抢购，抢购失败，程序终止！")
            break


if __name__ == "__main__":
    login()
    buy('2020-03-02 19:59:58')

# if __name__ == "__main__":
#     # 中文账号记得decode编码
#     login("九曲烟雨", 'cyh88kh69')
#     buy('2019-11-10 01:01:01.000001')
