import threading
from tkinter import Button
import numpy as np
from time import sleep
from imagesearch import click_image, imagesearch

Gate = True


''' 
Clase que crea un thread que busca imágenes dadas en una lista 
continuamente hasta encontrarse y clickea la imagen en la pantalla.
'''
class DetectarPantalla(threading.Thread):
        
        def __init__(self):
                super().__init__()
                self.SECONDS = 0.5
                self.detener = threading.Event()
                self.daemon = True
                self.pos = None
                self.image_list = [
                        "images/initiateLink.jpg",
                        "images/Suspended_duel.jpg",
                        "images/pop_up_ok.jpg", 
                        "images/Button_next.jpg",
                        "images/go_back_button.jpg",
                        "images/Gate.jpg"
                        ]
        
        def run(self):
                while True:
                        for index, imagen in enumerate(self.image_list):
                                if self.detener.is_set():
                                        return None

                                self.pos = imagesearch(imagen)
                                if self.pos[0] == -1:
                                        print(imagen+" not found, waiting")
                                        sleep(self.SECONDS)
                                else:
                                        print(self.pos[0])
                                        if index == 0:
                                                click_image(imagen, self.pos, "left", self.SECONDS)
                                        elif index == 2:
                                                click_image(imagen,self.pos,"left", self.SECONDS)
                                        elif index == 4:
                                                click_image(imagen,self.pos,"left", self.SECONDS)
                                        elif index == 5:



        def stop(self):
                self.detener.set()

