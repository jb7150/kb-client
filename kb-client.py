#!/usr/bin/env python3

# kb-client2.py
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import socket

HOST = ''  # The server's hostname or IP address
IPV6HOST = ''
PORT = 65433  # The port used by the server

#s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# up    = input & 0b1000 0000 (0x80)
# down  = input & 0b0100 0000 (0x40)
# left  = input & 0b0010 0000 (0x20)
# right = input & 0b0001 0000 (0x10)
# fire  = input & 0b0000 1000 (0x08)

pygame.init()
window = pygame.display.set_mode((400, 400))
pygame.display.set_caption("C64 controller")
#background_color = (115, 115, 255)
background_color = (30, 30, 30)
inactive_color = (128,128,128)
#active_color = (0,255,0)
active_color = (143,188,143)
fire_active = (255,48,48)
programIcon = pygame.image.load('c64icon.png')
pygame.display.set_icon(programIcon)

window.fill(background_color)

#Font = pygame.font.SysFont('timesnewroman',30)
Font = pygame.font.Font(None,30)

input_box = pygame.Rect(10,10,140,32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')


# 3rd parameter is font colour
# 4th parameter is Font background
up_on  = Font.render("Up", False, active_color, background_color)
up_off = Font.render("Up", False, inactive_color, background_color)

down_on  = Font.render("Down", False, active_color, background_color)
down_off = Font.render("Down", False, inactive_color, background_color)

left_on  = Font.render("Left", False, active_color, background_color)
left_off = Font.render("Left", False, inactive_color, background_color)

right_on  = Font.render("Right", False, active_color, background_color)
right_off = Font.render("Right", False, inactive_color, background_color)

fire_on  = Font.render("Fire", False, fire_active, background_color)
fire_off = Font.render("Fire", False, inactive_color, background_color)

up_rect = up_on.get_rect()
up_rect.center = (100,100)

down_rect = down_on.get_rect()
down_rect.center = (100,300)

left_rect = left_on.get_rect()
left_rect.center = (50,200)

right_rect = right_on.get_rect()
right_rect.center = (150,200)

fire_rect = fire_on.get_rect()
fire_rect.center=(300,200)

pygame.display.flip()


def sendstringoversocket(I_string):
    L_text = ""
    L_text = I_string    
    s.sendall(L_text.encode())
    
def trytoconnect(I_hoststring):
    IPV6HOST = I_hoststring
    print("trying to connect to ipv4: {}, port:{}".format(IPV6HOST,PORT))
    s.connect((IPV6HOST, PORT))
    print('connected to server at {}, {}'.format(IPV6HOST, PORT))

print("waiting to connect to server...")
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))
#print('connected to server at {}, {}'.format(HOST, PORT))

#s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
#s.connect((IPV6HOST, PORT))
#print('connected to server at {}, {}'.format(IPV6HOST, PORT))


box_color = color_inactive
box_active=False
box_text = ''

up_status = up_off
down_status = down_off
left_status = left_off
right_status = right_off
fire_status = fire_off
mainloop=True
V_sendVal = 'udlrf'
inconnectmode = True
#V_sendValprev = V_sendVal
while mainloop:

    for event in pygame.event.get():
        #L_sendit = False
        if (event.type == pygame.QUIT):
            mainloop = False
        if (inconnectmode == False):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    V_sendVal = V_sendVal.replace('u','U')
                    up_status = up_on
                if event.key == pygame.K_s:
                    V_sendVal = V_sendVal.replace('d','D')
                    down_status = down_on
                if event.key == pygame.K_a:
                    V_sendVal = V_sendVal.replace('l','L')
                    left_status = left_on
                if event.key == pygame.K_d:
                    V_sendVal = V_sendVal.replace('r','R')
                    right_status = right_on
                if event.key == pygame.K_SPACE:
                    V_sendVal = V_sendVal.replace('f','F')
                    fire_status = fire_on
                sendstringoversocket((V_sendVal))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    V_sendVal = V_sendVal.replace('U','u')
                    up_status = up_off
                if event.key == pygame.K_s:
                    V_sendVal = V_sendVal.replace('D','d')
                    down_status = down_off
                if event.key == pygame.K_a:
                    V_sendVal = V_sendVal.replace('L','l')
                    left_status = left_off
                if event.key == pygame.K_d:
                    V_sendVal = V_sendVal.replace('R','r')
                    right_status = right_off
                if event.key == pygame.K_SPACE:
                    V_sendVal = V_sendVal.replace('F','f')
                    fire_status = fire_off
                sendstringoversocket((V_sendVal))
            window.blit(up_status,up_rect)
            window.blit(down_status,down_rect)
            window.blit(left_status,left_rect)
            window.blit(right_status,right_rect)
            window.blit(fire_status,fire_rect)
            
        else: 
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (input_box.collidepoint(event.pos)):
                    box_active = not box_active
                else:
                    box_active = False
                box_color = color_active if box_active else color_inactive
            if (event.type == pygame.KEYDOWN):
                if (box_active):
                    if (event.key == pygame.K_RETURN):
                        #print(box_text)
                        trytoconnect(box_text)
                        inconnectmode = False
                    elif (event.key == pygame.K_BACKSPACE):
                        box_text = box_text[:-1]
                    else:
                        box_text += event.unicode
            
            window.fill((30,30,30))
            txt_surface = Font.render(box_text, True, box_color)
            L_boxwidth = max(200, txt_surface.get_width() + 10)
            input_box.w = L_boxwidth
            
            window.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(window, box_color,input_box,2)
            pygame.display.flip()
    pygame.display.update()
    #clock.tick(60)

s.close()
pygame.quit()

