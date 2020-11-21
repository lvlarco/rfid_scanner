import serial

ser = serial.Serial("myUsbPortID", 9600)
by = ser.inWaiting()
print(ser.read(by))