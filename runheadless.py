from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay
from PIL import Image, ImageGrab
import random
import threading
import time
import keyboard
import mouse
import sys

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image

# rev.1 users set port=0
serial = i2c(port=1, address=0x3C)

device = ssd1306(serial, height=32)

def on_keyboard_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        pyautogui.keyDown(event.name)

    elif event.event_type == keyboard.KEY_UP:
        pyautogui.keyUp(event.name)

def on_mouse_event(event):
    print(event)

def process():
    with EasyProcess([sys.argv[1:]]) as proc:
        proc.wait()

def capture():
    while 1:
        img = ImageGrab.grab(xdisplay=":99")
        img = img.resize((128, 32), Image.Resampling.BICUBIC)
        with canvas(device) as draw:
            flipped_im = img.transpose(Image.FLIP_LEFT_RIGHT)
            draw.bitmap((0, 0), flipped_im, fill="white")

disp = SmartDisplay(backend="xvfb", use_xauth=True, extra_args=[":99"], size=(320, 200))
disp.start()

keyboard.hook(on_keyboard_action)
#mouse.hook(on_mouse_event) TODO mouse support

import pyautogui
threading.Thread(target=process).start()
threading.Thread(target=capture).start()