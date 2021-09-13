import pandas as pd
import tkinter as tk
from time import sleep


class UserInterface:
    def __init__(self, master, dataset):
        myFrame = tk.Frame(master)
        myFrame.pack()
        self.master = master
        self.symbol = None
        
        self.my_button = tk.Button(self.master, text="Select Symbol")
        self.my_button.pack(side = 'bottom')
        self.my_button.bind("<Button-1>", self.print_val)
        
        self.my_label = tk.Label(self.master, text="Select a symbol ... [Symbol || Name]", 
                            font=("Helvetica", 14), fg="grey")
        self.my_label.pack(pady=20)
        
        self.my_entry = tk.Entry(self.master, font=("Helvetica", 20))
        self.my_entry.pack()
        
        self.my_list = tk.Listbox(self.master, width=50)
        self.my_list.pack(pady=40)
        
        self.dataset = dataset
        self.update(self.dataset)
        
        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def update(self, data):
        self.my_list.delete(0, tk.END)
        for item in data:
            self.my_list.insert(tk.END, item)

    def fillout(self, e):
        self.my_entry.delete(0, tk.END)
        self.my_entry.insert(0, self.my_list.get(tk.ANCHOR))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == '':
            data = self.dataset
        else:
            data = []
            for item in self.dataset:
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)

    def print_val(self, a):
        pname = self.my_entry.get()
        self.my_label.config(text = "{} - Done".format(self.my_entry.get()))
        self.symbol = self.my_entry.get()
        self.exit_window()
        
    def get_symbol_value(self):
        return self.symbol
    
    def exit_window(self):
        self.master.destroy()
        

    