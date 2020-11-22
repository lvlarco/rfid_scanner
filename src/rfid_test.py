from serial import Serial
import time

baudrate = 9600
port = Serial('/dev/ttyAMA0', baudrate, timeout=0.2)

while True:
    print("Waiting")
    rcv = port.readline()
    rcv = ":".join("{:02x}".format(ord(c)) for c in rcv)
    if len(rcv) > 1:
        print("Tag: {}".format(str(rcv)))
    time.sleep(1)
