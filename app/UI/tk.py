from tkinter import *
from tkinter import ttk,messagebox
import json
import requests

API_ENDPOINT1 = "http://127.0.0.1:800/search_flight"

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
    l41 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 32)))
    l41.grid(row=1,column=3)
    l42 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 13)))
    l42.grid(row=2,column=3)
    l43 = ttk.Combobox(root2,height=5,width=15,values=list(range(2020, 2025)))
    l43.grid(row=3,column=3)
    Label(root2,text="Return Date").grid(row=0,column=4)
    l51 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 32)))
    l51.grid(row=1,column=4)
    l52 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 13)))
    l52.grid(row=2,column=4)
    l53 = ttk.Combobox(root2,height=5,width=15,values=list(range(2020, 2025)))
    l53.grid(row=3,column=4)
    Label(root2,text="Passenger").grid(row=0,column=5)
    l6 = ttk.Combobox(root2,height=5,width=15,values=["1","2","3","4","5","6","7","8","9"])
    l6.grid(row=1,column=5)
    Label(root2,text="Class").grid(row=0,column=6)
    l7 = ttk.Combobox(root2,height=5,width=15,values=["Economy","Business","First"])
    l7.grid(row=1,column=6)

    def fun2():
        f = l1.get()
        t = l2.get()
        trip = l3.get()
        dd1 = l41.get()
        dd2 = l42.get()
        dd3 = l43.get()
        rd1 = l51.get()
        rd2 = l52.get()
        rd3 = l53.get()
        p = l6.get()
        c = l7.get()
        if f=="" or t=="" or trip=="" or dd1=="" or dd2=="" or dd3=="" or rd1=="" or rd2=="" or rd3=="" or p=="" or c=="":
            messagebox.showerror("Error","Please fill all the fields")
        else:
            if f == t:
                messagebox.showerror("Error","Source and Destination cannot be same")
            else:
                if dd1+"/"+dd2+"/"+dd3 == rd1+"/"+rd2+"/"+rd3:
                    messagebox.showerror("Error","Departure and Return date cannot be same")
                else:
                    if dd1+"/"+dd2+"/"+dd3 > rd1+"/"+rd2+"/"+rd3:
                        messagebox.showerror("Error","Departure date cannot be greater than Return date")
                    else:
                        if c == "Economy":
                            c = "E"
                        elif c == "Business":
                            c = "B"
                        else:
                            c = "F"
                        
                        
                        url = API_ENDPOINT1 + "search"
                        data = {"from":f,"to":t,"departure":dd1+"/"+dd2+"/"+dd3,"return":rd1+"/"+rd2+"/"+rd3,"passenger":p,"class":c}
                        r = requests.post(url = url, data = data)
                        print(r.text)
                        root2.destroy()
                        root3=Tk()
                        root3.title("Search Flight")
                        Label(root3,text="Flight No").grid(row=0,column=0)
                        Label(root3,text="Airline").grid(row=0,column=1)
                        Label(root3,text="Departure").grid(row=0,column=2)
                        Label(root3,text="Arrival").grid(row=0,column=3)
                        Label(root3,text="Duration").grid(row=0,column=4)
                        Label(root3,text="Price").grid(row=0,column=5)
                        Label(root3,text="Book").grid(row=0,column=6)
                        root3.mainloop()
            
    Bc=Button(root2,text="Search",bg='green',command=fun2).grid(row=4,column=3)
    root2.mainloop()


B1=Button(root,text="Search Flight",command=fun1).pack()
#B2=Button(root,text="Cancel Booking",command=fun2).pack()
#B3=Button(root,text="Book Flight",command=fun3).pack()
