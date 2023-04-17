from tkinter import *
from tkinter import ttk

API_ENDPOINT1 = "http://127.0.0.1:800/"

root = Tk()
Label(root,text="Qatar Airways",font="Bold 20").pack()

def fun1():
    root.destroy()
    root2=Tk()
    root2.title("Search Flight")
    Label(root2,text="FROM").grid(row=0,column=0)
    l1 = ttk.Combobox(root2,height=5,width=15,values=["New York","Chicago","Dallas","San Francisco"])
    l1.grid(row=1,column=0)
    Label(root2,text="TO").grid(row=0,column=1)
    l2 = ttk.Combobox(root2,height=5,width=15,values=["New York","Chicago","Dallas","San Francisco"])
    l2.grid(row=1,column=1)
    Label(root2,text="Trip").grid(row=0,column=2)
    l3 = ttk.Combobox(root2,height=5,width=15,values=["One Way","Round Trip"])
    l3.grid(row=1,column=2)
    Label(root2,text="Departure Date").grid(row=0,column=3)
    l4 = ttk.Combobox(root2,height=5,width=15,values=["1/01/2020","2/01/2020","3/01/2020","4/01/2020"])
    l4.grid(row=1,column=3)
    Label(root2,text="Return Date").grid(row=0,column=4)
    l5 = ttk.Combobox(root2,height=5,width=15,values=["-","1/01/2020","2/01/2020","3/01/2020","4/01/2020"])
    l5.grid(row=1,column=4)
    if l3.get() == "One Way":
        l5.set("-")
    Label(root2,text="Passenger").grid(row=0,column=5)
    l6 = ttk.Combobox(root2,height=5,width=15,values=["1","2","3","4","5","6","7","8","9"])
    l6.grid(row=1,column=5)
    Label(root2,text="Class").grid(row=0,column=6)
    l7 = ttk.Combobox(root2,height=5,width=15,values=["Economy","Business","First"])
    l7.grid(row=1,column=6)

    def fun2():
        f = l1.get()
        t = l2.get()
        dd = l3.get()
        rd = l4.get()
        p = l5.get()
        c = l6.get()
    


    
    Bc=Button(root2,text="Search",bg='green',command=fun2).grid(row=2,column=3)
    root2.mainloop()


B1=Button(root,text="Search Flight",command=fun1).pack()
#B2=Button(root,text="Cancel Booking",command=fun2).pack()
#B3=Button(root,text="Book Flight",command=fun3).pack()
