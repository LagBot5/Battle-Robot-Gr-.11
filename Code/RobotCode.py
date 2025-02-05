from machine import Pin, PWM, ADC
import time #importing time for delay
from servo import Servo
import utime

import network
import socket
import urequests as requests

ssid = "CYBERTRON"
pw = "Mr.LamYo"



wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pw)

while wlan.isconnected() == False:
    print ("Connecting... ")
    time.sleep(1)
print("You have connected!")

wlanInfo = wlan.ifconfig()
print("My Pico's IP adress is ... ", wlanInfo[0])
#192.168.2.243

def get_html(html_name):
    with open(html_name, "r") as file:
        html = file.read()
        return html

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

STATE_OFF = 0

#OUT1  and OUT2
In1=Pin(6,Pin.OUT) 
In2=Pin(7,Pin.OUT)  
EN_A=Pin(8,Pin.OUT)

#OUT3  and OUT4
In3=Pin(4,Pin.OUT)  
In4=Pin(3,Pin.OUT)  
EN_B=Pin(2,Pin.OUT)

righthook= 26
lefthook= 27

global State
State = STATE_OFF
StateTime = 0

def setStateTimeToNow():
    global StateTime
    StateTime = utime.ticks_ms
    global StateTime2
    StateTime2 = utime.ticks_ms
    
global State

now = time.ticks_ms()

EN_A.high()
EN_B.high()


    
rightServo = Servo(righthook)
leftServo = Servo(lefthook)

        
# Forward
def move_forward():
    In1.high()
    In2.low()
    In3.high()
    In4.low()
    
# Backward
def move_backward():
    In1.low()
    In2.high()
    In3.low()
    In4.high()
    
#Turn Right
def turn_right():
    In1.low()
    In2.low()
    In3.high()
    In4.low()
    
#Turn Left
def turn_left():
    In1.high()
    In2.low()
    In3.low()
    In4.low()
   
#Stop
def Stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()    
    
print("waiting for requests...")
while True:           
    try:
        now = time.ticks_ms()
        State = STATE_OFF
        cl, addr = s.accept()
        r = cl.recv(1024)
        r = str(r)
        print("request is:", r)
        
        #requests here
        forward = r.find("forward")
        reverse = r.find("reverse")
        right = r.find("right")
        left = r.find("left")
        stop = r.find("stop")
        retreat = r.find("retreat")
        charge = r.find("charge")
        
        if forward > -1:
            move_forward()
            print ("Forward")
            
        elif reverse > -1:
            move_backward()
            print("Backward") 
        
        elif right > -1:
            turn_right()
            print("Right")
        
        elif left > -1:
            turn_left()
            print("Left")
            
        elif stop > -1:
            Stop()
            print("Stop")
            
        if charge > -1:
            rightServo.move(180)
            leftServo.move(180)
            
        if retreat > -1:
            leftServo.move(0)
            rightServo.move(0)
                  
        print('sending response')
        response = get_html("website.html")
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print(e)
