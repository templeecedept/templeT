# import necessary modules
from neopixel2 import Neopixel
import utime
import random
import machine
from machine import Pin
import micropython
import time

# initialize variables
counter = 0
mode = 0

# set up button pin for interrupt
buttonPin = Pin(15, Pin.IN, Pin.PULL_DOWN)
def alert(pin):
    global mode
    mode += 1
    print("mode = ",mode)
    print("Inside the interrupt handler function")
    if mode > 5:
        mode = 0

# attach interrupt handler function to button pin
buttonPin.irq(trigger = Pin.IRQ_RISING , handler = alert)

# set up neopixel strip
numpix = 35
strip = Neopixel(numpix, 0, 18, "GRB")
strip.brightness(20)


# set up color values
red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
blank = (0,0,0)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

# define functions for different modes

# Fills the strip with each color in the colors_rgb list
def color_change(mode_num, color, speed):
    for i in range(len(colors_rgb)):
        strip.fill(colors_rgb[i])
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break
        
# Displays a marquee effect with the specified color
def marquee(mode_num, color, speed):
    for x in range(33):
        utime.sleep(speed)
        strip.set_pixel(x+1, color)
        strip.show()
        if mode != mode_num:
             break
        utime.sleep(speed)
        strip.set_pixel(x, color)
        strip.show()
        if mode != mode_num:
            break
        utime.sleep(speed)
        strip.set_pixel(x+2, color)
        strip.show()
        if mode != mode_num:
            break
        utime.sleep(speed)
        strip.set_pixel(x, blank)
        strip.show()
        if mode != mode_num:
             break
        utime.sleep(speed)
        strip.set_pixel(x+1, blank)
        strip.show()
        if mode != mode_num:
            break
        utime.sleep(speed)
        strip.set_pixel(x+2, blank)
        strip.show()
        if mode != mode_num:
            break
 
    for x in reversed(range(33)):       
        strip.set_pixel(x+1, color)
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break
        strip.set_pixel(x, color)
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break
        strip.set_pixel(x+2, color)
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break
        strip.set_pixel(x, blank)
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break
        strip.set_pixel(x+1, blank)
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break
        strip.set_pixel(x+2, blank)
        utime.sleep(speed)
        strip.show()
        if mode != mode_num:
            break

# Define a function for randomly changing LED colors
def random_color_change(mode_num, color, speed):
    while True:
        strip.set_pixel(random.randint(0, numpix-1), color[random.randint(0, len(colors_rgb)-1)])
        strip.show()
        utime.sleep(speed)
        if mode != 2:
            break

# Define a function for creating a gradient effect
def gradient(mode_num, color, speed):
    if color is None:
        return

    brightness = 0
    increment = 5
    while True:
        if brightness >= 255:
            increment = -5
        elif brightness <= 0:
            increment = 5
        
        # Calculate color based on current brightness level
        current_color = tuple(int(c * (brightness / 255)) for c in color)
        strip.fill(current_color)
        strip.show()
        
        # Increment brightness level and wait
        brightness += increment
        utime.sleep(speed)
        
        # Check if mode has changed
        if mode != mode_num:
            break

# Define a function for creating a color wheel effect
def color_wheel(mode_num, speed):
    # Set up color wheel
    colors = []
    for i in range(256):
        if i < 85:
            colors.append((255 - i * 3, i * 3, 0))
        elif i < 170:
            colors.append((0, 255 - (i - 85) * 3, (i - 85) * 3))
        else:
            colors.append(((i - 170) * 3, 0, 255 - (i - 170) * 3))
    
    # Loop through color wheel
    while True:
        for color in colors:
            strip.fill(color)
            strip.show()
            utime.sleep(speed)
            if mode != mode_num:
                break
        if mode != mode_num:
            break

# Define a function for turning off all LEDs
def clear(mode_num):
    while True:
        strip.clear()
        strip.show()
        if mode != mode_num:
            break

# Main loop
while True:
    # Mode 0: change colors
    if mode == 0:
        color_change(mode_num=0, color=colors_rgb, speed=0.5)
    # Mode 1: marquee effect with red color
    elif mode == 1:   
        marquee(mode_num=1, color=red, speed=0.005)
    # Mode 2: random color change
    elif mode == 2:
        random_color_change(mode_num=2, color=colors_rgb, speed=0.01)

    # Mode 3: gradient effect with violet color
    elif mode == 3:
        gradient(mode_num=3, color=violet, speed=0.01)
    
    # Mode 4: color wheel effect
    elif mode == 4:
        color_wheel(mode_num=4, speed=0.01)
        
    # Mode 5: turn off all LEDs
    elif mode == 5:
        clear(mode_num=5)

    # Print current mode
    print("mode:",mode)
    # Wait for 1 second
    utime.sleep(1)
