# 自动登录BUAA GW





## 主要思想



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



### 主要逻辑



[selenium 教程](http://www.selenium.org.cn/1598.html)



- 通过访问GW页面，根据是否有用户名的标签来判断是否已经登录。
- 通过输入用户名，密码达到登录的目的。

## 守护进程



````
sudo apt-get install supervisor

cd /etc/supervisor/conf.d/
sudo vim /etc/supervisor/conf.d/AutoLogin.conf 


[program:AutoLogin]
command=bash ./run.sh
user=fukuiyuan
directory=/usr/local/AutoLogin
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
redirect_stderr=true
stdout_logfile_maxbytes=200MB
stdout_logfile_backups=10
stdout_logfile=/usr/local/AutoLogin/AutoLogin-supervisor.log 


sudo supervisorctl reload
sudo supervisorctl start AutoLogin

sudo supervisorctl tail AutoLogin stderr
````





