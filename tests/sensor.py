import time

import pigpio # type: ignore[import-not-found]

TRIGGER_PIN = 23
ECHO_PIN = 24
POLL_INTERVAL_SECONDS = 0.25
TIMEOUT_SECONDS = 0.03


def measure_distance_cm(pi, trigger_pin, echo_pin, timeout_seconds=TIMEOUT_SECONDS):
    pi.gpio_trigger(trigger_pin, 10, 1)

    start_wait = time.time()
    while pi.read(echo_pin) == 0:
        if time.time() - start_wait > timeout_seconds:
            return None

    pulse_start = time.time()
    while pi.read(echo_pin) == 1:
        if time.time() - pulse_start > timeout_seconds:
            return None

    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    return (pulse_duration * 34300) / 2


pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    raise SystemExit(1)

pi.set_mode(TRIGGER_PIN, pigpio.OUTPUT)
pi.set_mode(ECHO_PIN, pigpio.INPUT)
pi.write(TRIGGER_PIN, 0)

time.sleep(0.1)
print("Ultrasonic sensor test started. Press Ctrl+C to stop.")

try:
    while True:
        distance_cm = measure_distance_cm(pi, TRIGGER_PIN, ECHO_PIN)
        if distance_cm is None:
            print("Distance: timeout")
        else:
            print(f"Distance: {distance_cm:.1f} cm")

        time.sleep(POLL_INTERVAL_SECONDS)
except KeyboardInterrupt:
    print("\nTest interrupted.")
finally:
    pi.write(TRIGGER_PIN, 0)
    pi.stop()
    print("GPIO cleaned up.")
