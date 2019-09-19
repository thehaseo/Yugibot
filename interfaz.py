import tkinter as tk
from tkinter import scrolledtext, StringVar
from tkinter import ttk
import threading
from imagesearch import *
from programa import DetectarPantalla



class Gui(ttk.Notebook):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pestana1 = PestanaPrincipal(self)
        self.pestana2 = PestanaDuelistas(self)
        self.add(self.pestana1, text='bot', sticky='nsew')
        self.add(self.pestana2, text='duelistas', sticky='nsew')
        self.pestana1.start_button['command'] = self.start_program
        #lista de duelistas de la puerta para pasarselo al programa principal
        
        self.program = None
        

    def start_program(self):
        if self.program is None:
            self.pestana1.text_window.config(state='normal')
            self.pestana1.text_window.delete('1.0', 'end')
            self.pestana1.text_window.insert('1.0', "Detectando pantalla...\n")
            # self.pestana1.text_window.tag_add('right', '1.0', 'end')
            self.pestana1.text_window.config(state='disabled')
            self.program = DetectarPantalla(self.pestana1.npc_search_button, self.pestana1.farm_gate_button, 
                                            self.pestana1.text_window, self.pestana1.tag_duel_button, self.pestana2.lista_de_duelistas)
            self.program.start()
            self.pestana1.start_button["text"] = "Stop"
        else:
            self.program.stop()
            self.pestana1.start_button["text"] = "Start"
            self.program = None



class PestanaPrincipal(tk.Frame):
    '''
        class that holds all buttons from the main tab and organize them in a grid layout 
    '''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.start_button = tk.Button(self,
                                    text="Start", height=3, width=20,
                                    state="normal"
                                    ) 
        self.checkbuttons_frame = tk.Frame(self)
        self.npc_search_button = ttk.Checkbutton(self.checkbuttons_frame, text="npc search", 
                                                takefocus=0)
        self.npc_search_button.state(['!alternate'])
        self.farm_gate_button = ttk.Checkbutton(self.checkbuttons_frame, 
                                                text="Farm gate", takefocus=0) 
        self.farm_gate_button.state(['!alternate'])
        self.tag_duel_button = ttk.Checkbutton(self.checkbuttons_frame, text="auto tag duel", 
                                            takefocus=0, state='disabled') 
        self.tag_duel_button.state(['!alternate'])
        self.text_window = tk.scrolledtext.ScrolledText(self, width=30, height=20, 
                                                        state='disabled', wrap='word')
        # self.text_window.tag_configure('right', justify='right')

        self.checkbuttons_frame.grid(row=0, column=0, sticky='nw')
        self.npc_search_button.grid(row=0, column=0, sticky='w')
        self.farm_gate_button.grid(row=1, column=0, sticky='w')
        self.tag_duel_button.grid(row=2, column=0, sticky='w') 
        self.tag_duel_button.grid_remove() 
        self.start_button.grid(row=1, column=0, columnspan=3, sticky='s', pady=(10,0))      
        self.text_window.grid(row=0, column=1, sticky='nsew', padx=5)
                    
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=2)


class PestanaDuelistas(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Uso 2 frames para dividir la pantalla del frame principal en 2 mitades
        self.mitad1 = tk.Frame(self)
        self.mitad2 = tk.Frame(self)
        
        self.mitad1.grid(row=0, column=0, sticky='nsew')
        self.mitad2.grid(row=0, column=1, sticky='nsew')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=2)
        
        '''
            Crea un checkbutton con el nombre del duelista y al lado un combobox 
            con los niveles del duelista en la puerta
            
            input:
            
            nombre : nombre del duelista
            rw : fila en la que se colocará el checkbutton (debe ser un numero entero)
            clmn : columna en la que se colocará el checkbutton (debe ser un numero entero)
        '''
        def crear_duelista(self, nombre, rw, clmn, mitad):
            duelista = ttk.Checkbutton(mitad, takefocus=0, text=nombre)
            duelista.state(['!alternate'])
            niveldl = ttk.Combobox(mitad, takefocus=0, state='readonly',
                                   justify='right', width=8)
            niveldl['values'] = ('lvl 10', 'lvl 20', 'lvl 30', 'lvl 40')
            texto_cantidad = StringVar()
            cantidad = tk.Entry(mitad, takefocus=0, textvariable=texto_cantidad, width=5)
            
            duelista.grid(row=rw, column=clmn, padx=2, pady=3, sticky='w')
            cantidad.grid(row=rw, column=clmn+1, padx=3, pady=3)
            niveldl.grid(row=rw, column=clmn+2, padx=5, pady=3)
            
            return (duelista, cantidad, niveldl)
            
        
        # Aqui comienza la creación de los checkbuttons de los duelistas 
        self.yami_yugi = crear_duelista(self, 'Yami Yugi', 0, 0, self.mitad1)
        self.seto_kaiba = crear_duelista(self, 'Seto Kaiba', 1, 0, self.mitad1)
        self.joey = crear_duelista(self, 'Joey Wheeler', 3, 0, self.mitad1)
        self.mai = crear_duelista(self, 'Mai Valentine', 4, 0, self.mitad1)
        self.tea = crear_duelista(self, 'Tea Gardner', 5, 0, self.mitad1)
        self.weevil = crear_duelista(self, 'Weevil Underwood', 6, 0, self.mitad1)
        self.rex = crear_duelista(self, 'Rex Raptor', 7, 0, self.mitad1)
        self.mako = crear_duelista(self, 'Mako Tsunami', 8, 0, self.mitad1)
        self.keith = crear_duelista(self, 'Bandit Keith', 9, 0, self.mitad1)
        self.odion = crear_duelista(self, 'Odion', 9, 0, self.mitad1)
        self.ishizu = crear_duelista(self, 'Ishizu Ishtar', 10, 0, self.mitad1)
        self.pegasus = crear_duelista(self, 'Pegasus', 11, 0, self.mitad1)
        self.bakura = crear_duelista(self, 'Yami Bakura', 12, 0, self.mitad1)
        self.marik = crear_duelista(self, 'Yami Marik', 13, 0, self.mitad1)
        self.yugi = crear_duelista(self, 'Yugi Muto', 14, 0, self.mitad1)
        self.paradox = crear_duelista(self, 'Paradox Brothers', 15, 0, self.mitad1)
        self.mokuba = crear_duelista(self, 'Mokuba Kaiba', 16, 0, self.mitad1)
        self.arkana = crear_duelista(self, 'Arkana', 17, 0, self.mitad1)
        self.bonz = crear_duelista(self, 'Bonz', 18, 0, self.mitad1)
        self.roba = crear_duelista(self, 'Espa Roba', 19, 0, self.mitad1)
        self.tristan = crear_duelista(self, 'Tristan Taylor', 20, 0, self.mitad1)
        self.jaden = crear_duelista(self, 'Jaden Yuki', 21, 0, self.mitad1)
        self.chazz = crear_duelista(self, 'Chazz', 0, 0, self.mitad2)
        self.alexis = crear_duelista(self, 'Alexis Rhodes', 1, 0, self.mitad2)
        self.aster = crear_duelista(self, 'Aster Phoenix', 2, 0, self.mitad2)
        self.bastion = crear_duelista(self, 'Bastion Misawa', 3, 0, self.mitad2)
        self.crowler = crear_duelista(self, 'Vellian Crowler', 4, 0, self.mitad2)
        self.jesse = crear_duelista(self, 'Jesse Anderson', 5, 0, self.mitad2)
        self.syrus = crear_duelista(self, 'Syrus Truesdale', 6, 0, self.mitad2)
        self.zane = crear_duelista(self, 'Zane Truesdale', 7, 0, self.mitad2)
        self.tyranno = crear_duelista(self, 'Tyranno Hassleberry', 8, 0, self.mitad2)
        self.yusei = crear_duelista(self, 'Yusei Fudo', 9, 0, self.mitad2)
        self.jack = crear_duelista(self, 'Jack', 10, 0, self.mitad2)
        self.crow = crear_duelista(self, 'Crow Hogan', 11, 0, self.mitad2)
        self.akiza = crear_duelista(self, 'Akiza Izinski', 12, 0, self.mitad2)
        self.leo = crear_duelista(self, 'Leo', 13, 0, self.mitad2)
        self.luna = crear_duelista(self, 'Luna', 14, 0, self.mitad2)
        self.trudge = crear_duelista(self, 'Tetsu Trudge', 15, 0, self.mitad2)
        
        # creación de lista con todos los duelistas de gate para pasarle sus argumentos
        # al programa principal
        self.lista_de_duelistas = [self.yami_yugi, self.seto_kaiba, self.joey, self.mai,
                                   self.mai, self.tea, self.weevil, self.rex, self.mako,
                                   self.keith, self.odion, self.ishizu, self.pegasus, 
                                   self.bakura, self.marik, self.yugi, self.paradox,
                                   self.mokuba, self.arkana, self.bonz, self.roba, 
                                   self.tristan, self.jaden, self.chazz, self.alexis, 
                                   self.aster, self.bastion, self.crowler, self.jesse,
                                   self.syrus, self.zane, self.tyranno, self.yusei, 
                                   self.jack, self.crow, self.akiza, self.leo, self.luna,
                                   self.trudge]
            


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.title("Yu-Gi-Oh duel links bot")
    raiz.geometry('500x600')
    raiz.resizable(width=False, height=False)
    raiz.update_idletasks()
    Gui(raiz, height=raiz.winfo_height(), width=raiz.winfo_width()).grid(row=0, column=0)
    raiz.columnconfigure(0, weight=2)
    raiz.rowconfigure(0, weight=2)
    raiz.mainloop()
