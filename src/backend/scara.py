# Name: robot.py
# Author: Carter Hidalgo
#
# Purpose: Provide methods for controlling the scara

import concurrent.futures
import threading
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from time import sleep
from backend.kinematics import inverse_kinematics

class Scara:
    def __init__(self):
        self.base_dir_pin = 20
        self.base_step_pin = 21
        
        self.joint_dir_pin = 26
        self.joint_step_pin = 19

        self.end_dir_pin = 6
        self.end_step_pin = 13

        self.z_dir_pin = 22
        self.z_step_pin = 4

        self.servo_pin = 17
        
        self.motor_base = RpiMotorLib.A4988Nema(self.base_dir_pin, self.base_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_joint = RpiMotorLib.A4988Nema(self.joint_dir_pin, self.joint_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_end = RpiMotorLib.A4988Nema(self.end_dir_pin, self.end_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_z = RpiMotorLib.A4988Nema(self.z_dir_pin, self.z_step_pin, (-1, -1, -1), "A4988")

        self.fullstep_angle = 1.8
        self.step_angle = self.fullstep_angle / 4
        self.steps_per_rev = int(360 / self.step_angle)
        
        self.base_ang = 0
        self.joint_ang = 0
        self.servo_ang = 90

        self.z_steps = 0

        self.base_limit_pin = 18
        self.joint_limit_pin = 23
        self.z_limit_pin = 24
        self.end_limit_pin = 25

        self.base_reduc = 25
        self.joint_reduc = 20.45
        self.end_reduc = 5.65

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.servo_pin, GPIO.OUT)
        GPIO.setup(self.base_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.joint_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.z_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.end_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.pwm = GPIO.PWM(self.servo_pin, 50)
        self.pwm.start(0)

    def _convert(self, target_angle, curr_angle, reduc):
        angle_diff = target_angle - curr_angle

        if angle_diff > 0:
            direction = True # CCW
        else:
            direction = False # CW
        
        steps = int((abs(angle_diff) / self.step_angle) * reduc)

        return steps, direction

    def _set_angle(self, angle):
        duty = angle / 18 + 2.5
        self.pwm.ChangeDutyCycle(duty)
        sleep(0.7)  
        self.pwm.ChangeDutyCycle(0)

    def move(self, x, y, debug):
        theta1, theta2 = inverse_kinematics(x, y)
        
        base_steps, base_dir = self._convert(theta1, self.base_ang, self.base_reduc)
        joint_steps, joint_dir = self._convert(theta2, self.joint_ang, self.joint_reduc)

        if debug:
            print(f"coord: (x={x}, y={y})")
            print(f"angles: (theta1={theta1}, theta2={theta2})")
            print(f"base: (step={base_steps}, dir={base_dir})")
            print(f"joint: (step={joint_steps}, dir={joint_dir})")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            arm_one = executor.submit(self.motor_base.motor_go, base_dir, "1/4", base_steps, 0.001, False, 0.05)
            arm_two = executor.submit(self.motor_joint.motor_go, not joint_dir, "1/4", joint_steps, 0.001, False, 0.05)

            arm_one.result()
            arm_two.result()

            self.base_ang = theta1
            self.joint_ang = theta2

    def calibrate(self):
        self.calibrate_z()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            base = executor.submit(self.calibrate_base)
            joint = executor.submit(self.calibrate_joint)

            base.result()
            joint.result()

    def calibrate_base(self):
        base_cal_thread = threading.Thread(target=self.motor_base.motor_go, args=(True, "1/4", int(800 * self.base_reduc), 0.0005, False, 0.05))

        if not GPIO.input(self.base_limit_pin):
            base_cal_thread.start()
        
        while not GPIO.input(self.base_limit_pin):
            sleep(0.1)
        self.motor_base.motor_stop()

        sleep(0.5)

        self.motor_base.motor_go(False, "1/4", 9800, 0.0004, False, 0.05)
        self.motor_base.motor_stop()

        self.base_ang = 90

    def calibrate_joint(self):
        joint_cal_thread = threading.Thread(target=self.motor_joint.motor_go, args=(True, "1/4", int(800 * self.joint_reduc), 0.0005, False, 0.05))

        if not GPIO.input(self.joint_limit_pin):
            joint_cal_thread.start()

        while not GPIO.input(self.joint_limit_pin):
            sleep(0.1)
        self.motor_joint.motor_stop()

        sleep(0.5)

        self.motor_joint.motor_go(False, "1/4", 6900, 0.0004, False, 0.05)
        self.motor_joint.motor_stop()

        self.joint_ang = 0

    def calibrate_end(self):
        end_cal_thread = threading.Thread(target=self.motor_end.motor_go, args=(True, "1/4", int(800 * self.end_reduc), 0.001, False, 0.05))

        if not GPIO.input(self.end_limit_pin):
            end_cal_thread.start()

        while not GPIO.input(self.end_limit_pin):
            sleep(0.1)
        self.motor_end.motor_stop()

        sleep(0.5)

    def calibrate_z(self):
        self.motor_z.motor_go(False, "1/4", 9600, 0.0004, False, 0.05)
        self.z_steps = 9600

    def grab(self):
        if(self.servo_ang != 45):
            self._set_angle(45)
            self.servo_ang = 45

    def release(self):
        if(self.servo_ang != 160):
            self._set_angle(160)
            self.servo_ang = 160
    
    def set_servo(self, angle):
        self._set_angle(angle)

    def close(self):
        self.pwm.stop()
        del self.pwm

    def test(self):
        while True:
            print(GPIO.input(self.joint_limit_pin))