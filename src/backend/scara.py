# Name: robot.py
# Author: Carter Hidalgo
#
# Purpose: Provide methods for controlling the scara

import concurrent.futures
import Rpi.GPIO as GPIO
from kinematics import inverse_kinematics
from RpiMotorLib import RpiMotorLib

class Scara:
    def __init__(self):
        self.base_dir_pin = 20
        self.base_step_pin = 21

        self.z_dir_pin = 26
        self.z_step_pin = 19
        
        self.joint_dir_pin = 6
        self.joint_step_pin = 13
        
        self.motor_base = RpiMotorLib.A4988Nema(self.base_dir_pin, self.base_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_z = RpiMotorLib.A4988Nema(self.z_dir_pin, self.z_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_joint = RpiMotorLib.A4988Nema(self.joint_dir_pin, self.joint_step_pin, (-1, -1, -1), "DRV8825")

        self.fullstep_angle = 1.8
        self.step_angle = self.fullstep_angle / 4
        self.steps_per_rev = int(360 / self.step_angle)
        
        self.base_steps = 0
        self.z_steps = 0
        self.joint_steps = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def _convert(self, target_angle, curr_steps):
        curr_angle = (curr_steps * self.step_angle) % 360
        angle_diff = target_angle - curr_angle

        if angle_diff > 0:
            direction = True  # CCW
        else:
            direction = False  # CW

        steps = int(abs(angle_diff) / self.step_angle)

        return steps, direction

    def move(self, x, y):
        theta1, theta2 = inverse_kinematics(x, y)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            base_steps, base_dir = Scara._convert(theta1, self.base_steps)
            joint_steps, joint_dir = Scara._convert(theta2, self.joint_steps)

            print(f"base: (step={base_steps}, dir={base_dir})")
            print(f"joint: (step={joint_steps}, dir={joint_dir})")

            # arm_one = executor.submit(self.motor_base.motor_go, base_dir, "1/4", base_steps, 0.005, False, 0.05)
            # arm_two = executor.submit(self.motor_joint.motor_go, joint_dir, "1/4", joint_steps, 0.005, False, 0.05)

            # arm_one.result()
            # arm_two.result()

            self.base_steps += base_steps * (1 if base_dir else -1)
            self.joint_steps += joint_steps * (1 if joint_dir else -1)

    def calibrate(self):
        print("calibrating scara")