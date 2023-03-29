# Do a pip install pyautogui/pynput/keyboard --user
import random
import pyautogui
import time
import keyboard
from pynput.keyboard import Key, Controller

pyautogui.FAILSAFE = False

# Instructions:
# 1. Enter time you wanna afk for in SECONDS
# 2. Click away your cursor to the interpreter before you run the script
# 3. Script moves the mouse up and down + randomly presses keys to simulate human activity
# 4. Press 'q' on your keyboard if you want to interrupt

# -------------------------------------------------------------------------
# Number of seconds to do this for:
# 60 seconds = 1 minute
# 3600 seconds = 1 hour
# 32400 seconds = 9 hours (9AM - 6PM)
SECONDS = 3600
KEYS = ['w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']

# Start position in top middle part of screen
pyautogui.moveTo(1000,0)

for i in range(0,SECONDS+1):
    # Creating a breaking mechanism -> Press Q button to break the script
    if keyboard.is_pressed('q'):
        print('Stopping Script...')
        print('Time Elapsed (In Seconds): ', i)
        break

    # Normal running of the script 
    else:
        keypress = random.choice(KEYS)

        # If cursor move to to Y-axis halfway of screen, restart at top middle part of screen. 
        # # Assumes screen resolution Y-axis is in multiples of 10 and divisible by 2
        if int(pyautogui.position()[1]) == int(pyautogui.size()[1]/2):
            pyautogui.moveTo(1000,0)
        
        # If the cursor is not at the center of the screen, reset to top middle of the screen
        elif pyautogui.position()[0] != 1000:
            pyautogui.moveTo(1000,0)

        # If Y-axis position is not a multiple of 10, then reset it to the top middle part of screen
        elif pyautogui.position()[0] %10 != 0:
            pyautogui.moveTo(1000,0)
        
        # Else every 1 seconds, move the cursor down 10 units in Y-axis
        else:
            pyautogui.move(0,10)
            keyboard.press(keypress)
            time.sleep(1)
            keyboard.release(keypress)
    
print('Script Ended')

# Remove all the alphabets pressed from interpreter
keyboard.press('esc')
keyboard.release('esc')



