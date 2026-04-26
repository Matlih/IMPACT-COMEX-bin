import time

def measure_distance_cm(pi, trigger_pin, echo_pin, trigger_pulse_micros, timeout_seconds):
    pi.gpio_trigger(trigger_pin, trigger_pulse_micros, 1)

    start_wait = time.monotonic()
    while pi.read(echo_pin) == 0:
        if time.monotonic() - start_wait > timeout_seconds:
            return None

    pulse_start = time.monotonic()
    while pi.read(echo_pin) == 1:
        if time.monotonic() - pulse_start > timeout_seconds:
            return None

    pulse_end = time.monotonic()
    pulse_duration = pulse_end - pulse_start

    return (pulse_duration * 34300) / 2
