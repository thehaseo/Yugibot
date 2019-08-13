import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
from imagesearch import *
from programa import DetectarPantalla


class Gui(tk.Frame):
    """
    class that creates all buttons from the GUI and makes callbacks to the functions that
    starts the program.

    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.start_button = tk.Button(
            text="Start", height=3, width=20,
            state="normal", command=self.start_program
            )  # Botón de start del programa
        self.start_button.pack(side="bottom")
        self.variable_npc_button = tk.IntVar()
        self.npc_search_button = ttk.Checkbutton(text="npc search")  # npc search checkbutton
        self.npc_search_button.state(['!alternate'])
        self.npc_search_button.pack(side="left")
        # text screen and scrollbar ins
        self.text_window = tk.scrolledtext.ScrolledText(width=30, height=20, state='disabled', wrap='word')
        self.text_window.pack(side='right')
        self.program = None
        

    def start_program(self):
        if self.program is None:
            self.text_window.config(state='normal')
            self.text_window.delete('1.0', 'end')
            self.text_window.insert('1.0', "Detectando pantalla...\n")
            self.text_window.config(state='disabled')
            self.program = DetectarPantalla(self.npc_search_button)
            self.program.start()
            self.start_button["text"] = "Stop"
        else:
            self.program.stop()
            self.start_button["text"] = "Start"
            self.program = None

            
    def insert_text(self, text):
        self.text_window.insert(text)


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.title("Yu-Gi-Oh duel links bot")
    raiz.resizable(width=False, height=False)
    Gui(raiz).pack(side="top", fill="both", expand=True)
    raiz.mainloop()
