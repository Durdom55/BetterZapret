from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os
import subprocess
import ctypes
import sys
#---ПЕРЕМЕННЫЕ---
ZaOn = False
path = ""
#---ВИЗУАЛ---
app = Tk()
app.title("BetterZapret")
app.iconbitmap(default="BetZaicon.ico")
app.geometry("300x500+800+200")
app.resizable(False, False)
butOn_i = PhotoImage(file="resources/button_sprite/ButtonOn.png")
butOff_i = PhotoImage(file="resources/button_sprite/ButtonOff.png")
Bg1 = PhotoImage(file="resources/Background/BG1.png")
Bg2 = PhotoImage(file="resources/Background/BG2.png")
PathTr = PhotoImage(file="resources/button_sprite/MewoTrue.png")
PathTrInv = PhotoImage(file="resources/button_sprite/MewoTrueInv.png")
PathFl = PhotoImage(file="resources/button_sprite/MewoFalse.png")
PathFlInv = PhotoImage(file="resources/button_sprite/MewoFalseInv.png")

def ZaonBg():
    global ZaOn
    ZaOn = True
    but.config(image=butOn_i, bg="#f8f8f8", activebackground ="#f8f8f8")
    pathbut.config(bg="#f8f8f8", activebackground="#f8f8f8")
    if path == "":
        pathbut.config(image=PathFl)
    else:
        pathbut.config(image=PathTr)
    bg.config(image=Bg2)
    
def ZaoffBg():
    global ZaOn
    ZaOn = False
    but.config(image=butOff_i, bg="#070707", activebackground ="#070707")
    pathbut.config(bg="#070707", activebackground="#070707")
    if path == "":
        pathbut.config(image=PathFlInv)
    else:
        pathbut.config(image=PathTrInv)
    bg.config(image=Bg1)
    
#---ФУНКЦИИ---
def ZapretMode():
    if path != "":      
        if ZaOn == False:
            Zaon()
        else:
            Zaoff()
    else:
        tkinter.messagebox.showwarning(message="Для корректной работы программы нужно выбрать стратегию (.bat файл).\nПожалуйста, кликните на Мяво (кошка в левом углу), чтобы выбрать нужную стратегию (.bat файл)")
        
def Zaon():
    ZaonBg()
    os.startfile(path)
    print("Zapret vkluchen")
    
def Zaoff():
    ZaoffBg()
    os.system("taskkill /im winws.exe")
    os.system("sc stop windivert")
    print("Zapret viklichen")
    
def PathCreate():
    global path
    path = tkinter.filedialog.askopenfilename() 
    if path != "" and path.endswith(".bat"):
        if ZaOn == False:
            pathbut.config(image=PathTrInv)
        else:
            pathbut.config(image=PathTr)
        with open("batchange.txt", "w") as f:
            f.write(path)
    elif path != "" and not path.endswith(".bat"):
        tkinter.messagebox.showwarning(message="Это не .bat файл!")
        try:
            path = ""
            with open("batchange.txt", "r") as f:
                path = f.read()
        except:
            path = ""
    else:
        try:
            path = ""
            with open("batchange.txt", "r") as f:
                path = f.read()
        except:
            path = ""
        print("error")
        
#---FRAME 1---
frame1 = Frame(app)
bg = Label(frame1, image=Bg1)
bg.place(x=0, y=0, relwidth=1, relheight=1)
frame1.pack(fill=BOTH, expand=True)
but = Button(frame1, bg="#070707", activebackground ="#070707", image=butOff_i, relief=FLAT, bd=0, command=ZapretMode)
but.place(x=129)
pathbut = Button(frame1, relief=FLAT, bd=0, image=PathFl, activebackground="#070707", bg="#070707", width=62, height=36, command=PathCreate)
pathbut.place(x=1, y=1)

#---ХОД ПРОГРАММЫ---
def isadmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if isadmin() == False:
    tkinter.messagebox.showerror(message="Программа запущена не от имени администратора")
    sys.exit(1)
else:
    pass
ProgCheck = subprocess.run("tasklist", shell=True, text=True, capture_output=True)
ProgCheckCount = ProgCheck.stdout.count("BetterZapret")
if ProgCheckCount > 1:
    print("Закрыл")
    sys.exit(1)
else:
    pass
ZapretRun = subprocess.run("sc qc windivert", shell=True)
if ZapretRun.returncode == 0:
    ZaonBg()
    print("zapret vkl")
else:
    print("zapret vikl")
    
try:
    with open("batchange.txt", "r") as f:
        path = f.read()
        if ZaOn == False:
            pathbut.config(image=PathTrInv)
        else:
            pathbut.config(image=PathTr)  
except FileNotFoundError:
    tkinter.messagebox.showwarning(message="Для корректной работы программы нужно выбрать стратегию (.bat файл).\nПожалуйста, кликните на Мяво (кошка в левом углу), чтобы выбрать нужную стратегию (.bat файл)")

app.mainloop()