import time
import RPi.GPIO as GPIO
import concurrent
from kinematics import inverse_kinematics
from RpiMotorLib import RpiMotorLib

def _convert(target_angle, curr_steps, reduc):
    curr_angle = (curr_steps * step_angle) % 360
    angle_diff = target_angle - curr_angle

    if angle_diff > 0:
        direction = True # CCW
    else:
        direction = False # CW
    
    steps = int((abs(angle_diff) / step_angle) * reduc)

    return steps, direction

x = 0 # target x in mm
y = 200 # target y in mm

step_angle = 1.8 / 4

base_dir_pin = 20
base_step_pin = 21
base_reduc = 25

joint_dir_pin = 26
joint_step_pin = 19
joint_reduc = 20.5

theta1, theta2 = inverse_kinematics(x, y)

base_steps, base_dir = _convert(theta1, 0, base_reduc)
joint_steps, joint_dir = _convert(theta2, 0, joint_reduc)

motor_base = RpiMotorLib.A4988Nema(base_dir_pin, base_step_pin, (-1, -1, -1), "DRV8825")
motor_joint = RpiMotorLib.A4988Nema(joint_dir_pin, joint_step_pin, (-1, -1, -1), "DRV8825")

with concurrent.futures.ThreadPoolExecutor() as executor:
    arm_one = executor.submit(motor_base.motor_go, base_dir, "1/4", base_steps, 0.001, False, 0.05)
    arm_two = executor.submit(motor_joint.motor_go, joint_dir, "1/4", joint_steps, 0.001, False, 0.05)