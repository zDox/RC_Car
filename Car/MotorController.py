import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient
import constants as const

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio  # importing GPIO library


class Motor:
    def __init__(self):
        self.pi = pigpio.pi()
        self.speed = 1500
        self.pi.set_servo_pulsewidth(const.ESC_PIN, 0)

    def set_speed(self, speed):
        if const.ESC_MIN_VALUE <= speed <= const.ESC_MAX_VALUE:
            self.speed = speed
            self.pi.set_servo_pulsewidth(const.ESC_PIN, self.speed)

    def stop(self):  # This will stop every action your Pi is performing for ESC ofcourse.
        self.pi.set_servo_pulsewidth(const.ESC_PIN, 0)
        self.pi.stop()

    def calibrate(self):
        self.pi.set_servo_pulsewidth(const.ESC_PIN, 0)
        print("Disconnect the battery and press Enter")
        inp = input()
        if inp == '':
            self.pi.set_servo_pulsewidth(const.ESC_PIN, const.ESC_MAX_VALUE)
            print(
                "Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = input()
            if inp == '':
                self.pi.set_servo_pulsewidth(const.ESC_PIN, const.ESC_MIN_VALUE)
                print("Wierd eh! Special tone")
                time.sleep(7)
                print("Wait for it ....")
                time.sleep(5)
                print("Im working on it, DONT WORRY JUST WAIT.....")
                self.pi.set_servo_pulsewidth(const.ESC_PIN, 0)
                time.sleep(2)
                print("Arming ESC now...")
                self.pi.set_servo_pulsewidth(const.ESC_PIN, const.ESC_MIN_VALUE)
                time.sleep(1)
                print("See.... uhhhhh")
