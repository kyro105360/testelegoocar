#%% Load modules
import numpy as np
from urllib.request import urlopen
import socket
import sys
import json
import re
import matplotlib.pyplot as plt
import time
import pygame

##pygame init
pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Demo')

font = pygame.font.SysFont('Georgia',40,bold=True)

surfUp = font.render('up', True, 'white')
buttonUp = pygame.Rect(400,200,110,60)
surfDown = font.render('up', True, 'white')
buttonDown = pygame.Rect(400,400,110,60)
surfLeft = font.render('up', True, 'white')
buttonLeft = pygame.Rect(200,300,110,60)
surfRight = font.render('up', True, 'white')
buttonRight = pygame.Rect(600,300,110,60)


##robot car command
cmd_no = 0
off = [0.007,  0.022,  0.091,  0.012, -0.011, -0.05]
def cmd(sock, do, what = '', where = '', at = ''):
    global cmd_no
    cmd_no += 1
    msg = {"H":str(cmd_no)} # dictionary
    if do == 'move':
        msg["N"] = 3
        what = ' car '
        if where == 'forward':
            msg["D1"] = 3
        elif where == 'back':
            msg["D1"] = 4
        elif where == 'left':
            msg["D1"] = 1
        elif where == 'right':
            msg["D1"] = 2
        msg["D2"] = at # at is speed here
        where = where + ' '
    elif do == 'stop':
        msg.update({"N":1,"D1":0,"D2":0,"D3":1})
        what = ' car'
    elif do == 'rotate':
        msg.update({"N":5,"D1":1,"D2":at}) # at is an angle here
        what = ' ultrasonic unit'
        where = ' '
    elif do == 'measure':
        if what == 'distance':
            msg.update({"N":21,"D1":2})
        elif what == 'motion':
            msg["N"] = 6
        what = ' ' + what
    elif do == 'check':
        msg["N"] = 23
        what = ' off the ground'
    msg_json = json.dumps(msg)
    print(str(cmd_no) + ': ' + do + what + where + str(at), end = ': \n')
    try:
        sock.send(msg_json.encode())
    except:
        print('Error: ', sys.exc_info()[0])
        sys.exit()
    while 1:
        res = sock.recv(1024).decode()
        if '_' in res:
            break
    res = sock.recv(1024).decode()
    res = re.search('_(.*)}', res).group(1)
    if res == 'ok' or res == 'true':
        res = 1
    elif res == 'false':
        res = 0
    elif msg.get("N") == 6:
        res = res.split(",")
        res = [int(x)/16384 for x in res] # convert to units of g
        res[2] = res[2] - 1 # subtract 1G from az
        res = [round(res[i] - off[i], 4) for i in range(6)]
    else:
        res = int(res)
    print(res)
    return res


#%% Connect to car's WiFi
ip = "192.168.4.1"
port = 100
print('Connect to {0}:{1}'.format(ip, port))
car = socket.socket()
try:
    car.connect((ip, port))
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()
print('Connected!')

#%% Read first data from socket
print('Receive from {0}:{1}'.format(ip, port))
try:
    data = car.recv(1024).decode()
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()
print('Received: ', data)

#%% Main
speed = 150 
ang = [90, 10, 170]
dist = [0, 0, 0]
dist_min = 30
run = True
flag = 'stop'
while run:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.draw.rect(screen,(180,180,180), buttonUp)
    screen.blit(surfUp,(buttonUp.x +5, buttonUp.y+5))
    pygame.draw.rect(screen,(180,180,180), buttonDown)
    screen.blit(surfDown,(buttonDown.x +5, buttonDown.y+5))
    pygame.draw.rect(screen,(180,180,180), buttonLeft)
    screen.blit(surfLeft,(buttonLeft.x +5, buttonLeft.y+5))
    pygame.draw.rect(screen,(180,180,180), buttonRight)
    screen.blit(surfRight,(buttonRight.x +5, buttonRight.y+5))

    if event.type == pygame.MOUSEBUTTONDOWN:
        a,b=pygame.mouse.get_pos()
        if buttonUp.x <= a <= buttonUp.x + 110 and buttonUp.y <= b <= buttonUp.y +60:
            if flag != 'foward':
                cmd(car, do = 'move', where = 'forward', at = speed)
                flag = 'forward'
        elif buttonDown.x <= a <= buttonDown.x + 110 and buttonDown.y <= b <= buttonDown.y +60:
            if flag != 'back':
                cmd(car, do = 'move', where = 'back', at = speed)
                flag = 'back'
        elif buttonLeft.x <= a <= buttonLeft.x + 110 and buttonLeft.y <= b <= buttonLeft.y +60:
            if flag != 'left':
                cmd(car, do = 'move', where = 'left', at = speed)
                flag = 'left'
        elif buttonRight.x <= a <= buttonRight.x + 110 and buttonRight.y <= b <= buttonRight.y +60:
            if flag != 'right':
                cmd(car, do = 'move', where = 'right', at = speed)
                flag = 'right'
        else :
            if flag != 'stop':
                flag = 'stop'
                cmd(car, do = 'stop')
    else:
        if flag != 'stop':
            flag = 'stop'
            cmd(car, do = 'stop')
        
    pygame.display.update()
car.close()
            
    