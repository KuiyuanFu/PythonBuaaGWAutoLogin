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





## 守护进程



````
sudo apt-get install supervisor

sudo vim /etc/supervisor/conf.d/AutoLogin.conf 

[program:AutoLogin]
command=bash ./run.sh
user=USERNAME
directory=DIRECTORY
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
redirect_stderr=true
stdout_logfile_maxbytes=200MB
stdout_logfile_backups=10
stdout_logfile=DIRECTORY/AutoLogin-supervisor.log 


sudo supervisorctl reload
sudo supervisorctl start AutoLogin

sudo supervisorctl tail AutoLogin stderr

````



## 使用



`AutoLogin.conf.template` 为守护进程的配置文件，需要修改第三行 `user=USERNAME` 及 第四行 `directory=DIRECTORY` 第12行 `stdout_logfile=DIRECTORY/AutoLogin-supervisor.log ` 中的大写变量。



`run.sh.template` 为启动程序的shell文件。

`python3 AutoLogin.py USERNAME PASSWORD CHECKINTERVAL` 参数为 用户名 密码 及检测间隔。



需要把后缀去掉。

