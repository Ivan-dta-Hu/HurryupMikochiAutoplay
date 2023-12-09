from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import pyautogui
import time
import csv

def on_press(key):
    global lane
    if key == Key.up and lane != 0:
        lane = 0
        events.append((time.time()-start,'up','press'))
    if key == Key.down and lane != 2:
        lane = 2
        events.append((time.time()-start,'down','press'))
    if key == Key.space:
        events.append((time.time()-start,'space','press'))
def on_release(key):
    global lane
    if key == Key.up:
        lane = 1
        events.append((time.time()-start,'up','release'))
    if key == Key.down:
        lane = 1
        events.append((time.time()-start,'down','release'))
    if key == Key.shift_l:
        events.append((time.time()-start,'checkpoint','null'))
    if key == Key.esc:
        keyListener.stop()

mouseController = mouse.Controller()
mouseController.position=(856,742)
mouseController.click(Button.left, 1)

lane=1
events = []
start=time.time()
while time.time()-start<5 and not pyautogui.pixelMatchesColor(958, 570, (255, 255, 255)):
    pass
start=time.time()
mouseController.position=(1062,736)#Back to menu

keyboardController = keyboard.Controller()
with open('recorded_events.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)        
    for row in csv_reader:
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
mouseController.position=(1919,540)

keyListener = keyboard.Listener(on_press=on_press,on_release=on_release)
keyListener.start()
keyListener.join()

count=len(events)
index=-1
for i in range(count-1,-1,-1):
    if events[i][1]=='checkpoint':
        index=i
        break
events=events[:index+1]
with open('recorded_events.csv', 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(events)