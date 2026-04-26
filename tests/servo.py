import pigpio # type: ignore[import-not-found]
import time

pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

SERVO_PIN = 17
pi.set_mode(SERVO_PIN, pigpio.OUTPUT)

def set_angle(pin, target_angle):
    if target_angle < 0 or target_angle > 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    
    pulse_width = 500 + (target_angle * (2000 / 180))
    pi.set_servo_pulsewidth(pin, pulse_width)
    time.sleep(0.5)

try:
    while True:
        try:
            user_input = input("Enter angle (0-180) or 'q' to quit: ")
            if user_input.lower() == 'q':
                break
            
            angle = float(user_input)
            if angle < 0 or angle > 180:
                print("Angle must be between 0 and 180 degrees")
                continue
            
            set_angle(SERVO_PIN, angle)
            print(f"Servo moved to {angle} degrees")
        except ValueError:
            print("Invalid input. Please enter a number between 0-180 or 'q' to quit")
            continue
except KeyboardInterrupt:
    print("\nTest interrupted.")
finally:
    pi.set_servo_pulsewidth(SERVO_PIN, 0) 
    pi.stop()
    print("GPIO cleaned up.")