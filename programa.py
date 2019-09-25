import threading
import numpy as np
from time import sleep
from tkinter import ttk
from tkinter import messagebox

from imagesearch import click_image, imagesearch, imagesearch_numLoop, imagesearch_loop





class DetectarPantalla(threading.Thread):
        ''' 
        Clase que crea un thread que busca imágenes dadas en una lista 
        continuamente hasta encontrarse y clickea la imagen en la pantalla.

        '''
        def __init__(self, npc_checkbutton, farm_gate_button, cuadro_de_texto, tagbutton, duelistas):
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
                self.npc_searched = False
                self.npc_search_checkbox = npc_checkbutton
                self.farm_button = farm_gate_button
                self.tag_check = tagbutton
                self.texto = cuadro_de_texto
                self.lista_duelistas = duelistas
                self.contador_de_lineas = 2.0
                self.image_list = ["images/Button_next.jpg", "images/go_back_button.jpg",
                    "images/pop_up_ok.jpg", "images/close_button.jpg", 
                    "images/Gate_on.jpg", "images/initiateLink.jpg", 
                    "images/Suspended_duel.jpg", "images/duel_studio_on.jpg",
                    "images/avanzar_escena.jpg", "images/pvp_arena_on.jpg",
                    "images/shop_on.jpg", "images/character_text.jpg", 
                    "images/level_up.jpg"
                    ]
                self.npcdm_list = ["npc/andrew1.jpg", "npc/andrew2.jpg", "npc/andrew3.jpg",
                    "npc/andrew4.jpg", 
                    "npc/ashley1.jpg", "npc/ashley2.jpg", "npc/bella1.jpg", "npc/bella2.jpg", 
                    "npc/bella3.jpg", "npc/bella4.jpg", "npc/bella5.jpg", "npc/christine1.jpg", 
                    "npc/christine2.jpg", "npc/christine3.jpg", "npc/christine4.jpg", 
                    "npc/daniel1.jpg", 
                    "npc/daniel2.jpg", "npc/david1.jpg", "npc/david2.jpg", "npc/emma1.jpg", 
                    "npc/emma2.jpg", "npc/emma3.jpg", "npc/emma4.jpg", 
                    "npc/espa_roba1.jpg", "npc/espa_roba2.jpg", 
                    "npc/hailey1.jpg", "npc/hailey2.jpg", "npc/jess1.jpg", "npc/jess2.jpg", 
                    "npc/jess3.jpg", "npc/jess4.jpg", "npc/joey1.jpg",  "npc/joey2.jpg", 
                    "npc/joey3.jpg",
                    "npc/josh1.jpg", "npc/josh2.jpg", "npc/josh3.jpg", "npc/mickey1.jpg", 
                    "npc/meg1.jpg", "npc/meg2.jpg", "npc/meg3.jpg", "npc/mokuba1.jpg",
                    "npc/weevil_own.jpg"
                    ]
                self.npcgx_list = ["npc/alyssa1.jpg", "npc/bastion1.jpg"
                    "npc/bella1.jpg", "npc/bella2.jpg", 
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
                                # if self.tag_check.state() == ('selected',):
                                #         tag_duel = threading.Thread(target=self.tag_duel, daemon=True)
                                #         tag_duel.start()
                                #         tag_duel.join()
                                self.pos = imagesearch(imagen, precision=0.9)
                                if self.pos[0] == -1:
                                        print(imagen+" not found, waiting")
                                        sleep(0.1)
                                else:   #Si encuentra un personaje hablando clickea hasta que 
                                        # se calle
                                        print(self.pos[0])
                                        while index == 11:
                                                if self.detener.is_set():
                                                        return 
                                                if imagesearch(imagen) == [-1,-1]:
                                                        break
                                                else:
                                                        click_image(imagen, imagesearch(imagen), "left", 0.2)
                                                        sleep(1)
                                        # Al encontrar una imagen de la lista de 
                                        # que no sean algunas de las 4 pantallas principales
                                        # clickea sobre ellas
                                        if index in {0,1,2,3,5,6,8,12}:
                                                click_image(imagen, self.pos, "left", 0.2)
                                        elif index in {7,9,10}:
                                                self.change_screen(to_gate=True)
                                        elif index == 4:
                                                self.imprimir_texto("Gate detected")
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
                                                        self.imprimir_texto("Buscando npc...")
                                                        if self.dm_world:
                                                                search_npc = threading.Thread(target=self.npc_search(self.npcdm_list), daemon=True)
                                                                search_npc.start()
                                                                search_npc.join()
                                                        elif self.gx_world:
                                                                search_npc = threading.Thread(target=self.npc_search(self.npcgx_list), daemon=True)
                                                                search_npc.start()
                                                                search_npc.join()
                                                        elif self._5ds_world:
                                                                search_npc = threading.Thread(target=self.npc_search(self.npc5ds_list), daemon=True)
                                                                search_npc.start()
                                                                search_npc.join()
                                                if self.farm_button.state() == ('selected',):
                                                                farm = threading.Thread(target=self.farm_gate, daemon=True)
                                                                farm.start()
                                                                farm.join()


        def check_world(self):
                # Busca el botón de cambiar mundos y verifica en que mundo está
                # (cambiando la variable a True) dependiendo de cuales mundos aparezcan 
                # en las imágenes una vez presionado el botón
                coord = None
                contador = 0
                world_check_button = list(map(imagesearch, ("images/check_world_button.jpg", 
                                "images/check_world_button2.jpg", "images/check_world_button3.jpg",
                                "images/check_world_button4.jpg", "images/check_world_button5.jpg",
                                "images/check_world_button6.jpg", "images/check_world_button7.jpg")))
                
                for cordx, cordy in world_check_button:  
                        if not -1 in {cordx,cordy}:
                                x = cordx
                                y = cordy
                                coord = [x,y]
                                break
                        if contador == len(world_check_button) - 1:
                                self.imprimir_texto("no se encontró el botón para verificar el mundo")
                                self.imprimir_texto("se dará por hecho que se está en dm y por los npc buscados serán de este mundo")
                                self.gx_world = False
                                self._5ds_world = False
                                self.dm_world = True
                                self.world_checked = True
                                return
                        contador += 1
                click_image("images/check_world_button.jpg", coord, "left", 0.1)
                if imagesearch("images/gx_world_check.jpg")[0] != -1 and imagesearch("images/5ds_world_check.jpg")[0] != -1:    
                        self.gx_world = False
                        self._5ds_world = False
                        self.dm_world = True
                        self.world_checked = True
                        self.imprimir_texto("Gx world unlocked")
                        self.imprimir_texto("5ds world unlocked")
                        self.imprimir_texto("Se encuentra en dm world")
                elif imagesearch("images/dm_world_check.jpg")[0] != -1 and imagesearch("images/5ds_world_check.jpg")[0] != -1:
                        self.gx_world = True
                        self._5ds_world = False
                        self.dm_world = False
                        self.world_checked = True
                        self.imprimir_texto("Gx world unlocked")
                        self.imprimir_texto("5ds world unlocked")
                        self.imprimir_texto("Se encuentra en gx world")
                elif imagesearch("images/dm_world_check.jpg")[0] != -1 and imagesearch("images/gx_world_check.jpg")[0] != -1:
                        self.gx_world = False
                        self._5ds_world = True
                        self.dm_world = False
                        self.world_checked = True
                        self.imprimir_texto("Gx world unlocked")
                        self.imprimir_texto("5ds world unlocked")
                        self.imprimir_texto("Se encuentra en 5ds world")
                elif imagesearch("images/dm_world_check.jpg")[0] != -1 and imagesearch("images/5ds_world_check.jpg")[0] == -1:
                        self.gx_world = False
                        self._5ds_world = False
                        self.dm_world = True
                        self.world_checked = True
                        self.imprimir_texto("Gx world unlocked")
                        self.imprimir_texto("5ds world not unlocked")
                        self.imprimir_texto("Se encuentra en dm world")
                elif imagesearch("images/dm_world_check.jpg")[0] != -1 and imagesearch("images/5ds_world_check.jpg")[0] == -1:
                        self.gx_world = False
                        self._5ds_world = False
                        self.dm_world = True
                        self.world_checked = True
                        self.imprimir_texto("Gx world unlocked")
                        self.imprimir_texto("5ds world not unlocked")
                        self.imprimir_texto("Se encuentra en gx world")


        def change_screen(self, to_gate=False):
                if to_gate:
                        gate_coord = imagesearch("images/Gate_off.jpg")
                        if gate_coord[0] != -1:
                                click_image("images/Gate_off.jpg", gate_coord, "left", 0.2)
                                self.gate = True
                                self.shop = False
                                self.pvp_arena = False
                                self.duel_studio = False
                        else:
                                return
                else:
                        if self.gate:
                                pvp_coord = imagesearch("images/pvp_arena_off.jpg")
                                click_image("images/pvp_arena_off.jpg", pvp_coord, "left", 0.2)
                                self.gate = False
                                self.shop = False
                                self.pvp_arena = True
                                self.duel_studio = False
                                self.npc_searched = False
                        elif self.pvp_arena:
                                shop_coord = imagesearch("images/shop_off.jpg")
                                click_image("images/shop_off.jpg", shop_coord, "left", 0.2)
                                self.gate = False
                                self.shop = True
                                self.pvp_arena = False
                                self.duel_studio = False
                        elif self.shop:
                                studio_coord = imagesearch("images/duel_studio_off.jpg")
                                click_image("images/shop_off.jpg", studio_coord, "left", 0.2)
                                self.gate = False
                                self.shop = False
                                self.pvp_arena = False
                                self.duel_studio = True
                        elif self.duel_studio:
                                gate_coord = imagesearch("images/Gate_off.jpg")
                                click_image("images/Gate_off.jpg", gate_coord, "left", 0.2)
                                self.gate = True
                                self.shop = False
                                self.pvp_arena = False
                                self.duel_studio = False
                                self.npc_searched = True


        def tag_duel(self):
                while True:
                        # Busca el botón "tag duel"
                        tag_button = imagesearch("images/tag_duel_button.jpg")
                        # Idenficamos si estamos en la pantalla de elección de la copa
                        cup = imagesearch("images/choose_cup.jpg")
                        while tag_button[0] == -1:
                                if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                        return
                                # En caso de recibir premio después del duelo se buscará
                                # y presionará el botón ok
                                ok_button = imagesearch("images/pop_up_ok.jpg")
                                if ok_button[0] != -1:
                                        click_image("images/pop_up_ok.jpg", ok_button, "left", 0.2)
                                elif cup[0] != -1:
                                        click_image("images/pop_up_ok.jpg", cup, "left", 0.2)
                                tag_button = imagesearch("images/tag_duel_button.jpg")
                        # Se clickeará el botóg "tag duel" hasta que ya no salga en pantalla
                        while tag_button[0] != -1:
                                if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                        return
                                click_image("images/tag_duel_button.jpg", tag_button, "left", 0.2)
                                tag_button = imagesearch("images/tag_duel_button.jpg")
                        # Hará los clicks correspondientes hasta que le botón de autoduel aparezca
                        # en pantalla
                        while imagesearch("images/auto_duel_button.jpg") == [-1,-1]: # clickea hasta encontrar el botón auto-duel
                                if self.detener.is_set():
                                        return  
                                bonus_screen = imagesearch("images/tag_bonus40.jpg")
                                dialogo = imagesearch("images/character_text.jpg")
                                if bonus_screen[0] != -1:
                                        click_image("images/tag_bonus40.jpg", bonus_screen, "left", 0.2)
                                elif dialogo[0] != -1:
                                        click_image("images/character_text.jpg", dialogo, "left", 0.2)
                                elif imagesearch("images/choose_cup.jpg")[0] != -1:
                                        print("ga")
                                        break
                        # clickeará el botón autoduel y luego buscará de forma constante
                        # el botón "ok" que sale una vez finalizado el duelo y los
                        # botones siguientes hasta quedar nuevamente en la pantalla
                        # con el botón de "tag duel"
                        if imagesearch("images/auto_duel_button.jpg")[0] != -1:
                                        click_image("images/auto_duel_button.jpg", imagesearch("images/auto_duel_button.jpg"), "left", 0.2) # clickea el botón autodue
                                        ok_button = imagesearch("images/pop_up_ok.jpg")
                                        while ok_button[0] == -1:
                                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                                return
                                                        ok_button = imagesearch("images/pop_up_ok.jpg") 
                                        while True:
                                                if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                        return
                                                ok_button = imagesearch("images/pop_up_ok.jpg")
                                                dialogo = imagesearch("images/character_text.jpg", precision=0.9)
                                                level_up_screen = imagesearch("images/level_up.jpg", precision=0.9)
                                                if ok_button[0] != -1:
                                                        click_image("images/pop_up_ok.jpg", ok_button, "left", 0.2)
                                                        sleep(1)
                                                elif level_up_screen[0] != -1:
                                                        click_image("images/level_up.jpg", level_up_screen, "left", 0.2)
                                                        sleep(1)
                                                elif dialogo[0] != -1:
                                                        while dialogo != [-1,-1]:
                                                                if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                                        return
                                                                click_image("images/character_text.jpg", dialogo, "left", 0.2)
                                                                sleep(1)
                                                                dialogo = imagesearch("images/character_text.jpg")
                                                                tag_button = imagesearch("images/tag_duel_button.jpg")
                                                                if tag_button[0] != -1:
                                                                        break
                                                        break                     


        def npc_search(self,lista):
                npc_gate = False
                npc_pvp = False
                npc_shop = False
                npc_studio = False
                while self.npc_search_checkbox.state() == ('selected',):
                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                        return
                        # Busca los npc en la pantalla dados en la lista y al encontrar uno presiona el botón
                        # autoduel luego espera a que el duelo termine para regresar a la pantalla y seguir 
                        # buscando npc
                        Image_list = lista
                        for imagen in Image_list:
                                if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                        return
                                pos = imagesearch(imagen,precision=0.9)
                                if pos[0] == -1:
                                        print(imagen+" not found, waiting")
                                elif pos[0] != -1:
                                        print("npc encontrado")
                                        print(pos)
                                        click_image(imagen, pos, "left", 0.2)
                                        sleep(3)
                                        while imagesearch("images/auto_duel_button.jpg") == [-1,-1]: # clickea hasta encontrar el botón auto-duel
                                                if self.detener.is_set():
                                                        return  
                                                sleep(1)
                                                if imagesearch("images/character_text.jpg") != [-1,-1]:
                                                        click_image("images/character_text.jpg", imagesearch("images/character_text.jpg"), "left", 0.2)
                                                        sleep(1)
                                                else:
                                                        break
                                        if imagesearch("images/auto_duel_button.jpg")[0] != -1:
                                                click_image("images/auto_duel_button.jpg", imagesearch("images/auto_duel_button.jpg"), "left", 0.2) # clickea el botón autoduel
                                        sleep(3)
                                        # Se busca de forma constante los botones ok y next para regresar a la pantalla
                                        # principal una vez finalizado el duelo
                                        self.salir_de_duelo()     
                        self.change_screen()
                        if all((npc_gate, npc_pvp, npc_shop, npc_studio)):
                                print("Se ha completado la busqueda de todos los npc en este mundo")
                                npc_gate = False
                                npc_pvp = False
                                npc_shop = False
                                npc_studio = False
                                return
                        else:
                                if npc_shop:
                                        npc_studio = True
                                elif npc_pvp:
                                        npc_shop = True
                                elif npc_gate:
                                        npc_pvp = True     
                                elif not npc_gate:
                                        npc_gate = True
                        

        def coord_for_multiple(self, images_tuple):
                for cordx, cordy in list(map(imagesearch, images_tuple)):
                        coord = None
                        if not -1 in {cordx,cordy}:
                                x = cordx
                                y = cordy
                                coord = [x,y]
                                return coord
                return [-1,-1]


        def farm_gate(self):
                while True:
                        if self.detener.is_set():
                                return
                        if not self.gate:
                                self.change_screen(to_gate=True)
                        self.clickear_puerta()
                        for x, y in enumerate(self.lista_duelistas):
                                if self.detener.is_set():
                                        return
                                self.verificar_duelista(x)
                                
                 


        def verificar_duelista(self, nro_duelista):
                if self.lista_duelistas[nro_duelista][0].state() == ('selected',):
                        cantidad = self.lista_duelistas[nro_duelista][1].get()
                        if not cantidad.isdigit():
                                messagebox.showerror("caracter inválido", "Solo debe introducir números en la" 
                                                     + "casilla 'n° duels' de la pestaña 'duelistas'")
                                self.stop()
                                return
                        cantidad = int(cantidad)
                        while cantidad > 0:
                                if self.detener.is_set():
                                        return
                                if imagesearch('images/Gate_on.jpg')[0] != -1:
                                        self.clickear_puerta()
                                self.duelear_en_puerta(self.lista_duelistas[nro_duelista][0]['text'],
                                                        self.lista_duelistas[nro_duelista][2].get())
                else:
                        return 0


        def clickear_puerta(self):
                if self.gate:
                        coord_gate = imagesearch("images/gate_piece.jpg")
                        while coord_gate[0] == -1:
                                if self.detener.is_set():
                                        return
                                self.change_screen(to_gate=True)
                                coord_gate = imagesearch("images/gate_piece.jpg")
                        click_image("images/gate_piece.jpg", coord_gate, "left", 0.2)
                        go_back_button = imagesearch('images/go_back_button.jpg')
                        while go_back_button[0] == -1:
                                click_image("images/gate_piece.jpg", coord_gate, "left", 0.2)
                                sleep(2)
                                go_back_button = imagesearch('images/go_back_button.jpg')
                        
                        
        def duelear_en_puerta(self, duelista, nivel):
                duelistas = {
                        'Yami Yugi': 'images/yami_yugi_text.jpg',
                        'Seto Kaiba': 'images/seto_kaiba_text.jpg'
                        }
                niveles = {
                        'lvl 10' : 'images/lvl_10_check.jpg',
                        'lvl 20' : 'images/lvl_20_check.jpg',
                        'lvl 30' : 'images/lvl_30_check.jpg',
                        'lvl 40' : 'images/lvl_40_check.jpg'
                        }
                if duelista == 'Yami Yugi':
                                self.buscar_en_puerta(duelistas[duelista], niveles[nivel])
                                self.salir_de_duelo()
               
                    
                        
        '''
        Busca al duelista una vez clickeada la puerta, clickea en su nivel y comienza el duelo
        
        duelista: nombre del duelista a buscar
        nivel: nivel del duelista pasado como string "lvl x"
        '''                
        def buscar_en_puerta(self, duelista, nivel):
                flecha_cambiar = imagesearch('images/flecha_cambiar_duelista.jpg')
                while flecha_cambiar[0] == -1:
                        if self.detener.is_set():
                                return
                        flecha_cambiar = imagesearch('images/flecha_cambiar_duelista.jpg')
                nombre_duelista = imagesearch(duelista)
                while nombre_duelista[0] == -1:
                        if self.detener.is_set():
                                return
                        click_image('images/flecha_cambiar_duelista.jpg', flecha_cambiar, 'left', 0.2)
                        sleep(2)
                        nombre_duelista = imagesearch(duelista)
                nivel_duelista = imagesearch(nivel)
                if nivel_duelista[0] != -1:
                        click_image(nivel, nivel_duelista, 'left', 0.2)
                        coor_duel_button = imagesearch("images/duel_button.jpg")
                        click_image("images/duel_button.jpg", coor_duel_button, "left", 0.2)
                        sleep(2)
                        dialogo = imagesearch("images/character_text.jpg")
                        while dialogo != [-1,-1]:
                                if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                        return
                                click_image("images/character_text.jpg", dialogo, "left", 0.2)
                                sleep(1)
                                dialogo = imagesearch("images/character_text.jpg")
                                if imagesearch("images/duel_button.jpg")[0] != -1:
                                        break
                        coor_duel_button = imagesearch("images/duel_button.jpg")
                        click_image("images/duel_button.jpg", coor_duel_button, "left", 0.2)


        '''
        Una vez iniciado el duelo busca de forma constante los botones ok y next hasta
        salir a la pantalla principal donde una vez que la detecta sale de la función
        
        '''        
        def salir_de_duelo(self):
                while True:
                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                return
                        ok_button = imagesearch("images/pop_up_ok.jpg") 
                        next_button = imagesearch("images/Button_next.jpg")
                        level_up_screen = imagesearch("images/level_up.jpg")
                        dialogo = imagesearch("images/character_text.jpg")
                        if ok_button[0] != -1:
                                click_image("images/pop_up_ok.jpg", ok_button, "left", 0.2)
                                sleep(2)
                        elif next_button[0] != -1:
                                click_image("images/Button_next.jpg", next_button, "left", 0.2)
                                sleep(2)
                        elif level_up_screen[0] != -1:
                                click_image("images/level_up.jpg", level_up_screen, "left", 0.2)
                                sleep(2)
                        # Se detecta la pantalla de diálogo después del duelo y clickea hasta que el personaje
                        # deja de hablar
                        elif dialogo[0] != -1:
                                while dialogo != [-1,-1]:
                                        if self.detener.is_set(): # Si se presiona el botón stop la busqueda se detiene
                                                return
                                        click_image("images/character_text.jpg", dialogo, "left", 0.2)
                                        sleep(1)
                                        dialogo = imagesearch("images/character_text.jpg")
                        elif imagesearch("images/Gate.jpg")[0] != -1:
                                return


        def imprimir_texto(self, texto):
                
                self.texto.config(state='normal')
                self.texto.insert(str(self.contador_de_lineas), texto + "\n")
                self.texto.config(state='disabled')
                self.contador_de_lineas += 1.0
                    
                                                       
        def stop(self):
                self.detener.set()

