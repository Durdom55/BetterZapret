from tkinter import *
from tkinter import ttk
from tkinter import font
from pathlib import Path
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
import tkinter.filedialog
import os
import subprocess
import ctypes
import sys
import json
#---ПЕРЕМЕННЫЕ---
ZaOn = False
data={}
path = ""
pathList = ""
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
_listbut = PhotoImage(file="resources/button_sprite/List.png")
_listbutInv = PhotoImage(file = "resources/button_sprite/ListInv.png")
pathlisttext = StringVar()
   
#---ФУНКЦИИ---
def newWindow():
    global domain, SaveBut
    window = Toplevel()
    window.title("List-general")
    window.protocol("WM_DELETE_WINDOW", lambda: closeWindow(window))
    window.iconbitmap(default="BetZaicon.ico")
    window.geometry("600x500+650+200")
    window.resizable(False, False)
    
    fontEntry = font.Font(family="Consolas", size=10)
    fontHeader = font.Font(family="Segoe UI", size=18, weight="bold")
    fontText = font.Font(family='Consolas', size=12)
    
    header_frame=Frame(window, bg='#f0f2f5')
    header_frame.pack(side=TOP, fill=X, pady=20)
    
    body_frame=Frame(window, bg='#f0f2f5')
    body_frame.pack(side=TOP, fill=BOTH)
    
    Label(header_frame, text="Управление списком доменов", font=fontHeader).pack()
    PathAuto = ttk.Button(body_frame, text="Найти автоматически", command=AutoPathList)
    PathAuto.grid(row=1, column=1, ipadx=20, ipady=15, padx=[15, 0], pady=[10, 0])
    PathShow = ttk.Button(body_frame, text="Выбрать вручную", command=PathListCreate)
    PathShow.grid(row=2, column=1, ipadx=31, ipady=15, padx=[15, 0], pady=[10, 0],)
    PathEntry = Entry(body_frame, state="readonly", bg='white', font=fontEntry, textvariable=pathlisttext, fg='#333333', relief=SOLID, highlightthickness=0, bd=1)
    PathEntry.grid(row=1, column=0, ipadx=110, ipady=5, padx=[20, 0])
    SaveBut = ttk.Button(body_frame, text="Сохранить", command=SaveDomains, state=DISABLED)
    SaveBut.place(x=10, y=105)
    domain = ScrolledText(window, bg='white', fg='#333333', font=fontText, bd=1, relief=SOLID, highlightthickness=0, wrap='none')
    domain.place(height=260, width=580, x=10, y=230)
    domain.config(undo=True, maxundo=10)
    if pathList != "":
        pathlisttext.set(pathList)
        ListСhecker()
    else:
        pathlisttext.set("Путь к файлу не выбран...")
    domain.bind("<Control-z>", undoAction)
    
    window.grab_set()
    
def undoAction(event):
    try:
        domain.text.edit_undo()
    except Exception:
        pass

def SaveButOn():
    SaveBut.config(state=NORMAL)

def SaveDomains():
    domains = domain.get('1.0', 'end')
    with open(pathList, "w") as f:
        f.write(domains)
    
def readPath():
    global path, pathList
    with open("Paths.json", "r") as f:
        data = json.load(f)
        path = data['BatPath']
        pathList = data['ListPath']
        
def writePath():
    with open("Paths.json", "w") as f:
        data["BatPath"] = path
        data['ListPath'] = pathList
        json.dump(data, f, indent=4)
    
def ZaonBg():
    global ZaOn
    ZaOn = True
    but.config(image=butOn_i, bg="#f8f8f8", activebackground ="#f8f8f8")
    pathbut.config(bg="#f8f8f8", activebackground="#f8f8f8")
    listbut.config(bg="#f8f8f8", activebackground="#f8f8f8", image=_listbut)
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
    listbut.config(bg="#070707", activebackground="#070707", image=_listbutInv)
    if path == "":
        pathbut.config(image=PathFlInv)
    else:
        pathbut.config(image=PathTrInv)
    bg.config(image=Bg1)
    
def ZapretMode():
    if path != "":      
        if ZaOn == False:
            Zaon()
        else:
            Zaoff()
    else:
        tkinter.messagebox.showwarning(message="Для корректной работы программы нужно выбрать стратегию (.bat файл).\nПожалуйста, кликните на Мяво (кошка в левом углу), чтобы выбрать нужную стратегию (.bat файл)")
    
def PathNull():
    global path
    path = ""   
    
def PathListNull():
    global pathList
    pathList = ""       
        
def Zaon():
    try:
        os.startfile(path)
        ZaonBg()
    except:
        tkinter.messagebox.showwarning(message="Ошибка при открытии bat-файла")
    # print("Zapret vkluchen")
    
def Zaoff():
    ZaoffBg()
    os.system("taskkill /im winws.exe")
    os.system("sc stop windivert")
    #print("Zapret viklichen")
    
def PathCreate():
    global path
    path = tkinter.filedialog.askopenfilename() 
    if path != "" and path.endswith(".bat"):
        if ZaOn == False:
            pathbut.config(image=PathTrInv)
        else:
            pathbut.config(image=PathTr)
        writePath()
    elif path != "" and not path.endswith(".bat"):
        tkinter.messagebox.showwarning(message="Это не .bat файл!")
        try:
            PathNull()
            readPath()
        except:
            PathNull()
    else:
        try:
            PathNull()
            readPath()
        except:
            PathNull()
        #print("error")

def PathListCreate():
    global pathList
    pathList = tkinter.filedialog.askopenfilename() 
    if pathList != "" and pathList.endswith(".txt"):
        pathlisttext.set(pathList)
        writePath()
        ListСhecker()
    elif pathList != "" and not pathList.endswith(".txt"):
        tkinter.messagebox.showwarning(message="Это не .txt файл!")
        try:
            PathListNull()
            readPath()
            ListСhecker()
        except:
            PathListNull()
    else:
        try:
            PathListNull()
            readPath()
            ListСhecker()
        except:
            PathListNull()
        #print("error")
        
def AutoPathList():
    global path, pathList
    if path != "":
        zapret_dir = Path(path).parent
        target_file = "list-general.txt"
        found_path = None
        for root, _, files in os.walk(zapret_dir):
            if target_file in files:
                found_path = Path(root) / target_file
                break
        if found_path:
            pathlisttext.set(found_path)
            pathList = str(found_path)
            writePath()
            ListСhecker()
        else:
            tkinter.messagebox.showerror(message="Не удалось найти list-general.\nВыберите путь к файлу вручную")
    else:
        tkinter.messagebox.showerror(message="Сначала выберите стратегию (.bat-файл)")

def ListСhecker():
    SaveButOn()
    domain.config(undo=False)
    with open(pathList, 'r') as f:
        for line in f:
            domain.insert('1.0', f'\n{line.strip()}')
    domain.edit_modified(False)
    domain.config(undo=True)
        
            
def closeWindow(window):
    window.grab_release()
    window.destroy()
        
#---FRAME 1---
frame1 = Frame(app)
bg = Label(frame1, image=Bg1)
bg.place(x=0, y=0, relwidth=1, relheight=1)
frame1.pack(fill=BOTH, expand=True)
but = Button(frame1, bg="#070707", activebackground ="#070707", image=butOff_i, relief=FLAT, bd=0, command=ZapretMode)
but.place(x=129)
pathbut = Button(frame1, relief=FLAT, bd=0, image=PathFlInv, activebackground="#070707", bg="#070707", width=62, height=36, command=PathCreate)
pathbut.place(x=1, y=1)
listbut = Button(frame1, relief=FLAT, bd=0, image=_listbutInv, activebackground="#070707", bg="#070707", width=60, height=62, command=newWindow)
listbut.place(x=1,y=55)

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
    #print("Закрыл")
    sys.exit(1)
else:
    pass
ZapretRun = subprocess.run("sc qc windivert", shell=True)
if ZapretRun.returncode == 0:
    ZaonBg()
    #print("zapret vkl")
    
try:
    readPath()
    if ZaOn == False:
        pathbut.config(image=PathTrInv)
    else:
        pathbut.config(image=PathTr)  
except FileNotFoundError:
    tkinter.messagebox.showwarning(message="Для корректной работы программы нужно выбрать стратегию (.bat файл).\nПожалуйста, кликните на Мяво (кошка в левом углу), чтобы выбрать нужную стратегию (.bat файл)")

app.mainloop()