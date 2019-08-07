import tkinter as tk
from imagesearch import *
from programa import DetectarPantalla


"""
class that creates all buttons from the GUI and makes callbacks to the functions that
starts the program
"""
class Gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.start_button = tk.Button(
            text="Start", height=3, width=20,
            state="normal", command=self.start_program
            )
        self.start_button.pack(side="bottom")
        self.program = None

    def start_program(self):
        if self.program is None:
            self.program = DetectarPantalla()
            self.program.start()
            self.start_button["text"] = "Stop"
        else:
            self.program.stop()
            self.start_button["text"] = "Start"
            self.program = None


if __name__ == "__main__":
    raiz = tk.Tk()
    Gui(raiz).pack(side="top", fill="both", expand=True)
    raiz.mainloop()
