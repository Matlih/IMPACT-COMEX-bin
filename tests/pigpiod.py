import pigpio # type: ignore[import-not-found]

pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    raise SystemExit(1)

try:
    revision = pi.get_hardware_revision()
    print("Connected to pigpio daemon")
    print(f"Hardware revision: {revision}")
finally:
    pi.stop()
    print("pigpio connection closed")
