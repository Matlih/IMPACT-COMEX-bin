import time

import pigpio # type: ignore[import-not-found]

LED_PIN = 25
BLINK_ON_SECONDS = 0.25
BLINK_OFF_SECONDS = 0.25


def set_led_output(pi, is_on):
    value = 1 if is_on else 0
    pi.write(LED_PIN, value)


pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    raise SystemExit(1)

pi.set_mode(LED_PIN, pigpio.OUTPUT)
set_led_output(pi, False)

print("LED output test")
print("Commands: on, off, blink, q")

try:
    while True:
        command = input("> ").strip().lower()

        if command == "q":
            break

        if command == "on":
            set_led_output(pi, True)
            print("LED output ON")
            continue

        if command == "off":
            set_led_output(pi, False)
            print("LED output OFF")
            continue

        if command == "blink":
            for _ in range(10):
                set_led_output(pi, True)
                time.sleep(BLINK_ON_SECONDS)
                set_led_output(pi, False)
                time.sleep(BLINK_OFF_SECONDS)
            print("Blink test complete")
            continue

        print("Unknown command. Use: on, off, blink, q")
except KeyboardInterrupt:
    print("\nTest interrupted.")
finally:
    set_led_output(pi, False)
    pi.stop()
    print("GPIO cleaned up.")
