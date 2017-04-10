#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" 百度贴吧签到脚本 """
from __future__ import print_function
from selenium import webdriver
from bs4 import BeautifulSoup
from config import *
import traceback
from sign import parse_tiebas, sleep_for_a_while, take_screenshot
import cPickle as pickle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def get_login_user(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    elem = soup.find("p", {"class": "user_info_name"})
    return elem.get_text()


if __name__ == '__main__':
    driver = webdriver.PhantomJS(executable_path=exe_path, desired_capabilities=dcap)
    driver.delete_all_cookies()
    with open("cookies.pickle") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except: pass

    try:
        # 获取当前用户
        driver.get("https://tieba.baidu.com/?page=user")
        username = get_login_user(driver.page_source)
        print("当前用户为: ", username)

        # 开始进行签到
        print("开始签到")
        driver.get("http://tieba.baidu.com/?page=like")
        expand_more = driver.find_element_by_xpath("//div[@class='expand-all']/p")
        expand_more.click()
        sleep_for_a_while()

        # 获取常逛的贴吧
        tiebas = parse_tiebas(driver.page_source)

        # 逐个签到
        for tieba in tiebas:
            print(u"正在签到-->\"" + tieba['title'] + u"\"吧", end='')
            driver.get(tieba['href'])
            bs_obj = BeautifulSoup(driver.page_source, "html.parser")
            sign_btn_tag = bs_obj.find("a", {'class': 'sign-button'})
            if sign_btn_tag.text == u"已签到":
                print("(已经完成签到,不需要重新签到)")
                continue
            # 点击签到
            sign_btn = driver.find_element_by_class_name('sign-button')
            sign_btn.click()
            sleep_for_a_while()

            # 关闭贴吧客户端窗口
            close_client_btn = driver.find_element_by_class_name('daoliu_sign_in_prompt_close')
            close_client_btn.click()
            sleep_for_a_while()
            print("(签到成功)")

        print('全部签到完成!!!')
    except Exception, ex:
        traceback.print_exc()
    finally:
        print('正在退出')
        driver.quit()



