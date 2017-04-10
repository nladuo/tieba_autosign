# tieba_autosign
百度贴吧自动签到脚本
## 效果
![效果](./effect.png)

## 安装
1、下载源码
``` sh
git clone https://github.com/nladuo/tieba_autosign.git
cd tieba_autosign && mv config.sample.py config.py
```
2、安装[phantomjs](http://phantomjs.org/)<br>
3、安装依赖库
``` sh
pip install -r requirements.txt
```
3、修改配置(config.py)
``` python
username = u"你的用户名"
passwd = "your password"
exe_path = "/usr/local/bin/phantomjs"
```
## 运行
### 本地模式
``` sh
python sign.py   # 对常逛的贴吧直接逐个签到
```
### 部署模式
目前只支持本地, 完善中.....
``` sh
python get_cookies.py           # 先获取cookies
python sign_with_cookies.py     # 然后通过cookies登陆
```

## TODO
- [ ] 解决登陆时手机验证
## LICENSE
MIT
