import threading
from tkinter import ttk
import numpy as np
from time import sleep



from imagesearch import click_image, imagesearch, imagesearch_numLoop, imagesearch_loop





class DetectarPantalla(threading.Thread):
        ''' 
        Clase que crea un thread que busca imágenes dadas en una lista 
        continuamente hasta encontrarse y clickea la imagen en la pantalla.

        '''
        def __init__(self, Checkbutton):
                super().__init__()
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
                self.npc_search_checkbox = Checkbutton
                self.image_list = ["images/Button_next.jpg", "images/Gate.jpg", 
                    "images/go_back_button.jpg", "images/initiateLink.jpg", 
                    "images/pop_up_ok.jpg", "images/Suspended_duel.jpg",
                    "images/close_button.jpg", "images/duel_studio.jpg",
                    "images/avanzar_escena.jpg", "images/pvp_arena.jpg",
                    "images/shop.jpg", "images/character_text.jpg", "images/level_up.jpg"
                    ]
                self.npcdm_list = ["npc/andrew1.jpg", "npc/andrew2.jpg",  "npc/bella1.jpg", 
                    "npc/bella2.jpg", "npc/bella3.jpg", "npc/christine1.jpg", 
                    "npc/christine2.jpg", "npc/christine3.jpg", "npc/daniel1.jpg",
                    "npc/david1.jpg", "npc/emma1.jpg", "npc/espa_roba1.jpg", 
                    "npc/espa_roba2.jpg", "npc/hailey1.jpg", "npc/hailey2.jpg", 
                    "npc/jess1.jpg", "npc/jess2.jpg", "npc/joey1.jpg", 
                    "npc/josh1.jpg", "npc/mickey1.jpg", "npc/meg1.jpg"
                    ]
                self.npcgx_list = ["npc/alyssa1.jpg", "npc/bella1.jpg", "npc/bella2.jpg", 
                    "npc/bella3.jpg", "npc/emma1.jpg", "npc/jaden_own.jpg", 
                    "npc/kylie1.jpg", "npc/logan1.jpg", "npc/madison1.jpg",
                    ]
                self.npc5ds_list = ["npc/bella1.jpg", "npc/bella2.jpg", "npc/bella3.jpg", 
                    "npc/chloe1.jpg", "npc/emma1.jpg", "npc/erika1.jpg", 
                    "npc/liam1.jpg", "npc/yusei_own1.jpg", 
                    "npc/wild_dan1.jpg",
                    ]
        
        
        def run(self):
                # ejecuta un loop infinito buscando las imágenes de la pantalla
                while True:
                        
                        for index, imagen in enumerate(self.image_list):
                                if self.detener.is_set():
                                        return 

                                self.pos = imagesearch(imagen)
                                if self.pos[0] == -1:
                                        print(imagen+" not found, waiting")
                                        sleep(0.1)
                                else:   # Al encontrar una imagen de la lista de 
                                        # que no sean algunas de las 4 pantallas principales
                                        # clickea sobre ellas
                                        print(self.pos[0])
                                        while index == 12:
                                                if self.detener.is_set():
                                                        return 
                                                if imagesearch(imagen) == [-1,-1]:
                                                        break
                                                else:
                                                        click_image(imagen, imagesearch(imagen), "left", 0.2)
                                                        sleep(1)
                                        if index in {0,2,3,4,5,6,8,11,12}:
                                                click_image(imagen, self.pos, "left", 0.2)
                                        elif index == 1:
                                                print("Gate detected")
                                                self.gate = True
                                                self.shop = False
                                                self.pvp_arena =  False
                                                self.duel_studio = False
                                                # checkear el mundo actual si no se ha hecho
                                                if not self.world_checked: 
                                                        checkear = threading.Thread(target=self.check_world,
                                                                daemon=True)
                                                        checkear.start()
                                                        checkear.join()
                                                # Si el botón de buscar npc está marcado crea un nuevo hilo
                                                # para hacer la busqueda de npc y haciendo que la busqueda
                                                # principal de la pantalla espere a que la busqueda de npc
                                                # termine
                                                if self.npc_search_checkbox.state() == ('selected',):
                                                        if self.dm_world:
                                                                search_npc = threading.Thread(target=self.npc_search(self.npcdm_list), daemon=True)
                                                                search_npc.start()
                                                                search_npc.join()
                                                        elif self.gx_world:
                                                                search_npc = threading.Thread(target=self.npc_search(self.npcgx_list), daemon=True)
                                                                search_npc.start()
                                                                search_npc.join()
                                                                



        def check_world(self):
                # Busca el botón de cambiar mundos y verifica en que mundo está
                # (cambiando la variable a True) dependiendo de cuales mundos aparezcan 
                # en las imágenes una vez presionado el botón
                coord = None
                world_check_button = list(map(imagesearch, ("images/check_world_button.jpg", 
                                "images/check_world_button2.jpg", "images/check_world_button3.jpg",
                                "images/check_world_button4.jpg", "images/check_world_button5.jpg")))
                for cordx, cordy in world_check_button:
                        if not -1 in {cordx,cordy}:
                                x = cordx
                                y = cordy
                                coord = [x,y]
                click_image("images/check_world_button.jpg", coord, "left", 0.1)
                if imagesearch("images/gx_world_check.jpg") != -1 and imagesearch("images/5ds_world_check.jpg") != -1:    
                        self.gx_world = False
                        self._5ds_world = False
                        self.dm_world = True
                        self.world_checked = True
                        print("Gx world unlocked")
                        print("5ds world unlocked")
                elif imagesearch("images/dm_world_check.jpg") != -1 and imagesearch("images/5ds_world_check.jpg") != -1:
                        self.gx_world = True
                        self._5ds_world = False
                        self.dm_world = False
                        self.world_checked = True
                        print("Gx world unlocked")
                        print("5ds world unlocked")
                elif imagesearch("images/dm_world_check.jpg") != -1 and imagesearch("images/gx_world_check.jpg") != -1:
                        self.gx_world = False
                        self._5ds_world = True
                        self.dm_world = False
                        self.world_checked = True
                        print("Gx world unlocked")
                        print("5ds world unlocked")
                elif imagesearch("images/gm_world_check.jpg") != -1 and imagesearch("images/5ds_world_check.jpg") == -1:
                        self.gx_world = False
                        self._5ds_world = False
                        self.dm_world = True
                        self.world_checked = True
                        print("Gx world unlocked")
                        print("5ds world not unlocked")


        def npc_search(self,lista):
        # Busca los npc en la pantalla dados en la lista y al encontrar uno presiona el botón
        # autoduel luego espera a que el duelo termine para regresar a la pantalla y seguir 
        # buscando npc.l
                Image_list = lista
                count = 0 
                for imagen in Image_list:
                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                return
                        pos = imagesearch(imagen)
                        if pos[0] == -1:
                                print(imagen+" not found, waiting")
                                count += 1
                                sleep(0.1)
                        elif pos[0] != -1:
                                print("npc encontrado")
                                click_image(imagen, pos, "left", 0.2)
                                sleep(2)
                                while imagesearch("images/auto_duel_button.jpg") == [-1,-1]: # clickea hasta encontrar el botón auto-duel
                                        if self.detener.is_set():
                                                return  
                                        sleep(1)
                                        if imagesearch("images/character_text.jpg"):
                                                click_image("images/character_text.jpg", imagesearch("images/character_text.jpg"), "left", 0.2)
                                                sleep(1)
                                        else:
                                                return
                                click_image("images/auto_duel_button.jpg", imagesearch("images/auto_duel_button.jpg"), "left", 0.2) # clickea el botón autoduel
                                # Se busca de forma constante el botón ok que aparece luego de terminar el duelo
                                # y lo clickea al aparecer junto a los botones next hasta quedar de nuevo en la 
                                # pantalla principal
                                ok_button = imagesearch("images/pop_up_ok.jpg")
                                while ok_button == [-1,-1]:    
                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                return
                                        ok_button = imagesearch("images/pop_up_ok.jpg")
                                click_image("images/pop_up_ok.jpg", ok_button, "left", 0.2)
                                # Se ejecuta el mismo código 2 veces para presionar next en
                                # las pantallas de experiencia y de puntaje
                                next_button = imagesearch("images/Button_next.jpg",3)
                                while next_button == [-1,-1]:    
                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                return
                                        if imagesearch("images/level_up.jpg") != [-1,-1]:
                                                click_image("images/level_up.jpg", imagesearch("images/level_up.jpg"), "left", 0.2)
                                        next_button = imagesearch("images/Button_next.jpg")
                                click_image("images/pop_up_ok.jpg", next_button, "left", 0.2)
                                next_button = imagesearch("images/Button_next.jpg",3)
                                while next_button == [-1,-1]:    
                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                return
                                        next_button = imagesearch("images/Button_next.jpg")
                                click_image("images/pop_up_ok.jpg", next_button, "left", 0.2)
                                # Detecta el dialogo del personaje al finalizar el duelo y clickea hasta
                                # volver a la pantalla principal
                                dialogo = imagesearch("images/character_text.jpg")
                                while dialogo == [-1,-1]:
                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                return
                                        dialogo = imagesearch("images/character_text.jpg")
                                while imagesearch("images/character_text.jpg") != [-1,-1]:
                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                return
                                        click_image("images/character_text.jpg", dialogo, "left", 0.2)
                                        sleep(1)




        def stop(self):
                self.detener.set()

