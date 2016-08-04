# Install_imaginarium
Install process for hybrid drone cycle robot.

# Pinout for cycle drone :
- GPIO23 = servo-pan
- GPIO24 = servo-tilt
- GPIO26 = brushless 1
- GPIO19 = brushless 2
- GPIO13 = brushless 3
- GPIO6 = brushless 4

![Raspberry Pi 3 pinout](http://i.imgur.com/JEQzRdo.jpg)

# Drone drawing
The drone drawings are in [OnShape](https://cad.onshape.com/documents/f4d4c97e5ffdfa706e45c09e/w/39e162a0dcdda166288d931f/e/9e4372879e71d8f50a5a7206) CAO online tool.

# BOM
- 4 ESC 12A
- 4 2204 2300kV brushless motors
- 4 propellers 3 pals
- 1 Raspberry Pi 3 (enlarged mounting holes to 3mm diameter)
- 1 Power supply plate with XT60 connector
- 4m of 3mm glass fiber beam
- 4 3x25 nut and bolt
- 4 3x40 nut and bolt
- 2 servo sg90

# Wifi configuration (WIFI N)
For the moment, let's install a classical WIFI 802.11N dongle as [EDIMAX-EW-7811UN](https://www.amazon.fr/Edimax-EW-7811UN-Nano-Adaptateur-sans/dp/B003MTTJOY) Or use the integrated Wifi of the RPI3
- connect the WIFI dongle to the card
- Edit the file /etc/network/interfaces and add the following lines :
```
allow-hotplug wlan0
iface wlan0 inet dhcp
  wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```
- Edit the file /etc/wpa_supplicant/wpa_supplicant.conf which must be like this :
```
ctrl_interface=/var/run/wpa_supplicant
network={
    ssid="XXXXXXXXXX"
    psk="xxxxxxx"
}
```
- sudo reboot
The Pi shall connect to your WIFI. The Pi is now able to live completely wireless.

# How to access GPIO of the Raspberry Pi 3
It is very simple.
In command line type ```sudo pigpiod```
Then, in Python :

```
import pigpio
pi = pigpio.pi()
pi.set_servo_pulsewidth(id, t)
```

with id : the number of the GPIO (NOT OF THE PIN!!!) and t the time of impulsion in micro second (from 1000 to 2000)




