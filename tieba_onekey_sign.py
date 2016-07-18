#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 百度贴吧一键签到
from selenium import webdriver
import time

username = u"你的用户名"
passwd = "your password"
exe_path = "/Users/kalen/Programfiles/phantomjs-2.1.1-macosx/bin/phantomjs"

print "正在模拟登陆百度贴吧...."
# 模拟登陆
driver = webdriver.PhantomJS(executable_path=exe_path)
driver.get('http://tieba.baidu.com/')
login_a_tag = driver.find_element_by_xpath('//*[@class="u_login"]/div/a')
login_a_tag.click()
time.sleep(1)
username_input = driver.find_element_by_id("TANGRAM__PSP_8__userName")
username_input.send_keys(username)
passwd_input = driver.find_element_by_id("TANGRAM__PSP_8__password")
passwd_input.send_keys(passwd)

login_btn = driver.find_element_by_id("TANGRAM__PSP_8__submit")
login_btn.click()
time.sleep(1)

# 一键签到
driver.get("http://tieba.baidu.com/")
onekey_sign = driver.find_element_by_xpath('//*[@id="onekey_sign"]/a')
print "登陆成功"

onekey_sign.click()
time.sleep(1)

print "开始一键签到"
onekey_sign_btn = driver.find_element_by_xpath('//div[@class="sign_detail_hd"]/a')
onekey_sign_btn.click()
time.sleep(1)

print "一键签到成功"

driver.quit()

