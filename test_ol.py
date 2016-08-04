import pigpio
import zmq
import time

IP = '0.0.0.0'
port = '8000'

c = zmq.Context()
s = c.socket(zmq.REP)
s.bind("tcp://"+IP+":"+port)

pi = pigpio.pi()


reply = s.recv_json()
    if reply.has_key("pad"):
        pad = reply["pad"]
        thr = (-pad["thrust"]+1)*1000
        yaw = pad["stickYaw"]*50

        pi.set_servo_pulsewidth(26, 0)
        pi.set_servo_pulsewidth(19, thr+yaw)
        pi.set_servo_pulsewidth(13, thr-yaw)
        pi.set_servo_pulsewidth( 6, thr)

time.sleep(5)

thr = 2000
pi.set_servo_pulsewidth(26, thr)
pi.set_servo_pulsewidth(19, thr)
pi.set_servo_pulsewidth(13, thr)
pi.set_servo_pulsewidth( 6, thr)

time.sleep(5)

thr = 0
pi.set_servo_pulsewidth(26, thr)
pi.set_servo_pulsewidth(19, thr)
pi.set_servo_pulsewidth(13, thr)
pi.set_servo_pulsewidth( 6, thr)