# Rk3399Pro-Face-Recognize-Program
## Rk3399Pro 基于pyqt的人脸检测程序 
1. 环境配置 
> 注意大小写
```
sudo dnf install python3-PyQt5
sudo dnf install python3-opencv
```

## RK3399Pro 启动人脸检测
```
python3 running.py
```
## Rk3399Pro linux 配置
1. 需要开机自动登录
```
vim /etc/lxdm/lxdm.conf
```
>写入toybrick 为用户名称 
```
Autologin = toybrick
```
2. 程序的自动启动 
>自启动的Qt程序需要在加载桌面之后才能完全启动，不然锁频的方法就会失效 

>桌面自启动的方法设置
```
vim ~/.config/lxsession/LXDE/autostart
```
> 在autostart中加入需要自启动的命令
```
python3 /home/toybrick/Desktop/running.py
```
3. 修改系统的时区 
```
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
> 查看当前时间

```
date -R
```
4. 关闭锁屏 
```
在首选项中，打开屏幕保护程序，Mode 选择 Disable Screen Saver
```


