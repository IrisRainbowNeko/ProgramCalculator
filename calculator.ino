#include <PWM.h>

//74LS138的ABC口分别接Arduino的D7、D6、D5
const int A=7; 
const int B=6;
const int C=5;//C为高位
const int pwm_pin=10;
const int music=11;

bool key_state[6][8];//行，列
bool waveon;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(A,OUTPUT);
  pinMode(B,OUTPUT);
  pinMode(C,OUTPUT);
  InitTimersSafe();
}

void loop() {  
  // put your main code here, to run repeatedly:
 lineCycle();
}
void lineCycle(){
  for(int line=0;line<6;line++){ //从第1行到第6行
    int a=line&1;
    int b=line&2;
    int c=line&4;
  
    digitalWrite(A,a);
    digitalWrite(B,b);
    digitalWrite(C,c);
    delayMicroseconds(10);
    shiftRead(3,4,2,line);

    docmd(getData());
  }
}

void checkWave(){
  sendData("wave",analogRead(A0));
}

void docmd(String cmd){
  //Serial.print(cmd);
  int index=cmd.indexOf(",");
  String head=index>0?cmd.substring(0,index):cmd;
  if(head.equals("freq")){
    int freq=cmd.substring(index+1).toInt();
    SetPinFrequencySafe(pwm_pin, freq);
  }else if(head.equals("duty")){
    int duty=cmd.substring(index+1).toInt();
    pwmWriteHR(pwm_pin, duty);
  }else if(head.equals("wave")){
    checkWave();
  }else if(head.equals("tone")){
    int ton=cmd.substring(index+1).toInt();
    if(ton<=0)noTone(music);
    else{
      noTone(music);
      tone(music,ton);
    }
  }
}

String getData(){
  //接收树莓派消息
    String recvdata="";
    while(Serial.available()>0){
      char ch=char(Serial.read());
      if(ch=='<'){
        while((ch=Serial.read())!='>'){
          if(ch>0)
            recvdata+=ch;
        }
        break;
      }
    }
    return recvdata;
}

byte shiftRead(int pin_ld,int pin_clk,int pin_data,int line){//适用于74LS194
  pinMode(pin_ld,OUTPUT);     //接S0
  pinMode(pin_clk,OUTPUT);    //接CLK
  pinMode(pin_data,INPUT);    //接SL
  
  digitalWrite(pin_clk,LOW);
  delayMicroseconds(1);
  digitalWrite(pin_ld,HIGH);
  delayMicroseconds(1);
  makePulse(pin_clk);
  delayMicroseconds(1);
  digitalWrite(pin_ld,LOW); 
  byte data=0;
  for(int i=0;i<8;i++){
    data<<=1;
    data|=digitalRead(pin_data);
    makePulse(pin_clk);
  }
  byte comparand =0x80; //比较数初始为1000 0000
  for(int i=0;i<8;i++){
    byte temp=(~data)&comparand;
    if(temp == comparand){
      if(!key_state[line][i]){
        sendData("keydown",line,(i+4)%8);
        key_state[line][i]=1;
      }
    }else{
      if(key_state[line][i]){
        sendData("keyup",line,(i+4)%8);
        key_state[line][i]=0;
      }
    }
    comparand>>=1;
  }
  
  //delay(200);
}
void sendData(String head,int value){
  String s_data = "("+head +","+ String(value) +")";
  Serial.print(s_data);
  delayMicroseconds(2);  
}
void sendData(String head,int x,int y){
  String s_data = "("+head +","+ String(x) +","+String(y)+")";
  Serial.print(s_data);
  delayMicroseconds(2);  
}

void makePulse(int p_pin){//脉冲产生信号
  digitalWrite(p_pin,LOW);
  delayMicroseconds(1);
  digitalWrite(p_pin,HIGH);
  delayMicroseconds(1);
  digitalWrite(p_pin,LOW);
  delayMicroseconds(1);
}
