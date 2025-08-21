import tkinter
import customtkinter
from customtkinter import *


class App:
    def __init__(self,root):
        self.root=root
        self.root.title("TKRAISE")
        self.root.geometry("600x400")
        self.container=CTkFrame(self.root).pack()

        self.page1=CTkFrame(master=self.container)
        self.page1.pack()
        self.page1=CTkLabel(master=self.page1,text="Page1",bg_color="red")
        self.page1.place(x=200,y=200)

        self.page2=CTkFrame(master=self.container,bg_color="red")
        self.page2.pack()
        self.page2=CTkLabel(master=self.page2,text="Page1",bg_color="red")
        self.page2.place(x=200,y=250)

        button=CTkButton(master=self.container,bg_color="green",corner_radius=5,text="Changer de page",command=self.show_pages(self.page1))
        button.pack()

     
    def show_pages(self,page):
        pass
        # page=self.pages[page]
        # page.tkraise()
    
if __name__=="__main__":
    root=CTk()
    App(root)
    root.mainloop()
