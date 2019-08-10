import threading
from tkinter import Button
import numpy as np
from time import sleep

from imagesearch import click_image, imagesearch





class DetectarPantalla(threading.Thread):
        ''' 
        Clase que crea un thread que busca imágenes dadas en una lista 
        continuamente hasta encontrarse y clickea la imagen en la pantalla.

        '''
        def __init__(self):
                super().__init__()
                self.SECONDS = 0.3
                self.detener = threading.Event()
                self.daemon = True
                self.pos = None
                self.gate = False
                self.shop = False
                self.pvp_arena = False
                self.duel_studio = False
                self.world_checked = False
                self.dm_world = False
                self.gx_world = False
                self._5ds_world = False
                self.image_list = ["images/Button_next.jpg", "images/Gate.jpg", 
                    "images/go_back_button.jpg", "images/initiateLink.jpg", 
                    "images/pop_up_ok.jpg", "images/Suspended_duel.jpg",
                    "images/close_button.jpg", "images/duel_studio.jpg",
                    "images/avanzar_escena.jpg", "images/pvp_arena.jpg",
                    "images/shop.jpg",
                    ]
                self.npcdm_list = ["andrew.jpg", "npc/mickey1.jpg",
                    "npc/bella1.jpg", "npc/bella2.jpg", "npc/bella3.jpg", 
                    "npc/christine1.jpg", "npc/emma1.jpg", "npc/hailey1.jpg", 
                    "npc/jess1.jpg", "npc/joey1.jpg", "npc/vagabond1.jpg",
                    "npc/vagabond2.jpg", "npc/vagabond3.jpg"
                    ]
                self.npcgx_list = ["npc/alssa1.jpg", "npc/bella1.jpg", "npc/bella2.jpg", 
                    "npc/bella3.jpg", "npc/emma1.jpg", "npc/jaden_own.jpg", 
                    "npc/kylie1.jpg", "npc/logan1.jpg", "npc/madison1.jpg",
                    "npc/vagabond1", "npc/vagabond2.jpg", "npc/vagabond3.jpg",
                    "npc/vagabond4"
                    ]
                self.npc5ds_list = ["npc/bella1.jpg", "npc/bella2.jpg", "npc/bella3.jpg", 
                    "npc/chloe1.jpg", "npc/emma1.jpg", "npc/erika1.jpg", 
                    "npc/liam1.jpg", "npc/vagabond1", "npc/vagabond2.jpg", 
                    "npc/vagabond3.jpg", "npc/vagabond4", "npc/yusei_own1.jpg", 
                    "npc/wild_dan1.jpg"
                    ]
        
        # ejecuta un loop infinito buscando las imágenes de la pantalla
        def run(self):
                while True:
                        
                        for index, imagen in enumerate(self.image_list):
                                if self.detener.is_set():
                                        return 

                                self.pos = imagesearch(imagen)
                                if self.pos[0] == -1:
                                        print(imagen+" not found, waiting")
                                        sleep(self.SECONDS)
                                else:  # Al encontrar una imagen de la lista de imagenes ejecuta una accion
                                        print(self.pos[0])
                                        if index in {0,2,3,4,5,6,8}:
                                                click_image(imagen, self.pos, "left", self.SECONDS)
                                        elif index == 1:
                                                print("Gate detected")
                                                self.gate = True
                                                self.shop = False
                                                self.pvp_arena =  False
                                                self.duel_studio = False
                                                if not self.world_checked:
                                                        self.check_world()


        def check_world(self):
                world_check_button = list(map(imagesearch, ("images/check_world_button.jpg", 
                                "images/check_world_button2.jpg", "images/check_world_button3.jpg")))
                for cordx, cordy in world_check_button:
                        if not -1 in {cordx,cordy}:
                                x= cordx
                                y=cordy
                coord = [x,y]
                click_image("images/check_world_button.jpg", coord, "left", 0.1)
                if imagesearch("images/gx_world_check.jpg") != -1 and imagesearch("images/5ds_world_check.jpg") != -1:    
                        self.gx_world = False
                        self._5ds_world = False
                        self.dm_world = True
                        self.world_checked = True
                        print("Gx world detected")
                        print("5ds world detected")

        def npc_search():
                print("hola")
                sleep(3)


        def stop(self):
                self.detener.set()

