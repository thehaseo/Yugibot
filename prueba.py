from pyautogui import scroll, moveTo, drag
from time import sleep
from imagesearch import imagesearch

sleep(5)
coord = imagesearch("images/gx_world_icon.jpg")
moveTo(coord)
drag(0, -50, 0.5, button="left")