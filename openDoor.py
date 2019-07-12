import os

class OpenDoor():
    def __init__(self):
        # 注册5号io
        self.destory()
        print("申请控制5号IO")
        os.system("sudo sh - c 'echo 5 > /sys/class/gpio/export'")
        os.system("sudo sh - c  'echo out > /sys/class/gpio/gpio5/direction'")

    def open(self):
        # 注册5号io为输出高电平
        print("设置5号IO输出高电平")
        os.system("sudo sh - c  'echo 1 > /sys/class/gpio/gpio5/value'")

    def close(self):
        print("注册5号IO输出为低电平")
        os.system("sudo sh - c  'echo 0 > /sys/class/gpio/gpio5/value'")

    def destory(self):
        # 销毁5号io
        print("销毁5号IO")
        os.system("sudo sh - c  'echo 5 > /sys/class/gpio/unexport'")


if __name__ == '__main__':
    openDoor = OpenDoor()
    openDoor.open()
    

