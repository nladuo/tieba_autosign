# tieba_autosign
百度贴吧自动签到(一键签到)
## 说明
只能签到7级以上的贴吧，最多可签50个吧。
## 安装
1、下载源码
``` shell
git clone https://github.com/nladuo/tieba_autosign.git
```
2、下载phantomjs  
3、安装selenium webdriver
``` shell
pip install selenium
```
3、修改配置
``` python
username = u"你的用户名"
passwd = "your password"
exe_path = "/home/kalen/Programfiles/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
```
4、测试
``` shell
cd ./tieba_autosign
./tieba_autosign.py
```
## LICENSE
MIT
