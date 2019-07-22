# ProgramCalculator
多功能可编程科学计算器，电子技术课程设计

# 树莓派环境配置
sudo raspi-config进入设置开启串口和SPI<br>
sudo rpi-update更新固件<br>
sudo modprobe fbtft_device name=adafruit28 gpios=reset:19，dc:26 speed=16000000连接到显示屏 （对应ILI9341驱动）<br>
https://github.com/notro/fbtft/blob/master/fbtft_device.c 查看具体驱动对应的型号<br>
FRAMEBUFFER=/dev/fb1 startx把界面投影到显示屏<br>
在/etc/rc.local中添加以上命令开机自启<br>
在/root/.config/lxsession/LXDE-pi/autostart中添加命令@lxterminal --working-directory=/home/pi/ --command='python3 ./main.py'在图形界面启动时自动启动主程序<br>
