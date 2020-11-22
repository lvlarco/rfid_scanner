import serial
import time
while True:
    print("wait")
    ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.2)
    by = ser.inWaiting()
    data = ":".join("{02x}".format(ord(by)))
    print(ser.read(data))
    time.sleep(5)
