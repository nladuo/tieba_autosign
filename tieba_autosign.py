#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 百度贴吧一键签到
from __future__ import print_function
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from config import *

if __name__ == '__main__':
    print("正在模拟登陆百度贴吧....")
    # 模拟登陆
    driver = webdriver.PhantomJS(executable_path=exe_path, desired_capabilities=dcap)
    driver.get('http://tieba.baidu.com/?page=user')

    # 隐藏跳转app界面
    app_continue_span = driver.find_element_by_id('index-app-continue')
    app_continue_span.click()
    time.sleep(1)

    # 显示登陆窗口
    login_tag = driver.find_element_by_class_name('j_footer_toast')
    login_tag.click()
    time.sleep(1)

    # 开始模拟登陆
    username_input = driver.find_element_by_id("TANGRAM__PSP_6__username")
    username_input.send_keys(username)
    passwd_input = driver.find_element_by_id("TANGRAM__PSP_6__password")
    passwd_input.send_keys(passwd)

    login_btn = driver.find_element_by_id("TANGRAM__PSP_6__submit")
    login_btn.click()
    time.sleep(1)

    print ('登陆成功, 开始签到!')

    # 开始进行签到
    driver.get("http://tieba.baidu.com/?page=like")
    expand_more = driver.find_element_by_xpath("//div[@class='expand-all']/p")
    expand_more.click()
    time.sleep(1)

    # 获取常逛的贴吧
    tiebas = []
    bs_obj = BeautifulSoup(driver.page_source, "html.parser")
    for a in bs_obj.find_all('a', {'class': 'j_forumTile_wrapper'}):
        title = a.get("data-start-app-param")
        href = a.get("href")
        tiebas.append({
            'title': title,
            'href': 'http://tieba.baidu.com' + href
        })

    # 逐个签到
    for tieba in tiebas:
        print(u"正在签到-->\"" + tieba['title'] + u"\"吧", end = '')
        driver.get(tieba['href'])
        bs_obj = BeautifulSoup(driver.page_source, "html.parser")
        sign_btn_tag = bs_obj.find("a", {'class': 'sign-button'})
        if sign_btn_tag.text == u"已签到":
            print("(已经完成签到,不需要重新签到)")
            continue
        # 点击签到
        sign_btn = driver.find_element_by_class_name('sign-button')
        sign_btn.click()
        time.sleep(1)

        # 关闭贴吧客户端窗口
        close_client_btn = driver.find_element_by_class_name('daoliu_sign_in_prompt_close')
        close_client_btn.click()
        time.sleep(1)
        print("(签到成功)")

    print('全部签到完成!!!')
    driver.quit()

