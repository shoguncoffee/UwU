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

    def fun11():
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
                if trip == "Round Trip" and (dd1+"/"+dd2+"/"+dd3 == rd1+"/"+rd2+"/"+rd3):
                    messagebox.showerror("Error","Departure and Return date cannot be same")
                elif trip == "Round Trip" and dd1+"/"+dd2+"/"+dd3 > rd1+"/"+rd2+"/"+rd3:
                    messagebox.showerror("Error","Departure date cannot be greater than Return date")
                else:

                    #algorithm for searching flight

                    data = {"from":f,"to":t,"departure":dd1+"/"+dd2+"/"+dd3,"return":rd1+"/"+rd2+"/"+rd3,"passenger":p,"class":c}
                    r = requests.get(url = API_ENDPOINT1, data = data)
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
            
    Bc=Button(root2,text="Search",bg='green',command=fun11).grid(row=4,column=3)
    root2.mainloop()

def fun2():
    root.destroy()
    root4=Tk()
    root4.title("Cancel Booking")
    Label(root4,text="Enter Booking ID").grid(row=0,column=0)
    l1=Entry(root4)
    l1.grid(row=1,column=0)
    def fun21():
        b = l1.get()
        if b=="":
            messagebox.showerror("Error","Please enter Booking ID")
        else:
            #algorithm for canceling booking
            root4.destroy()
            root5=Tk()
            root5.title("Cancel Booking")
            Label(root5,text="Booking Cancelled Successfully").pack()
            root5.mainloop()
    Bc=Button(root4,text="Cancel",bg='green',command=fun21).grid(row=2,column=0)
    root4.mainloop()

def fun3():
    root.destroy()
    root6=Tk()
    root6.title("Book Flight")
    Label(root6,text="Enter Booking ID").grid(row=0,column=0)
    l1=Entry(root6)
    l1.grid(row=1,column=0)
    def fun31():
        b = l1.get()
        if b=="":
            messagebox.showerror("Error","Please enter Booking ID")
        else:
            #algorithm for booking flight
            root6.destroy()
            root7=Tk()
            root7.title("Book Flight")
            Label(root7,text="Flight Booked Successfully").pack()
            root7.mainloop()
    Bc=Button(root6,text="Book",bg='green',command=fun31).grid(row=2,column=0)
    root6.mainloop()
    
def fun4():
    root.destroy()
    root8=Tk()
    root8.title("View Booking")
    Label(root8,text="Enter Booking ID").grid(row=0,column=0)
    l1=Entry(root8)
    l1.grid(row=1,column=0)
    def fun41():
        b = l1.get()
        if b=="":
            messagebox.showerror("Error","Please enter Booking ID")
        else:
            #algorithm for viewing booking
            root8.destroy()
            root9=Tk()
            root9.title("View Booking")
            Label(root9,text="Booking Details").pack()
            root9.mainloop()
    Bc=Button(root8,text="View",bg='green',command=fun41).grid(row=2,column=0)
    root8.mainloop()
def fun5():
    root.destroy()
    root10=Tk()
    root10.title("Login")
    Label(root10,text="Username").grid(row=0,column=0)
    l1=Entry(root10)
    l1.grid(row=1,column=0)
    Label(root10,text="Password").grid(row=0,column=1)
    l2=Entry(root10,show="*")
    l2.grid(row=1,column=1)
    def fun51():
        u = l1.get()
        p = l2.get()
        if u=="" or p=="":
            messagebox.showerror("Error","Please enter Username and Password")
        else:
            #algorithm for login
            root10.destroy()
            root11=Tk()
            root11.title("Login")
            Label(root11,text="Login Successful").pack()
            root11.mainloop()
    Bc=Button(root10,text="Login",bg='green',command=fun51).grid(row=2,column=0)
    root10.mainloop()

def fun6():
    root.destroy()
    root12=Tk()
    root12.title("Register")
    Label(root12,text="Username").grid(row=0,column=0)
    l1=Entry(root12)
    l1.grid(row=1,column=0)
    Label(root12,text="Password").grid(row=0,column=1)
    l2=Entry(root12,show="*")
    l2.grid(row=1,column=1)
    Label(root12,text="Confirm Password").grid(row=0,column=2)
    l3=Entry(root12,show="*")
    l3.grid(row=1,column=2)
    def fun61():
        u = l1.get()
        p = l2.get()
        cp = l3.get()
        if u=="" or p=="" or cp=="":
            messagebox.showerror("Error","Please fill all the fields")
        else:
            if p!=cp:
                messagebox.showerror("Error","Password and Confirm Password do not match")
            else:
                data = {'username':u,'password':p}
                r = requests.post(url = API_ENDPOINT1, json = data)
                print(r.text)

                #algorithm for registration
                #need to fix this

                root12.destroy()
                root13=Tk()
                root13.title("Register")
                Label(root13,text="Registration Successful").pack()
                root13.mainloop()
    Bc=Button(root12,text="Register",bg='green',command=fun61).grid(row=2,column=0)
    root12.mainloop()

B1=Button(root,text="Search Flight",command=fun1).pack()
B2=Button(root,text="Cancel Booking",command=fun2).pack()
B3=Button(root,text="Book Flight",command=fun3).pack()
B4=Button(root,text="View Booking",command=fun4).pack()
B5=Button(root,text="Login",command=fun5).pack()
B6=Button(root,text="Register",command=fun6).pack()
B7=Button(root,text="Exit",command=root.destroy).pack()
