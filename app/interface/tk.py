from tkinter import *
from tkinter import ttk,messagebox
import json
import requests

API_ENDPOINT1 = "http://127.0.0.1:8000/search/one-way"
API_DATA1 = "http://127.0.0.1:8000/data/airports"

root = Tk()
Tk.geometry(root,"500x500")
Label(root,text="Qatar Airways",font="Bold 20").pack()
airports = requests.get(API_DATA1).json()
airports_code = [airport["location_code"] for airport in airports]

def fun1():
    root.destroy()
    root2=Tk()
    root2.title("Search Flight")
    Label(root2,text="FROM").grid(row=0,column=0)
    l1 = ttk.Combobox(root2,height=5,width=15,values=airports_code) #need to change to airport
    l1.grid(row=1,column=0)
    Label(root2,text="TO").grid(row=0,column=1)
    l2 = ttk.Combobox(root2,height=5,width=15,values=airports_code) #need to change to airport
    l2.grid(row=1,column=1)
    Label(root2,text="Trip").grid(row=0,column=2)
    l3 = ttk.Combobox(root2,height=5,width=15,values=["One Way"]) #delete Round Trip
    l3.grid(row=1,column=2)
    Label(root2,text="Departure Date").grid(row=0,column=3)
    l41 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 32)))
    l41.grid(row=1,column=3)
    l41.insert(0,"Day")
    l42 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 13)))
    l42.grid(row=2,column=3)
    l42.insert(0,"Month")
    l43 = ttk.Combobox(root2,height=5,width=15,values=['2023']) #need to add more year
    l43.grid(row=3,column=3)
    l43.insert(0,"Year")
    '''Label(root2,text="Return Date").grid(row=0,column=4)
    l51 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 32)))
    l51.grid(row=1,column=4)
    l52 = ttk.Combobox(root2,height=5,width=15,values=list(range(1, 13)))
    l52.grid(row=2,column=4)
    l53 = ttk.Combobox(root2,height=5,width=15,values=list(range(2020, 2025)))
    l53.grid(row=3,column=4)'''
    Label(root2,text="Passenger").grid(row=0,column=5)
    l61 = ttk.Combobox(root2,height=5,width=15,values=["1","2","3","4","5","6","7","8","9"])
    l61.insert(0,"Adult")
    l61.grid(row=1,column=5)
    l62 = ttk.Combobox(root2,height=5,width=15,values=["0","1","2","3","4","5","6","7","8","9"])
    l62.grid(row=2,column=5)
    l62.insert(0,"Children")
    l63 = ttk.Combobox(root2,height=5,width=15,values=["0","1","2","3","4","5","6","7","8","9"])
    l63.grid(row=3,column=5)
    l63.insert(0,"Infant")

    '''Label(root2,text="Class").grid(row=0,column=6)
    l7 = ttk.Combobox(root2,height=5,width=15,values=["Economy","Business","First"])
    l7.grid(row=1,column=6)'''

    def fun11():
        f = l1.get()
        t = l2.get()
        trip = l3.get()
        dd1 = l41.get()
        dd2 = l42.get()
        dd3 = l43.get()
        '''rd1 = l51.get()
        rd2 = l52.get()
        rd3 = l53.get()'''
        pa = l61.get()
        pc = l62.get()
        pi = l63.get()
        '''c = l7.get()'''
        if f=="" or t=="" or trip=="" or dd1=="" or dd2=="" or dd3=="" ''' or rd1=="" or rd2=="" or rd3=="" ''' or pa=="" or pc=="" or pi=="":
            messagebox.showerror("Error","Please fill all the fields")
        else:
            if f == t:
                messagebox.showerror("Error","Source and Destination cannot be same")
            else:
                '''if trip == "Round Trip" and (dd1+"/"+dd2+"/"+dd3 == rd1+"/"+rd2+"/"+rd3):
                    messagebox.showerror("Error","Departure and Return date cannot be same")
                elif trip == "Round Trip" and dd1+"/"+dd2+"/"+dd3 > rd1+"/"+rd2+"/"+rd3:
                    messagebox.showerror("Error","Departure date cannot be greater than Return date")'''
                '''else:'''

                    #algorithm for searching flight

                data = {
                    "origin":f,
                    "destination":t,
                    "date":dd3+"-"+dd2+"-"+dd1,
                    "adult":pa,
                    "child":pc,
                    "infant":pi,
                    }
                r = requests.get(url = API_ENDPOINT1, params=data)
                print('text= ', r.text)
                root2.destroy()
                root3=Tk()
                root3.title("Search Flight")
                Label(root3,text="Origin").grid(row=0,column=0)
                Label(root3,text="Destination").grid(row=0,column=1)
                Label(root3,text="Departure").grid(row=0,column=2)
                Label(root3,text="Arrival").grid(row=0,column=3)
                Label(root3,text="Economy").grid(row=0,column=5)
                Label(root3,text="Business").grid(row=0,column=6)
                Label(root3,text="First").grid(row=0,column=7)
                #print(r.json)
                result = r.json() 
                for n, itinerary in enumerate(result) :
                    first_flight = itinerary['flights'][0]
                    last_flight = itinerary['flights'][-1]

                    departure = first_flight['departure']
                    arrival = last_flight['arrival']
                    origin = first_flight['origin']
                    destination = last_flight['destination']
                    '''economy = itinerary[0]['fare']['economy']
                    business = itinerary[0]['fare']['business']
                    first = itinerary[0]['fare']['first']'''

                    Label(root3,text=origin).grid(row=n+1,column=0)
                    Label(root3,text=destination).grid(row=n+1,column=1)
                    Label(root3,text=departure).grid(row=n+1,column=2)
                    Label(root3,text=arrival).grid(row=n+1,column=3)
                    '''Label(root3,text=economy).grid(row=1,column=6)
                    Label(root3,text=business).grid(row=1,column=7)
                    Label(root3,text=first).grid(row=1,column=8)'''

                root3.mainloop()
            
    Bc=Button(root2,text="Search",bg='green',command=fun11).grid(row=4,column=2)
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

def fun7():
    root.destroy()
    root14=Tk()
    root14.geometry("500x500")
    root14.title("Passenger Details")
    Label(root14,text="Title").grid(row=0,column=0)
    chk1=BooleanVar()
    chk2=BooleanVar()
    chk3=BooleanVar()
    chk4=BooleanVar()
    chk5=BooleanVar()
    Checkbutton(root14,text="Mr.",variable=chk1).grid(row=1,column=0)
    Checkbutton(root14,text="Mrs.",variable=chk2).grid(row=1,column=1)
    Checkbutton(root14,text="Ms.",variable=chk3).grid(row=1,column=2)
    Label(root14,text="First Name").grid(row=2,column=0)
    l1=Entry(root14)
    l1.grid(row=3,column=0)
    Label(root14,text="Last Name").grid(row=2,column=1)
    l2=Entry(root14)
    l2.grid(row=3,column=1)
    Label(root14,text="Date of Birth (DD/MM/YYYY)").grid(row=4,column=0)
    l3=Entry(root14)
    l3.grid(row=5,column=0)
    l4 = ttk.Combobox(root14,height=5,width=15,values=["Thailand","India","China"])
    l4.insert(0,"Nationality")
    l4.grid(row=5,column=1)
    Label(root14,text="").grid(row=6,column=1)
    Checkbutton(root14,text="MALE",variable=chk4).grid(row=7,column=0)
    Checkbutton(root14,text="FEMALE",variable=chk5).grid(row=7,column=1)
    Label(root14,text="").grid(row=8,column=1)

    Label(root14,text="Passport details (Optional)").grid(row=9,column=0)
    l5=Entry(root14)
    l5.grid(row=10,column=0)
    Label(root14,text="Passport expiry date (Optional)").grid(row=9,column=1)
    l6=Entry(root14)
    l6.grid(row=10,column=1)
    Label(root14,text="Travel document (Optional)").grid(row=11,column=0)
    l7=ttk.Combobox(root14,height=5,width=15,values=["Passport","Green Card","Visa"])
    l7.insert(0,"Travel Document Type")
    l7.grid(row=12,column=0)
    Label(root14,text="Country of residence (Optional)").grid(row=11,column=1)
    l8=ttk.Combobox(root14,height=5,width=15,values=["Thailand","India","China"])
    l8.insert(0,"Select Country")
    l8.grid(row=12,column=1)
    Label(root14,text="").grid(row=13,column=1)
    Label(root14,text="Contact details").grid(row=15,column=0)
    l9=Entry(root14)
    l9.insert(0,"Phone number")
    l9.grid(row=16,column=0)
    l10=Entry(root14)
    l10.insert(0,"Email address")
    l10.grid(row=16,column=1)
    Label(root14,text="").grid(row=17,column=1)





    def fun71():
        fn = l1.get()
        ln = l2.get()
        dob = l3.get()
        nat = l4.get()
        pp = l5.get()
        ppe = l6.get()
        td = l7.get()
        cor = l8.get()
        pn = l9.get()
        ea = l10.get()
        mr = chk1.get()
        mrs = chk2.get()
        ms = chk3.get()
        m = chk4.get()
        f = chk5.get()

        if fn=="" or ln=="" or dob=="" or nat=="" or pn=="" or ea=="" or mr==False and mrs==False and ms==False or m==False and f==False:
            messagebox.showerror("Error","Please Fill All the Fields")
        else:
            
            root14.destroy()
            root15=Tk()
            root15.title("Passenger Details")

            #STORE THE DETAILS IN THE DATABASE (need to fix this)
            

            Label(root15,text="Passenger Details").pack()
            root15.mainloop()
        
    #PROCEED TO BOOKING (need to fix this)

    Bc=Button(root14,text="Start Booking",bg='green',command=fun71).grid(row=18,column=1)
    root14.mainloop()

B1=Button(root,text="Search Flight",command=fun1).pack()
B2=Button(root,text="Cancel Booking",command=fun2).pack()
B3=Button(root,text="Book Flight",command=fun3).pack()
B4=Button(root,text="View Booking",command=fun4).pack()
B5=Button(root,text="Passenger Details",command=fun7).pack()
B6=Button(root,text="Login",command=fun5).pack()
B7=Button(root,text="Register",command=fun6).pack()
B8=Button(root,text="Exit",command=root.destroy).pack()
root.mainloop()