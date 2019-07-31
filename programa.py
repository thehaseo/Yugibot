from imagesearch import *
import threading
from tkinter import Button
from sys import exit
import numpy as np

#Cambia el boton start en la interfaz grafica a stop y al mismo tiempo comienza el programa
#DetectScreenImage
def change(boton):
        Boton = Button.config(boton, text="Stop",command=exit)
        detect = threading.Thread(target = DetectScreenImage)
        detect.start()

#Detecta la imagen en pantalla 

def DetectScreenImage():
        Image_list = ["images\initiateLink.jpg","images\Suspended_duel.jpg"]
        print("Detectando pantalla...")
        screen = imagesearch_loop_list(Image_list,1)
        print(screen)
        



