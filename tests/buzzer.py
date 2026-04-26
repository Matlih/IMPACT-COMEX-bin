import time

import pigpio  # type: ignore[import-not-found]

BUZZER_PIN = 27
BEEP_SECONDS = 0.2
PAUSE_SECONDS = 0.2


def set_buzzer_output(pi, is_on):
    value = 1 if is_on else 0
    pi.write(BUZZER_PIN, value)


pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    raise SystemExit(1)

pi.set_mode(BUZZER_PIN, pigpio.OUTPUT)
set_buzzer_output(pi, False)

print("Active buzzer test")
print("Commands: on, off, beep, q")

try:
    while True:
        command = input("> ").strip().lower()

        if command == "q":
            break

        if command == "on":
            set_buzzer_output(pi, True)
            print("Buzzer ON")
            continue

        if command == "off":
            set_buzzer_output(pi, False)
            print("Buzzer OFF")
            continue

        if command == "beep":
            for _ in range(5):
                set_buzzer_output(pi, True)
                time.sleep(BEEP_SECONDS)
                set_buzzer_output(pi, False)
                time.sleep(PAUSE_SECONDS)
            print("Beep test complete")
            continue

        print("Unknown command. Use: on, off, beep, q")
except KeyboardInterrupt:
    print("\nTest interrupted.")
finally:
    set_buzzer_output(pi, False)
    pi.stop()
    print("GPIO cleaned up.")
