
import board
import digitalio
import busio
import time


import adafruit_ssd1306


from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros


keyboard = KMKKeyboard()


macros = Macros()
keyboard.modules.append(macros)


PINS = [board.GP1, board.GP3]  


keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)


keyboard.keymap = [
    [KC.TAB, KC.ENTER]
]



encoder_a = digitalio.DigitalInOut(board.GP4)
encoder_a.direction = digitalio.Direction.INPUT
encoder_a.pull = digitalio.Pull.UP

encoder_b = digitalio.DigitalInOut(board.GP2)
encoder_b.direction = digitalio.Direction.INPUT
encoder_b.pull = digitalio.Pull.UP


led = digitalio.DigitalInOut(board.GP26)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.GP7, board.GP6)  
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


last_a = encoder_a.value
last_b = encoder_b.value
direction = "None"

def update_oled(text):
    oled.fill(0)
    oled.text(text, 0, 0, 1)
    oled.show()


update_oled("Skibidi")
while True:
    keyboard.go()  
    
    
    a = encoder_a.value
    b = encoder_b.value
    if a != last_a:
        if b != a:
           
            direction = "Right"
            keyboard.tap_key(KC.RIGHT)
        else:
           
            direction = "Left"
            keyboard.tap_key(KC.LEFT)
        update_oled(direction)
    last_a = a
    last_b = b
    
    led.value = any(keyboard._is_pressed)
    time.sleep(0.01)