from src.hardware.sensor import measure_distance_cm
from src.hardware.servo import set_servo_angle
from src.hardware.led import set_led_output
from src.hardware.buzzer import set_buzzer_output

def init(bins):
    result = {}
    for bin_item in bins:
        result[bin_item["name"]] = {
            "is_open": False,
            "blocked_since": None,
            "is_full": False,
            "sensor_paused_until": 0.0,
            "close_due_at": None,
        }
    return result

def check_full(context):
    pi = context["pi"]
    bin_item = context["bin_item"]
    state = context["state"]
    now = context["now"]

    has_sensor = bin_item.get("hasSensor", True)
    has_led = bin_item.get("hasLed", True)
    has_buzzer = bin_item.get("hasBuzzer", True)
    sensor = bin_item.get("sensor")
    if pi is None or not has_sensor or sensor is None:
        return

    if state["is_open"] or now < state["sensor_paused_until"]:
        state["blocked_since"] = None
        return

    distance = measure_distance_cm(
        pi,
        sensor["triggerPin"],
        sensor["echoPin"],
        sensor.get("triggerPulseMicros", 10),
        sensor.get("timeoutSeconds", 0.03),
    )

    is_blocked = distance is not None and distance <= sensor["blockedDistanceCm"]
    block_seconds = sensor["blockSeconds"]

    if is_blocked:
        if state["blocked_since"] is None:
            state["blocked_since"] = now

        blocked_time = now - state["blocked_since"]
        if blocked_time >= block_seconds and not state["is_full"]:
            state["is_full"] = True
            print(f"{bin_item['name']} is FULL (sensor blocked for {block_seconds} seconds)")

            led_pin = bin_item.get("ledPin")
            if has_led and led_pin is not None:
                set_led_output(pi, led_pin, True)

            buzzer_pin = bin_item.get("buzzerPin")
            if has_buzzer and buzzer_pin is not None:
                set_buzzer_output(pi, buzzer_pin, True)
    else:
        state["blocked_since"] = None

        if state["is_full"]:
            state["is_full"] = False
            print(f"{bin_item['name']} is no longer full")

        led_pin = bin_item.get("ledPin")
        if has_led and led_pin is not None:
            set_led_output(pi, led_pin, False)

        buzzer_pin = bin_item.get("buzzerPin")
        if has_buzzer and buzzer_pin is not None:
            set_buzzer_output(pi, buzzer_pin, False)


def check_lid(context):
    pi = context["pi"]
    bin_item = context["bin_item"]
    state = context["state"]
    detected_labels = context["detected_labels"]
    open_angle = context["open_angle"]
    closed_angle = context["closed_angle"]
    move_delay = context["move_delay"]
    close_delay = context["close_delay"]
    now = context["now"]

    bin_name = bin_item["name"]
    has_servo = bin_item.get("hasServo", True)
    servo_pin = bin_item["servoPin"]
    required_labels = bin_item["labels"]

    has_required_label = any(label in detected_labels for label in required_labels)

    if state["is_full"] and state["is_open"]:
        print(f"{bin_name} full -> closing lid")
        if pi is not None and has_servo:
            set_servo_angle(pi, servo_pin, closed_angle, move_delay)
            pi.set_servo_pulsewidth(servo_pin, 0)
        state["is_open"] = False
        state["close_due_at"] = None
        state["sensor_paused_until"] = now + move_delay

    if has_required_label and not state["is_open"] and not state["is_full"]:
        print(f"Detected target for {bin_name} -> opening lid")
        if pi is not None and has_servo:
            set_servo_angle(pi, servo_pin, open_angle, move_delay)
            state["is_open"] = True
            state["sensor_paused_until"] = now + move_delay
        state["close_due_at"] = None

    if not has_required_label and state["is_open"]:
        close_due_at = state.get("close_due_at")
        if close_due_at is None:
            close_due_at = now + max(0.0, close_delay)
            state["close_due_at"] = close_due_at
            print(f"No target for {bin_name} -> waiting {max(0.0, close_delay):.2f}s before closing")

        if now < close_due_at:
            return

        print(f"No target for {bin_name} -> closing lid")
        if pi is not None and has_servo:
            set_servo_angle(pi, servo_pin, closed_angle, move_delay)
            pi.set_servo_pulsewidth(servo_pin, 0)
        state["is_open"] = False
        state["close_due_at"] = None
        state["sensor_paused_until"] = now + move_delay
