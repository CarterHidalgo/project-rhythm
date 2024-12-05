# Name: robot.py
# Author: Carter Hidalgo
#
# Purpose: Provide methods for controlling the scara

import concurrent.futures
import RPi.GPIO as GPIO
from backend.kinematics import inverse_kinematics
from RpiMotorLib import RpiMotorLib

class Scara:
    def __init__(self):
        self.base_dir_pin = 20
        self.base_step_pin = 21

        self.z_dir_pin = 6
        self.z_step_pin = 13
        
        self.joint_dir_pin = 26
        self.joint_step_pin = 19
        
        self.motor_base = RpiMotorLib.A4988Nema(self.base_dir_pin, self.base_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_z = RpiMotorLib.A4988Nema(self.z_dir_pin, self.z_step_pin, (-1, -1, -1), "DRV8825")
        self.motor_joint = RpiMotorLib.A4988Nema(self.joint_dir_pin, self.joint_step_pin, (-1, -1, -1), "DRV8825")

        self.fullstep_angle = 1.8
        self.step_angle = self.fullstep_angle / 4
        self.steps_per_rev = int(360 / self.step_angle)
        
        self.base_ang = 0
        self.z_ang = 0
        self.joint_ang = 0

        self.base_reduc = 25 # base is 20:1 reduction
        self.joint_reduc = 20.45 # joint is 16:1 reduction

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def _convert(self, target_angle, curr_angle, reduc):
        angle_diff = target_angle - curr_angle

        if angle_diff > 0:
            direction = True # CCW
        else:
            direction = False # CW
        
        steps = int((abs(angle_diff) / self.step_angle) * reduc)

        return steps, direction

    def move(self, x, y):
        theta1, theta2 = inverse_kinematics(x, y)
        
        base_steps, base_dir = self._convert(theta1, self.base_ang, self.base_reduc)
        joint_steps, joint_dir = self._convert(theta2, self.joint_ang, self.joint_reduc)

        print(f"base: (step={base_steps}, dir={base_dir})")
        print(f"joint: (step={joint_steps}, dir={joint_dir})")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            arm_one = executor.submit(self.motor_base.motor_go, base_dir, "1/4", base_steps, 0.0005, False, 0.05)
            arm_two = executor.submit(self.motor_joint.motor_go, not joint_dir, "1/4", joint_steps, 0.0005, False, 0.05)

            arm_one.result()
            arm_two.result()

    def calibrate(self):
        print("calibrating scara")