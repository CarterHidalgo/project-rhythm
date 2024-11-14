# Name: kinematics.py
# Author: Carter Hidalgo
#
# Purpose: code for inverse kinematic equations

from math import acos, atan, sin, cos, sqrt, pi

def inverse_kinematics(x, y):
    L1 = 100 # length of arm 1
    L2 = 100 # length of arm 2

    theta2 = acos((sqrt(x) + sqrt(y) - sqrt(L1) - sqrt(L2)) / (2 * L1 * L2))
    if(x < 0 & y < 0):
        theta2 = (-1) * theta2
  
    theta1 = atan(x / y) - atan((L2 * sin(theta2)) / (L1 + L2 * cos(theta2)))
    
    theta2 = (-1) * theta2 * 180 / pi
    theta1 = theta1 * 180 / pi

    # Angles adjustment depending in which quadrant the final tool coordinate x,y is
    if(x >= 0 & y >= 0):
        theta1 = 90 - theta1
    
    if(x < 0 & y > 0):
        theta1 = 90 - theta1
    
    if(x < 0 & y < 0):
        theta1 = 270 - theta1
        phi = 270 - theta1 - theta2
        phi = (-1) * phi
        
    if(x > 0 & y < 0):
        theta1 = -90 - theta1
    
    if(x < 0 & y == 0):
        theta1 = 270 + theta1
    
    # Calculate "phi" angle so gripper is parallel to the X axis
    phi = 90 + theta1 + theta2
    phi = (-1) * phi

    # Angle adjustment depending in which quadrant the final tool coordinate x,y is
    if(x < 0 & y < 0):
        phi = 270 - theta1 - theta2
    
    if(abs(phi) > 165):
        phi = 180 + phi

    theta1 = round(theta1)
    theta2 = round(theta2)
    phi = round(phi)

    return theta1, theta2, phi

print(f"result: {inverse_kinematics(100, 100)}")