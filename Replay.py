from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import pyautogui
import time
import csv

stop=False
def stopReplay(key):
    global stop
    if key == Key.esc:
        stop=True
        keyListener.stop()
        
keyListener = keyboard.Listener(on_release=stopReplay)
keyListener.start()
mouseController = mouse.Controller()
keyboardController = keyboard.Controller()

while True:
    mouseController.position=(856,742)
    mouseController.click(Button.left, 1)
    start=time.time()
    while time.time()-start<5 and not pyautogui.pixelMatchesColor(958, 570, (255, 255, 255)):
        pass
    start=time.time()
    mouseController.position=(1062,736)# Back to menu
    with open('recorded_events.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if stop:
                break
            timestamp, btn, action = row
            interval = float(timestamp) + start - time.time()
            if interval>0:
                time.sleep(interval)
            if btn == 'up':
                if action == 'press':
                    keyboardController.press(Key.up)
                if action == 'release':
                    keyboardController.release(Key.up)
            if btn == 'down':
                if action == 'press':
                    keyboardController.press(Key.down)
                if action == 'release':
                    keyboardController.release(Key.down)
            if btn == 'space':
                if action == 'press':
                    keyboardController.press(Key.space)
                    keyboardController.release(Key.space)
        start=time.time()
    if stop:
        break
    while not pyautogui.pixelMatchesColor(805,187,(141,122,124)):
        pass
    time.sleep(1)
    # keyboardController.press(Key.esc)
    # keyboardController.release(Key.esc)
keyListener.join()
