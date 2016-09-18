import pigpio
import zmq
import time


# declaration of constants
# control sampling time (s)
dt = 0.010
# limits of thrust
thrustmin = 1200
thrustmax = 1600
thrustzero = 1000
# plug the motors ?
mockup = True
# IP adress of the XBOX
IP_xbox = '10.0.0.3'
# IP adress of the vision system
IP_vision = '127.0.0.1'

# declaration of routines
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

# initialization of the robot
# Open GPIO
pi = pigpio.pi()

# Open ZMQ ports for request
c_xbox = zmq.Context()
s_xbox = c_xbox.socket(zmq.REQ)
s_xbox.connect('tcp://'+IP_xbox+':8000')
poll_xbox = zmq.Poller()
poll_xbox.register(s_xbox,zmq.POLLIN)

c_vision = zmq.Context()
s_vision = c_vision.socket(zmq.REQ)
s_vision.connect('tcp://'+IP_vision+':8100')
poll_vision = zmq.Poller()
poll_vision.register(s_vision,zmq.POLLIN)

# Infinite Loop
while True:
    t0=time.time()
    
    ## Ask the values of the sensors
    # Pad
    s_xbox.send_json({"ask":"1"})
    pad = s_xbox.recv_json()
    # Vision
    s_vision.send_json({"ask":"1"})
    vision = s_vision.recv_json()
    # Lidar
    
    
    
    ## Compute the actions
    # switch between manual and AP
    if manual == 1:
        thrust = thrustman
        delta = deltaman
    else:
        thrust = thrustauto
        delta = deltaauto
    
    # pilot delta oriented
    thrustD = thrust+delta
    thrustG = thrust-delta
    if thrustD<thrustmin:
        thrustD = thrustmin
        thrustG = thrust-delta
    if thrustG<thrustmin:
        thrustG = thrustmin
        thrustD = thrust+delta
    if thrustD>thrustmax:
        thrustD = thrustmax
        thrustG = thrust-delta
    if thrustG>thrustmax:
        thrustG = thrustmax
        thrustD = thrust+delta
        
    ## Act
    set_thrust([thrustG,thrustG,thrustD,thrustD],pi,mockup)
    
    #wait the end of the cycle
    while (time.time()-t0)<dt:
        time.sleep(0.001)
