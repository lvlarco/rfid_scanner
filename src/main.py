import RPi.GPIO as GPIO
from datetime import datetime
import time
from RPLCD.gpio import CharLCD
import requests

GPIO.setwarnings(False)

rfid_in = 15
GPIO.setup(rfid_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)


cat_dict = {"Theo": "000001",
            "Troll": "000002",
            "Tako": "000003",
            "Ollie": "000004"}


def directional_signal():
    """Sensor that is only activated when door is flung inwards"""
    pass


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


def lcd_display():
    # configure LCD and define GPIO mode
    cols = 16
    rows = 2
    wait_time = 3
    gpio_mode = "BOARD"

    if gpio_mode == "BOARD":
        lcd = CharLCD(pin_rs=19, pin_rw=None, pin_e=16, pins_data=[21, 18, 23, 24],
                      numbering_mode=GPIO.BOARD, cols=cols, rows=rows, dotsize=8)
    else:
        lcd = CharLCD(pin_rs=10, pin_rw=None, pin_e=23, pins_data=[9, 24, 11, 8], numbering_mode=GPIO.BCM)

    cat_name = get_cat_name("000004")

    # # second screen
    # message02 = str("It is so " + day_status)
    # message12 = str("in " + city_name.capitalize() + " today")
    # pos02 = center_cursor(message02, cols)
    # pos12 = center_cursor(message12, cols)
    #
    # # third screen
    # message03 = "We are at"
    # message13 = "{0}{1}".format(str(temperature), temp_units)
    # pos03 = center_cursor(message03, cols)
    # pos13 = center_cursor(message13, cols)

    while True:
        lcd.clear()
        if get_cat_name():
            cat_location = 'IN'
        else:
            cat_location = 'OUT'

        scan_time = last_rfid_scan()
        message01 = "{} is {}SIDE".format(cat_name, cat_location.upper())
        message11 = "He came {} at {}".format(cat_location.lower(), scan_time)
        pos01 = center_cursor(message01, cols)
        pos11 = center_cursor(message11, cols)
        lcd.cursor_pos = (0, pos01)
        lcd.write_string(message01)
        lcd.cursor_pos = (1, pos11)
        lcd.write_string(message11)
        time.sleep(wait_time)
        lcd.clear()
        # lcd.cursor_pos = (0, pos02)
        # lcd.write_string("It is so " + day_status)
        # lcd.cursor_pos = (1, pos12)
        # lcd.write_string("in " + city_name.capitalize() + " today")
        # time.sleep(wait_time)
        # lcd.clear()
        # lcd.cursor_pos = (0, pos03)
        # lcd.write_string(message03)
        # lcd.cursor_pos = (1, pos13)
        # lcd.write_string(str(temperature) + temp_units)
        time.sleep(wait_time)

    lcd.close()
    GPIO.cleanup()
