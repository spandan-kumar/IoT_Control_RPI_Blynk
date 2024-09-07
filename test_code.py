import BlynkLib
import RPi.GPIO as GPIO
import time

BLYNK_AUTH_TOKEN = ''

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN)
GPIO.setup(23, GPIO.OUT)  
GPIO.setup(24, GPIO.IN)   

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

@blynk.VIRTUAL_WRITE(2)
def v2_write_handler(value):
    pass  # Handle virtual pin 2 writes if needed

def smesensor():
    ir = GPIO.input(7)
    print("IR Value:", ir)

    if ir == GPIO.HIGH:
        GPIO.output(23, GPIO.LOW)
        time.sleep(2)
        for i in range(10):
            blynk.virtual_write(2, 0)
            ultrasonic()
            time.sleep(0.2)
    else:
        GPIO.output(23, GPIO.HIGH)
        blynk.virtual_write(2, 0)
        ultrasonic()
        time.sleep(0.2)

def ultrasonic():
    GPIO.output(23, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(23, GPIO.LOW)
    duration = GPIO.pulse_in(24, GPIO.HIGH)
    distance = duration * 0.034 / 2
    bin_level = int(distance)
    blynk.virtual_write(0, distance)
    blynk.virtual_write(1, bin_level)

GPIO.add_event_detect(7, GPIO.BOTH, callback=smesensor, bouncetime=200)
blynk.run()

#gpt reference

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

ultrasonic_pins = [(18, 23), (24, 25), (12, 16), (20, 21)]

servo_pins = [17, 27, 22, 5]

button_pin = 6

for echo_pin, trigger_pin in ultrasonic_pins:
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(trigger_pin, GPIO.OUT)

servos = [GPIO.PWM(servo_pin, 50) for servo_pin in servo_pins]
for servo in servos:
    servo.start(0)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def move_servo(servo, angle):
    duty_cycle = angle / 18.0 + 2.5
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  
    servo.ChangeDutyCycle(0)  

def activate_servo(channel):
    print("Button pressed! Activating servos.")
    for servo in servos:
        move_servo(servo, 180) 
    time.sleep(3) 
    for servo in servos:
        move_servo(servo, 0) 
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=activate_servo, bouncetime=300)

try:
    while True:
        # Monitor ultrasonic sensors or perform other tasks as needed
        pass

except KeyboardInterrupt:
    print("Program terminated by user.")
    for servo in servos:
        servo.stop()
    GPIO.cleanup()

finally:
    for servo in servos:
        servo.stop()
    GPIO.cleanup()



import RPi.GPIO as GPIO
import blynklib
import time


BLYNK_AUTH = "YOUR_BLYNK_AUTH_TOKEN"


TRIG_PINS = [18, 23, 24, 25]
ECHO_PINS = [24, 25, 4, 5]
SERVO_PINS = [12, 13, 18, 19]
BUTTON_PIN = 17


DEPTH_WIDGETS = [V1, V2, V3, V4]
SLIDER_WIDGETS = [W1, W2, W3, W4]
BUTTON_WIDGET = B1


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

@blynk.handle_event(SLIDER_WIDGETS)
def slider_updated(pin, value):
    control_servo(SERVO_PINS[SLIDER_WIDGETS.index(pin)], value)

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

