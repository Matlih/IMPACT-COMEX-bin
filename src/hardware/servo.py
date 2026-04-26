import time

def angle_to_pulse_width(angle):
    if angle < 0 or angle > 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    return int(500 + (angle * (2000 / 180)))


def set_servo_angle(pi, pin, angle, move_delay):
    pulse_width = angle_to_pulse_width(angle)
    pi.set_servo_pulsewidth(pin, pulse_width)
    time.sleep(move_delay)
