import math
import numpy as np


def to_quaternions(roll, pitch, yaw):
    roll = f_radians(roll)
    pitch = f_radians(pitch)
    yaw = f_radians(yaw)
    cy = math.cos(-yaw * 0.5)
    sy = math.sin(-yaw * 0.5)
    cr = math.cos(-roll * 0.5)
    sr = math.sin(-roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)

    w = cy * cr * cp + sy * sr * sp
    x = cy * sr * cp - sy * cr * sp
    y = cy * cr * sp + sy * sr * cp
    z = sy * cr * cp - cy * sr * sp
    return w, x, y, z


def to_euler(w, x, y, z):
    # roll(x - axis rotation)
    sinr = +2.0 * (w * x + y * z)
    cosr = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr, cosr)

    # pitch (y-axis rotation)
    sinp = +2.0 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = f_copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)
    # yaw (z-axis rotation)
    siny = +2.0 * (w * z + x * y)
    cosy = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny, cosy)
    return f_degrees(roll), f_degrees(pitch), f_degrees(yaw)


def quaternion_multiply(quaternion0, quaternion1):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    w = x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0
    x = -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0
    y = x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0
    z = -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0
    # print("XX", w, x, y, z)
    return w, x, y, z


def f_copysign(x, y):
    return abs(x) * sign(y)


def f_radians(deg):
    return deg * math.pi / 180.0


def f_degrees(rad):
    return rad * 180.0 / math.pi


def sign(x): return 1 if x >= 0 else -1