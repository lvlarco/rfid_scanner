import RPi.GPIO as GPIO
from datetime import datetime
import time
from RPLCD.gpio import CharLCD
from serial import Serial

GPIO.setwarnings(False)

cols = 16
rows = 2
wait_time = 3

rfid_in = 15
GPIO.setup(rfid_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
baudrate = 9600
port = Serial('/dev/ttyAMA0', baudrate, timeout=0.2)

cat_dict = {"Theo": "aa:0f:08:00:03:d9:1a:14:45:03:b0:25:bb",
            "Troll": "000002",
            "Tako": "000003",
            "Ollie": "000004",
            "Oliver": "aa:0f:08:00:03:df:00:b2:d5:25:3a:a3:bb"}

lcd = CharLCD(pin_rs=19, pin_rw=None, pin_e=16, pins_data=[21, 18, 23, 24],
              numbering_mode=GPIO.BOARD, cols=cols, rows=rows, dotsize=8)


def directional_signal():
    """Sensor that is only activated when door is flung inwards"""
    return 'IN'


def reset_location():
    """Resets the RFID location to IN (True)"""
    cat_location = "in"
    return cat_location


def get_cat_name(rfid_signal):
    return list(cat_dict.keys())[list(cat_dict.values()).index(rfid_signal)]


def last_rfid_scan():
    return datetime.now().strftime('%H:%M')


def center_cursor(message, lcd_length):
    """Finds the cursor position to center message in LCD screen"""
    msg_length = len(message)
    cursor_pos = int((lcd_length - msg_length) / 2)
    return cursor_pos


def update_lcd_screen(cat):
    """Resets LCD screen and outputs the cat name with a timestamp"""
    lcd.clear()
    cat_location = directional_signal()
    scan_time = last_rfid_scan()
    message01 = "{} is {}SIDE".format(cat, cat_location.upper())
    message11 = "He walked {} at {}".format(cat_location.lower(), scan_time)
    pos01 = center_cursor(message01, cols)
    pos11 = center_cursor(message11, cols)
    lcd.cursor_pos = (0, pos01)
    lcd.write_string(message01)
    lcd.cursor_pos = (1, pos11)
    lcd.write_string(message11)


while True:
    rfid_tag = port.readline()
    rfid_tag = ":".join("{:02x}".format(ord(c)) for c in rfid_tag)
    cat_name = get_cat_name(rfid_tag)
    update_lcd_screen(cat_name)
    time.sleep(1)
