import pyautogui
import keyboard

def simulate_copy():
    pyautogui.hotkey('ctrl', 'c')

def simulate_paste():
    pyautogui.hotkey('ctrl', 'v')

def simulate_select_all():
    pyautogui.hotkey('ctrl', 'a')

def press_enter():
    keyboard.press_and_release('enter')