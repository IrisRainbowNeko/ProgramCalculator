import os

def typeok(n):
    return n.endswith('.cs') or n.endswith('.xaml')

files=filter(typeok,os.listdir(r'E:\各种论文\数据结构\esp8266测试程序(C#)\wifitest_esp8266'))

for x in files:

    print(x)


