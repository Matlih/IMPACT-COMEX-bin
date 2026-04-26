def set_buzzer_output(pi, buzzer_pin, is_on):
    value = 1 if is_on else 0
    pi.write(buzzer_pin, value)
