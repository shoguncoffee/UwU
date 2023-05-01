from tkinter import *
from tkinter.ttk import *
import time
 
# toplevel window
root = Tk()
 
def forget():
    b1.forget()
    print("After Forget method called. Is widget mapped? = ", b1.winfo_ismapped())
 
def retrieve():
    b1.pack()
    print("After retrieval of widget. Is widget mapped? = ", b1.winfo_ismapped())
 
# Button widgets
b1 = Button(root, text = "Btn 1")
b1.pack()
 
# This is used to make widget invisible
b2 = Button(root, text = "Btn 2", command=forget)
b2.pack()
  
# This will retrieve widget
b3 = Button(root, text = "Btn 3", command=retrieve)
b3.pack()
 
# infinite loop, interrupted by keyboard or mouse
mainloop()