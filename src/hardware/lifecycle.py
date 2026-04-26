try:
    import pigpio # type: ignore[import-not-found]
except ImportError:
    pigpio = None

from src.hardware.servo import set_servo_angle
from src.hardware.led import set_led_output
from src.hardware.buzzer import set_buzzer_output


def connect():
    if pigpio is None:
        print("Warning: pigpio module not found. Hardware control disabled.")
        return None

    pi = pigpio.pi()
    if not pi.connected:
        print("Warning: pigpio daemon is not connected. Hardware control disabled.")
        pi.stop()
        return None

    return pi


def setup(pi, bins, closed_angle, move_delay):
    for bin_item in bins:
        has_servo = bin_item.get("hasServo", False)
        has_sensor = bin_item.get("hasSensor", False)
        has_led = bin_item.get("hasLed", False)
        has_buzzer = bin_item.get("hasBuzzer", False)

        servo_pin = bin_item.get("servoPin")
        if has_servo and servo_pin is not None:
            pi.set_mode(servo_pin, pigpio.OUTPUT)
            set_servo_angle(pi, servo_pin, closed_angle, move_delay)
            pi.set_servo_pulsewidth(servo_pin, 0)

        sensor = bin_item.get("sensor")
        if has_sensor and sensor is not None:
            pi.set_mode(sensor["triggerPin"], pigpio.OUTPUT)
            pi.set_mode(sensor["echoPin"], pigpio.INPUT)
            pi.write(sensor["triggerPin"], 0)

        led_pin = bin_item.get("ledPin")
        if has_led and led_pin is not None:
            pi.set_mode(led_pin, pigpio.OUTPUT)
            set_led_output(pi, led_pin, False)

        buzzer_pin = bin_item.get("buzzerPin")
        if has_buzzer and buzzer_pin is not None:
            pi.set_mode(buzzer_pin, pigpio.OUTPUT)
            set_buzzer_output(pi, buzzer_pin, False)


def cleanup(pi, bins):
    for bin_item in bins:
        has_servo = bin_item.get("hasServo", False)
        has_led = bin_item.get("hasLed", False)
        has_buzzer = bin_item.get("hasBuzzer", False)

        if has_servo:
            pi.set_servo_pulsewidth(bin_item["servoPin"], 0)

        led_pin = bin_item.get("ledPin")
        if has_led and led_pin is not None:
            set_led_output(pi, led_pin, False)

        buzzer_pin = bin_item.get("buzzerPin")
        if has_buzzer and buzzer_pin is not None:
            set_buzzer_output(pi, buzzer_pin, False)

    pi.stop()
