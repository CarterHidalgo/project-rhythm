import time
import RPi.GPIO as GPIO
import concurrent.futures
from kinematics import inverse_kinematics
from RpiMotorLib import RpiMotorLib

def _convert(target_angle, curr_angle, reduc):
    angle_diff = target_angle - curr_angle

    if angle_diff > 0:
        direction = True # CCW
    else:
        direction = False # CW
    
    steps = int((abs(angle_diff) / step_angle) * reduc)

    return steps, direction

x = -200 # target x in mm
y = 200 # target y in mm

step_angle = 1.8 / 4

base_dir_pin = 20
base_step_pin = 21
base_reduc = 25
base_ang = 0

joint_dir_pin = 26
joint_step_pin = 19
joint_reduc = 20.45
joint_ang = 0

theta1, theta2 = inverse_kinematics(x, y)
print(f"theta1={theta1}, theta2={theta2}")

base_steps, base_dir = _convert(theta1, base_ang, base_reduc)
joint_steps, joint_dir = _convert(theta2, joint_ang, joint_reduc)

motor_base = RpiMotorLib.A4988Nema(base_dir_pin, base_step_pin, (-1, -1, -1), "DRV8825")
motor_joint = RpiMotorLib.A4988Nema(joint_dir_pin, joint_step_pin, (-1, -1, -1), "DRV8825")

with concurrent.futures.ThreadPoolExecutor() as executor:
    arm_one = executor.submit(motor_base.motor_go, base_dir, "1/4", base_steps, 0.001, False, 0.05)
    arm_two = executor.submit(motor_joint.motor_go, not joint_dir, "1/4", joint_steps, 0.001, False, 0.05)