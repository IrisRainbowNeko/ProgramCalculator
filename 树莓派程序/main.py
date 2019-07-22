print('正在初始化')
import numpy as np
import scipy as sci
import sympy
from sympy import symbols as sym
import os
import editor
import threading
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import serial
import wavesee
import time
import readline
import tanchi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

mouse = PyMouse()
keyboard = PyKeyboard()

ser = serial.Serial("/dev/ttyAMA0", 115200)  # 开启串口，波特率115200
ser.flushInput()
global ws
ws=None
wave_T=500*1000
global getwave
getwave=False


tones=[33,35,37,39,41,44,46,49,52,55,58,62,65,69,73,78,82,87,93,98,104,110,117,123,131,139,147,156,165,175,185,196,208,220,233,247,262,277,294,311,330,349,370,392,415,440,
              466,494,523,554,587,622,659,698,740,784,831,880,932,988,1047,1109,1175,1245,1319,1397,1480,1568,1661,1760,1865,1976,2093,2217,2349,2489,2637,2794,2960,3136,3322,3520,
              3729,3951,4186,4435,4699,4978]

#定义各种功能函数
def runpy(file):
    run(file+'.py')

def run(file):
    print(f'运行程序 {file}')
    os.system(f'python3 {file}')
    print(f'运行完毕')

def prog():
    editor.main()

def easymod():
    os.system("python3")
    os.system("clear")

def install(model):
    os.system(f"python3 -m pip install {model}")

def showimg(path):
    img=mpimg.imread(path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def updater():
    global getwave
    while getwave:
        ser.write('<wave>'.encode('utf-8'))
        time.sleep(wave_T/50/1000000)

def startWaver():
    global getwave
    global ws

    ws=wavesee.WaveShower()
    getwave=True
    t = threading.Thread(target=updater, args=tuple())
    t.start()
    ws.show()

def playGame():
    tanchi.main()

def runMusicFile(path):
    rate=1
    tone_key=[[0,2,4,5,7,9,11],
              [1,3,5,6,8,10,12]]
    with open(path, 'r') as f:
        for line in f:
            if line[0]=='#':
                continue
            tone = line.split(',') #音符,时间
            if tone[0]=='rate':
                rate=float(tone[1])
                continue
            if(tone[0]=='stop'):
                ser.write('<tone,-1>'.encode('utf-8'))
            else:
                ser.write(f'<tone,{tones[(int(tone[0])-1)*12+(tone_key[1][int(tone[1][:-1])-1] if tone[1].endswith("#") else tone_key[0][int(tone[1])-1])]}>'.encode('utf-8'))
            time.sleep(rate*int(tone[-1])/1000)
    ser.write('<tone,-1>'.encode('utf-8'))

def playMusic(path):
    t = threading.Thread(target=runMusicFile, args=(path,))
    t.start()

def setFreq(freq):
    ser.write(f'<freq,{freq}>'.encode('utf-8'))

def duty(duty):
    ser.write(f'<duty,{duty}>'.encode('utf-8'))

global isSwitch
isSwitch=False

keyevent_normal=[['q','w','e','r','t','y','u','i'],
                 ['o','p','a','s','d','f','g','h'],
                 ['j','k','l','z','x','c','v','b'],
                 [keyboard.shift_key,'[',']','n','m',';','\'',keyboard.tab_key],
                 [keyboard.control_key,keyboard.alt_key,',',' ',' ','(',')',keyboard.backspace_key],
                 [0,0,keyboard.right_key,keyboard.down_key,keyboard.enter_key,keyboard.up_key,keyboard.left_key,keyboard.escape_key]]

keyevent_shift=[['!','@','#',"$",'7','8','9','+'],
                ['%','^','&','|','4','5','6','-'],
                ['{','}',':','?','1','2','3','*'],
                [keyboard.shift_key,'\\','_','=','"','0','.','/'],
                [keyboard.control_key, keyboard.alt_key, ' ', ' ',' ', '<', '>', keyboard.backspace_key],
                [0, 0, keyboard.right_key, keyboard.down_key, keyboard.enter_key, keyboard.up_key, keyboard.left_key,keyboard.escape_key]]

def read_cmd():
    count = ser.inWaiting()
    data = ''
    flag = False
    while count > 0:
        by = ser.read(1).decode()
        count -= 1

        if by == '(':
            while True:
                by = ser.read(1).decode()
                if by == ')':
                    flag = True
                    break
                data += by
        if flag:
            return data
    return data

def KeyListener():
    print('键盘监听启动')
    global isSwitch
    global ws
    global getwave

    while True:
        try:
            data=read_cmd()

            if (data is None) or len(data)<=0:
                continue
            #产生对应的键盘事件
            cmds=data.split(',')

            if cmds[0]=='keydown':
                if cmds[1]=='5' and cmds[2]=='1' :
                    keyboard.type_string("easymod()")
                    keyboard.tap_key(keyboard.enter_key)
                elif cmds[1]=='5' and cmds[2]=='0' :
                    isSwitch=not isSwitch
                elif isSwitch:
                    keyboard.press_key(keyevent_shift[int(cmds[1])][int(cmds[2])])
                else:
                    keyboard.press_key(keyevent_normal[int(cmds[1])][int(cmds[2])])
            elif cmds[0]=='keyup':
                if cmds[1]=='5' and cmds[2]=='1' :
                    pass
                elif cmds[1]=='5' and cmds[2]=='0' :
                    pass
                elif isSwitch:
                    keyboard.release_key(keyevent_shift[int(cmds[1])][int(cmds[2])])
                else:
                    keyboard.release_key(keyevent_normal[int(cmds[1])][int(cmds[2])])
            elif cmds[0] == 'wave':
                if ws == None:
                    getwave=False
                else:
                    ws.update(int(cmds[1]))
        except Exception as e:
            getwave = False
            print(e)

t = threading.Thread(target=KeyListener, args=tuple())
t.start()
print('初始化完毕')

while True:
    cmd = input()
    try:
        code_exec = compile(cmd, '<string>', 'exec')
        exec(code_exec)
    except Exception as e:
        print(e)
