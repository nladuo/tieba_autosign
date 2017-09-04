#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" 百度贴吧签到脚本 """
from __future__ import print_function
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from config import *
import traceback


# 判断是否存在验证码
def have_verifycode(page_source):
    bs_obj = BeautifulSoup(page_source, "html.parser")
    return not (bs_obj.find('input', {'id': 'TANGRAM__PSP_6__verifycode'}) is None)


# 解析贴吧
def parse_tiebas(page_source):
    tiebas = []
    bs_obj = BeautifulSoup(page_source, "html.parser")
    for a in bs_obj.find_all('a', {'class': 'j_forumTile_wrapper'}):
        title = a.get("data-start-app-param")
        href = a.get("href")
        tiebas.append({
            'title': title,
            'href': 'http:' + href
        })
    return tiebas


# 等待一会儿
def sleep_for_a_while():
    time.sleep(1)


# 截图,用于调试
def take_screenshot(driver, id):
    driver.get_screenshot_as_file("debug" + id + ".png")


if __name__ == '__main__':
    print("正在模拟登陆百度贴吧....")
    # 模拟登陆
    driver = webdriver.PhantomJS(executable_path=exe_path, desired_capabilities=dcap)
    try:
        driver.get('http://tieba.baidu.com/?page=user')

        # 隐藏跳转app界面
        try:
            app_continue_span = driver.find_element_by_id('index-app-continue')
            app_continue_span.click()
            sleep_for_a_while()
        except: pass

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

        print('登陆成功, 开始签到!')
        # 开始进行签到
        driver.get("http://tieba.baidu.com/?page=like")
        try:
            expand_more = driver.find_element_by_xpath("//div[@class='expand-all']/p")
            expand_more.click()
        except: pass
        sleep_for_a_while()

        # 获取常逛的贴吧
        tiebas = parse_tiebas(driver.page_source)

        # 逐个签到
        for tieba in tiebas:
            print(u"正在签到-->\"" + tieba['title'] + u"\"吧", end='')
            driver.get(tieba['href'])
            bs_obj = BeautifulSoup(driver.page_source, "html.parser")
            sign_btn_tag = bs_obj.find("a", {'class': 'sign-button'})
            if sign_btn_tag is None:
                print("(未找到签到标签)")
                continue
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
    except Exception as ex:
        traceback.print_exc()
    finally:
        print('正在退出')
        driver.quit()



