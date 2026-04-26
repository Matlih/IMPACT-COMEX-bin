def set_led_output(pi, led_pin, is_on):
    value = 1 if is_on else 0
    pi.write(led_pin, value)
