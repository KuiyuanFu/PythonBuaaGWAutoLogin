# 自动登录BUAA网关

## 主要思想

使用场景为校内服务器的自动登录网关。

以指定的时间间隔监控是否登录网关，若没有登录则进行登录操作。



- 使用Headless Chrome 和 selenium 操作网页
- 一个守护程序自动启动



## 环境搭建



[下载chrome 的安装文件](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)

[下载chrome driver 的安装文件](http://chromedriver.storage.googleapis.com/index.html)

[下载python包的离线安装文件](https://www.lfd.uci.edu/~gohlke/pythonlibs/)



````shell
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt --fix-broken install ./google-chrome-stable_current_amd64.deb

unzip chromedriver_linux64.zip

pip3 install selenium-3.141.0-py3-none-any.whl

````



将解压出来的 chromedriver 文件放置在 python 文件的同目录下。



## 主要逻辑



[selenium 教程](http://www.selenium.org.cn/1598.html)



- 通过访问GW页面，根据是否有用户名的标签来判断是否已经登录。
- 通过输入用户名，密码达到登录的目的。


## 使用

```sh
usage: buaagw [-h] {login,logout,status} ...

BUAA gateway.

positional arguments:
  {login,logout,status}
                        functions
    login               login
    logout              logout
    status              status

optional arguments:
  -h, --help            show this help message and exit

```

```sh
usage: buaagw login [-h] [-r interval] username password

positional arguments:
  username     buaa gw username.
  password     buaa gw password.

optional arguments:
  -h, --help   show this help message and exit
  -r interval  The interval of testing the network connection. Default is 0,
               not test and retry.
```

## 注册为服务


```sh
sudo vim /etc/systemd/system/buaagw.service

# context start
[Unit]
Description=buaagw
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/etc/bin/buaagw login

[Install]
WantedBy=multi-user.target
# context end

sudo systemctl daemon-reload
sudo systemctl enable buaagw.service 
sudo systemctl restart buaagw.service
sudo systemctl status buaagw.service

```