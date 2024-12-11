# Name: kinematics.py
# Author: chatGPT
#
# Purpose: code for inverse kinematic equations

from math import atan2, acos, sqrt, sin, cos, pi

def inverse_kinematics(x, y):
    # L1 = 231.8  # Length of the first link in mm
    # L2 = 146.0  # Length of the second link in mm

    L1 = 226
    L2 = 136.5

    # temporary values for testing with SCARA simulator (see https://www.geogebra.org/m/E9g4q7F5)
    # L1 = 2.3
    # L2 = 1.3

    # Calculate the distance from the origin to the target point
    distance = sqrt(x**2 + y**2)

    # Check if the target is reachable
    if distance > (L1 + L2) or distance < abs(L1 - L2):
        return None, None  # Target out of reach

    # Calculate theta2 using the law of cosines
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    theta2 = acos(cos_theta2)  # In radians

    # Calculate theta1 using the law of cosines and atan2 for direction
    theta1 = atan2(y, x) - atan2(L2 * sin(theta2), L1 + L2 * cos(theta2))

    # Convert angles from radians to degrees
    theta1 = theta1 * 180 / pi
    theta2 = theta2 * 180 / pi

    # Calculate phi to ensure the end effector is parallel to the x-axis
    phi = (-theta2) + (90 - theta1)

    # Return angles rounded to one decimal place
    return round(theta1, 1), round(theta2, 1), round(phi, 1)