from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay
from PIL import Image, ImageGrab
import random
import threading
import time
import keyboard
import mouse

def on_keyboard_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        pyautogui.keyDown(event.name)

    elif event.event_type == keyboard.KEY_UP:
        pyautogui.keyUp(event.name)

def on_mouse_event(event):
    print(event)

def process():
    with EasyProcess(["chocolate-doom", "-iwad", "/home/pigu/.config/gzdoom/DOOM2.WAD", "-1"]) as proc:
        proc.wait()

def capture():
    while 1:
        img = ImageGrab.grab(xdisplay=":99")
        img = img.resize((128, 32), Image.Resampling.BICUBIC)
        img.save(f"balls.png")
        time.sleep(0.1)

disp = SmartDisplay(backend="xvfb", use_xauth=True, extra_args=[":99"], size=(320, 200))
disp.start()

keyboard.hook(on_keyboard_action)
#mouse.hook(on_mouse_event) TODO mouse support

import pyautogui
threading.Thread(target=process).start()
threading.Thread(target=capture).start()