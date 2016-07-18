#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 百度贴吧逐个签到
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time

username = u"你的用户名"
passwd = "your password"
exe_path = "/Users/kalen/Programfiles/phantomjs-2.1.1-macosx/bin/phantomjs"

# 模拟登陆
print "正在模拟登陆百度贴吧...."
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


# 签到
chains = ActionChains(driver)
driver.get("http://tieba.baidu.com/")
more_a_tag = driver.find_element_by_xpath('//div[@id="moreforum"]/a')
chains.move_to_element(more_a_tag).perform()

tiebas = []

bs_obj = BeautifulSoup(driver.page_source, "html.parser")
# 爱逛的贴吧
like_forum = bs_obj.find('div', {'id': 'likeforumwraper'})
for a in like_forum.find_all('a'):
    title = a.get("title")
    href = a.get("href")
    if title is None:
        title = a.get_text()
    tiebas.append((title, href))
# 常逛的贴吧
always_forum = bs_obj.find('div', {'class': 'tbui_panel_content j_panel_content clearfix'})
for a in always_forum.find_all('a'):
    title = a.get("title")
    href = a.get("href")
    if title is None:
        title = a.get_text()
    if href != '#':
        tiebas.append((title, href))

print "登陆完成!!"
print "开始签到....."

# 逐个签到
for tieba in tiebas:
    print "正在签到-->", tieba[0], "吧"
    driver.get("http://tieba.baidu.com" + tieba[1])
    bs_obj = BeautifulSoup(driver.page_source, "html.parser")
    a_tag = bs_obj.find("div", {'id': 'signstar_wrapper'}).a
    if a_tag.get("title") == u"签到完成":
        print "已经完成签到,不需要重新签到\n"
        continue
    sign_btn = driver.find_element_by_xpath('//div[@id="signstar_wrapper"]/a')
    sign_btn.click()
    time.sleep(2)
    print "签到成功" , "\n"

driver.quit()

