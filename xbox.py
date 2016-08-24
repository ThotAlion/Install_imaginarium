import pygame
import zmq
import time

IP = '192.168.1.34'

c = zmq.Context()
s = c.socket(zmq.REQ)
s.connect('tcp://'+IP+':8000')

pygame.init()
pygame.joystick.init()

goon = True
req = {}
req["pad"] = {}
while goon:
    t0 = time.clock()
    pygame.event.get()
    j = pygame.joystick.Joystick(0)
    j.init()
    req["pad"]["stickPitch"] = j.get_axis(3)
    req["pad"]["stickRoll"] = j.get_axis(4)
    req["pad"]["stickYaw"] = j.get_axis(0)
    req["pad"]["thrust"] = j.get_axis(2)
    req["pad"]["stickPal"] = j.get_axis(0)
    req["pad"]["stickTrim"] = j.get_hat(0)
    req["pad"]["A"] = j.get_button(0)
    req["pad"]["B"] = j.get_button(1)
    req["pad"]["X"] = j.get_button(2)
    req["pad"]["Y"] = j.get_button(3)
    req["pad"]["L"] = j.get_button(4)
    req["pad"]["R"] = j.get_button(5)
    req["pad"]["Back"] = j.get_button(6)
    req["pad"]["Start"] = j.get_button(7)
    
    s.send_json(req)
    a = s.recv_json()
    time.sleep(0.1)