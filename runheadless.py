from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay
from PIL import Image, ImageGrab, ImageFilter
import random
import threading
import time
import keyboard
import mouse
import sys

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import os

# rev.1 users set port=0
with open("/tmp/.oledlock", "w") as file:
    file.write(str(os.getpid()))
    file.close()
    os.chmod("/tmp/.oledlock", 0o777) 

serial = i2c(port=1, address=0x3C)

device = ssd1306(serial, height=32)

def on_keyboard_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        pyautogui.keyDown(event.name)

    elif event.event_type == keyboard.KEY_UP:
        pyautogui.keyUp(event.name)

def on_mouse_event(event):
    print(event)

print(sys.argv[1:])

def process():
    with EasyProcess(sys.argv[1:]) as proc:
        proc.wait()

def capture():
    while 1:
        img = ImageGrab.grab(xdisplay=":99")
        img = img.resize((128, 32), Image.Resampling.BICUBIC)
        with canvas(device, dither=True) as draw:
            flipped_im = img.transpose(Image.FLIP_LEFT_RIGHT)
            flipped_im = flipped_im.convert("L")
            flipped_im = flipped_im.filter(ImageFilter.FIND_EDGES)
            draw._image.paste(flipped_im)
        time.sleep(0.033)

disp = SmartDisplay(backend="xvfb", use_xauth=True, extra_args=[":99"], size=(320, 200))
disp.start()

keyboard.hook(on_keyboard_action)
#mouse.hook(on_mouse_event) TODO mouse support

import pyautogui
threading.Thread(target=process).start()
threading.Thread(target=capture).start()