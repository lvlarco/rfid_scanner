import serial

port = serial.Serial('/dev/ttyS0', 9600, timeout=0.2)

while True:
    rcv = port.readline()
    if len(rcv) > 10:
        print("Tag: {}".format(str(rcv)))
