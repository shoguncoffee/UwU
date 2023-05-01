import tkinter as tk
from tkinter import ttk

class FillPaymentDetailWindow:
    def __init__(self, master):
        self.master = master
        master.title("Fill payment details")

        self.label1 = tk.Label(master, 
                               text="Fill payment details"
                               )
        self.label1.grid(row=0, column=0) 
        self.payment_detail_lable = tk.Label(master, 
                                             text="Payable amount:"
                                             )
        self.payment_detail_lable.grid(row=1, column=0)
        self.method_label = tk.Label(master, 
                                          text="Payment Method:"
                                          )
        self.method_label.grid(row=2, column=0)
        self.method_combobox = ttk.Combobox(master,height=5,width=15,values=["Cradit card", "Master card"])
        self.method_combobox.grid(row=2, column=1)
        self.firstname_label = tk.Label(master, 
                                          text="Firstname:"
                                          )
        self.firstname_label.grid(row=4, column=0)
        self.firstname_entry = tk.Entry(master)
        self.firstname_entry.grid(row=4, column=1)
        self.lastname_label = tk.Label(master, 
                                          text="Lastname:"
                                          )
        self.lastname_label.grid(row=5, column=0)
        self.lastname_entry = tk.Entry(master)
        self.lastname_entry.grid(row=5, column=1)

        self.label2 = tk.Label(master, 
                               text=""
                               )
        self.label2.grid(row=6, column=1)

        self.card_number_label = tk.Label(master, 
                                          text="Card number:"
                                          )
        self.card_number_label.grid(row=7, column=0)
        self.card_number_entry = tk.Entry(master)
        self.card_number_entry.grid(row=7, column=1)
        self.expiration_date_label = tk.Label(master, 
                                          text="Expiration date(YYYY-MM-DD):"
                                          )
        self.expiration_date_label.grid(row=8, column=0)
        self.expiration_date_entry = tk.Entry(master)
        self.expiration_date_entry.grid(row=8, column=1)
        self.verification_label = tk.Label(master, 
                                          text="Verification number:"
                                          )
        self.verification_label.grid(row=9, column=0)
        self.verification_entry = tk.Entry(master)
        self.verification_entry.grid(row=9, column=1)

root = tk.Tk()
FillPaymentDetailWindow(root)
root.mainloop()