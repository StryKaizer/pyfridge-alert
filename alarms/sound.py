from time import sleep


def play_sound(arduino, pin_sound):
    led_status = 1
    while True:
        if led_status:
            led_status = 0
        else:
            led_status = 1
        arduino.digitalWrite(pin_sound, 1)
        sleep(2)
        arduino.digitalWrite(pin_sound, 0)
