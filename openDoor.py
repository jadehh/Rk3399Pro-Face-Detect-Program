import sys
import time
class OpenDoor():
    def __init__(self):
        # 注册5号io
        with open("/sys/class/gpio/export", "w") as f:
            print("注册5号IO")
            f.write(str(5))
            f.close()

        # 注册5号io为输出
        with open("/sys/class/gpio/gpio5/direction", "w") as f:
            print("注册5号IO为输出")
            f.write("out")
            f.close()

        self.close()

    def open(self):
        # 注册5号io为输出高电平
        with open("/sys/class/gpio/gpio5/value", "w") as f:
            print("注册5号IO输出为高电平")
            f.write(str(1))
            time.sleep(1)
            f.close()
        self.close()

    def close(self):
        with open("/sys/class/gpio/gpio5/value", "w") as f:
            print("注册5号IO输出为低电平")
            f.write(str(0))
            f.close()

    def destory(self):
        # 销毁5号io
        with open("/sys/class/gpio/unexport", "w") as f:
            print("销毁5号")
            f.write(str(5))
            f.close()


if __name__ == '__main__':
    openDoor = OpenDoor()
    openDoor.open()

