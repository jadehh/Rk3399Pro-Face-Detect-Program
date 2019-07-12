# Rk3399Pro-Face-Recognize-Program
## Rk3399Pro 基于pyqt的人脸识别程序 
### Rk3399Pro linux 配置

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
python /home/toybrick/Desktop/runing.py
```
3. 修改系统的时区 
```
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```
> 查看当前时间

```
date -R
```


