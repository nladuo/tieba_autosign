#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" 百度贴吧签到脚本 """
from __future__ import print_function
from selenium import webdriver
from config import *
import traceback
import cPickle as pickle
from sign import have_verifycode, sleep_for_a_while, take_screenshot


if __name__ == '__main__':
    print("正在模拟登陆百度贴吧....")
    # 模拟登陆
    driver = webdriver.PhantomJS(executable_path=exe_path, desired_capabilities=dcap)
    try:
        driver.get('http://tieba.baidu.com/?page=user')

        # 隐藏跳转app界面
        app_continue_span = driver.find_element_by_id('index-app-continue')
        app_continue_span.click()
        sleep_for_a_while()

        # 显示登陆窗口
        login_tag = driver.find_element_by_class_name('j_footer_toast')
        login_tag.click()
        sleep_for_a_while()

        # 开始模拟登陆
        username_input = driver.find_element_by_id("TANGRAM__PSP_6__username")
        username_input.send_keys(username)
        passwd_input = driver.find_element_by_id("TANGRAM__PSP_6__password")
        passwd_input.send_keys(passwd)

        login_btn = driver.find_element_by_id("TANGRAM__PSP_6__submit")
        login_btn.click()
        sleep_for_a_while()

        # 判断验证码
        if have_verifycode(driver.page_source):
            driver.get_screenshot_as_file('vcode.png')
            vcode_input = driver.find_element_by_id("TANGRAM__PSP_6__verifycode")
            vcode = raw_input("遇到验证码, 请查看vcode.png, 然后填写验证码: ")
            print('您输入的验证码为:"', vcode, '"')
            vcode_input.send_keys(vcode)
            login_btn.click()
            sleep_for_a_while()

        print('登陆成功!')
        print(driver.get_cookies())
        with open("cookies.pickle", "w") as f:
            pickle.dump(driver.get_cookies(), f)
        print('已保存cookies到./cookies.pickle')

    except Exception, ex:
        traceback.print_exc()
    finally:
        print('正在退出')
        driver.quit()



