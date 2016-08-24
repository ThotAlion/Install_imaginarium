import pigpio
import zmq
import time

IP = '0.0.0.0'
port = '8000'
dt = 1
lock = True
mockup = True

c = zmq.Context()
s = c.socket(zmq.REP)
s.bind("tcp://"+IP+":"+port)

# ouverture des GPIO
pi = pigpio.pi()

while True:
    try:
        if lock == False:
            reply = s.recv_json()
            if reply.has_key("pad"):
                pad = reply["pad"]
                # pour le thrustmaster
                # thr = (-pad["thrust"]+1)*1000
                # yaw = pad["stickYaw"]*50
                # pour la xbox
                thr = 1000*(abs(pad["thrust"])+1)
                yaw = pad["stickYaw"]*50
                set_thrust([thr+yaw,thr+yaw,thr-yaw,thr-yaw],pi,mockup)
                if pad["Back"] == 1:
                    lock = True
            else:
                set_thrust([1000,1000,1000,1000],pi,mockup)
            
        else:
            set_thrust([1000,1000,1000,1000],pi,mockup)
            reply = s.recv_json()
            if reply.has_key("pad"):
                pad = reply["pad"]
                if pad["Start"] == 1:
                    lock = False
    except:
        set_thrust([1000,1000,1000,1000],pi,mockup)

    time.sleep(dt)

def set_thrust(thrust,pi,mockup):
    # limitation
    if len(thrust)==4:
        for i in range(4):
            if thrust[i]<1000:
                thrust[i]=1000
            if thrust[i]>2000:
                thrust[i]=2000    
    if mockup == True:
        print thrust
        pi.set_servo_pulsewidth(26, 0)
        pi.set_servo_pulsewidth(19, 0)
        pi.set_servo_pulsewidth(13, 0)
        pi.set_servo_pulsewidth( 6, 0)
    else:
        # mapping 1->26; 2->19; 3->13 and 4->6
        pi.set_servo_pulsewidth(26, thrust[0])
        pi.set_servo_pulsewidth(19, thrust[1])
        pi.set_servo_pulsewidth(13, thrust[2])
        pi.set_servo_pulsewidth( 6, thrust[3])