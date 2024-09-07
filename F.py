import RPi.GPIO as GPIO
import blynklib
import time

BLYNK_AUTH = ""

TRIG_PINS = [18, 23, 24, 25]
ECHO_PINS = [24, 25, 4, 5]
SERVO_PINS = [12, 13, 18, 19]
BUTTON_PIN = 17

DEPTH_WIDGETS = [V1, V0, V3, V4]
#SLIDER_WIDGETS = [W1, W2, W3, W4]
#BUTTON_WIDGET = B1

blynk = blynklib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BCM)
for pin in TRIG_PINS + ECHO_PINS:
    GPIO.setup(pin, GPIO.OUT)
for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.PWM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm_channels = [
    GPIO.PWM(pin, 50) for pin in SERVO_PINS
]
for channel in pwm_channels:
    channel.start(0)

def read_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    pulse_start = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return distance

def update_blynk(sensor_id, distance):
    blynk.virtual_write(sensor_id, distance)

def predict():
    return 1

def control_servo(servo_pin, angle):
    duty_cycle = (0.05 * angle) + 2.5
    pwm_channels[SERVO_PINS.index(servo_pin)].ChangeDutyCycle(duty_cycle)

def button_pressed(pin):
    predicted_value = predict()
    for i, servo_pin in enumerate(SERVO_PINS):
        if i == predicted_value:
            control_servo(servo_pin, 180)
            time.sleep(2)
            control_servo(servo_pin, 0)
        else:
            control_servo(servo_pin, 0)


#@blynk.handle_event(SLIDER_WIDGETS)
#def slider_updated(pin, value):
#    control_servo(SERVO_PINS[SLIDER_WIDGETS.index(pin)], value)

@blynk.run
def main_loop():
    for i, pin in enumerate(TRIG_PINS + ECHO_PINS):
        if i % 2 == 0:
            distance = read_distance(pin, pin + 1)
            update_blynk(DEPTH_WIDGETS[i // 2], distance)

    time.sleep(0.1)

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed)

try:
    main_loop()
except KeyboardInterrupt:
    GPIO.cleanup()
    for channel in pwm_channels:
        channel.stop()
    blynk.stop()

