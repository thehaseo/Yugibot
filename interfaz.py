import tkinter as tk
from imagesearch import *
from programa import change


raiz = tk.Tk()

startBoton = tk.Button(text="Start",command=lambda widget='startBoton': change(startBoton),height=3,width=20,state="normal")
startBoton.pack(side="bottom")      


raiz.mainloop()