from tkinter import ttk
from tkinter import *
from customtkinter import *

import ipaddress
import webbrowser
import sqlite3
import bcrypt
import os
from PIL import ImageTk, Image
import customtkinter as ctk

### GROUPE 5 
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("green")  

set_appearance_mode("dark") 
set_default_color_theme("green")

APP_COUNT = 3

PAD_X = 30
PAD_Y = 30

SIZE_X = 1000
SIZE_Y = 560

FRAME_CORNER_RADIUS = 25

CENTER_WINDOW = SIZE_X / 2
FRAME_SIZE_X = SIZE_X - 2 * PAD_X
CONNECTION_FRAME_SIZE_X = (SIZE_X - 3 * PAD_X) / 5 * 2
SIGNUP_FRAME_SIZE_X = CONNECTION_FRAME_SIZE_X * 1.5
FRAME_SIZE_Y = SIZE_Y - 5 * PAD_Y

TITLE_PLACEMENT_Y = PAD_Y

CONNECTION_FRAME_CENTER = CONNECTION_FRAME_SIZE_X / 2
SIGNUP_FRAME_CENTER = SIGNUP_FRAME_SIZE_X / 2

FRAME_Y_ORIGIN = 3 * PAD_Y
FRAME_BUTTON_Y = FRAME_SIZE_Y - PAD_Y

APPFRAME_SIZE_X = (SIZE_X - (APP_COUNT + 1) * PAD_X) / APP_COUNT
APPFRAME_CENTER = APPFRAME_SIZE_X / 2

APPFRAME_DESC_LABEL_Y = FRAME_SIZE_Y - 3 * PAD_Y

INPUTFRAME_SIZE_X = (SIZE_X - 3 * PAD_X) / 4 * 1.5
TITLE_OUTPUT_SIZE_X = SIZE_X - 3 * PAD_X - INPUTFRAME_SIZE_X 

TITLE_FRAME_SIZE_Y = 120
OUTPUT_FRAME_SIZE_Y = SIZE_Y - 4 * PAD_Y - TITLE_FRAME_SIZE_Y

INPUTFRAME_CENTER = INPUTFRAME_SIZE_X / 2








# Gestion du statut de connexion
isConnected = False

def getConnected():
    global isConnected
    return isConnected

def setConnected():
    global isConnected
    isConnected = True
    app.returnButton.config(state= NORMAL, cursor="hand2")
    app.disconnectButton.config(state= NORMAL, cursor="hand2", command=setDisconnected)
    app.show_frame(HomePage)

def setDisconnected():
    global isConnected
    isConnected = False
    app.returnButton.config(state= DISABLED, cursor="tcross")
    app.disconnectButton.config(state= DISABLED, cursor="tcross")
    app.show_frame(Connexion)

# Check Inputs - Allow only Digits or "."
def verifCaracter(P):
    if str.isdigit(P) or P == "" or P == ".":
        return True
    else:
        return False


# ROOT
class MainApplication(Tk):
    """
    Main Application Class - Root
    """ 

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry(f"{SIZE_X}x{SIZE_Y}")
        self.title("Réseau - Vérificateur d'IP")
        self.resizable(False, False)
         
        # creating a container
        container = CTkFrame(self, cursor="tcross") 
        container.pack(anchor=CENTER, fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        quitButton = Button(self, text="Quitter l'application", command=self.destroy, cursor="hand2").place(x=SIZE_X-125, y=SIZE_Y-35)
        githubButton = Button(self, text="GitHub", command=self.ouvrir_github, cursor="hand2").place(x=SIZE_X-125-55, y=SIZE_Y-35)

        self.disconnectButton = Button(self, text="Se Déconnecter", cursor="hand2")
        self.disconnectButton.config(state= DISABLED, cursor="tcross")
        self.disconnectButton.place(x=130, y=SIZE_Y-35)

        self.returnButton = Button(self, text="Retourner au menu", command=lambda : self.show_frame(HomePage))
        self.returnButton.config(state= DISABLED, cursor="tcross")
        self.returnButton.place(x=10, y=SIZE_Y-35)

        self.frames = {} 
        for F in (Connexion, HomePage, Application1, Application2, Application3):
  
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Connexion)
  
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        if (getConnected()):
            frame = self.frames[cont]
            frame.reset()
            frame.tkraise()
        else:
            frame = self.frames[Connexion]
            frame.reset()
            frame.tkraise()

    def ouvrir_github(self):
        webbrowser.open("https://github.com/DrimoZ/projectIpCalculator")
        
# Page d'acceuil
class HomePage(CTkFrame):
    """
    - Les IP et masques invalides seront automatiquement refusés par le 
    système
    - Un menu (ou des boutons) permettant de choisir parmi les différentes 
    fonctionnalités sera proposé à l’utilisateur
    - Une interface graphique est souhaitée mais pas obligatoire (un bonus sera 
    attribué aux projets présentant une interface graphique)
    - L’accès au programme sera sécurisé par un mot de passe correctement 
    géré. Les projets qui gèreront les mots de passe via enregistrement dans 
    une base de données (module sqlite3 pour Python) bénéficieront d’un 
    bonus
    """

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        #Titre du Programme
        CTkLabel(self, text="Réseau - Ip : Vérificateur d'Ip - 2023/2024", font=CTkFont("Times", 29, "bold", underline=True)).place(y=TITLE_PLACEMENT_Y, x=CENTER_WINDOW, anchor="center")

        #3 applications
        list = [
            ["Application 1", "IPFinder.png", "Trouve les informations nécessaires par rapport\nà une ip donnée et un masque (facultatif)."],
            ["Application 2", "computer-network.png", "Vérifie si une ip est dans un réseau \n(ou dans un sous-réseau si découpe)."],
            ["Application 3", "decoupe.png", "Crée une découpe de sous-réseau\nen fonction des paramètres données."],
        ]

        for i in range(0, len(list)):
            #Frame par application
            appFrame = CTkFrame(self, width=APPFRAME_SIZE_X, height=FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)

            #Creation de l'image
            current_dir = os.path.dirname(os.path.abspath(__file__))
            img = Image.open(os.path.join(current_dir, "Image", list[i][1]))
            # Cree une image Tkinter a partir de l'image PIL
            img_tk = CTkImage(img,size=(250, 250))
            # Montre l'image dans un label
            self.appImglabel = CTkLabel(appFrame,image=img_tk,width=250,height=250,text="")

            # Label de description de l'application
            appDescLabel = CTkLabel(appFrame, text=list[i][2], text_color="gray", justify="center")

            # Bouton d'accès à l'application
            appButton = CTkButton(appFrame, text=list[i][0],fg_color=("Black"))

            # Définition des commandes des boutons
            if (i == 0):
                appButton.configure(command = lambda : controller.show_frame(Application1))
            elif (i == 1):
                appButton.configure(command = lambda : controller.show_frame(Application2))
            elif (i == 2):
                appButton.configure(command = lambda : controller.show_frame(Application3))

            # Placement des éléments
            appButton.place(x=APPFRAME_CENTER, y=FRAME_BUTTON_Y, anchor="center")
            appButton.bind("<Double 3>", lambda eff: Palergun())

            self.appImglabel.place(x=APPFRAME_CENTER, y=140, anchor="center")
            appDescLabel.place(x=APPFRAME_CENTER, y=APPFRAME_DESC_LABEL_Y, anchor="center")

            appFrame.place(y=FRAME_Y_ORIGIN, x= PAD_X + i * (PAD_X + APPFRAME_SIZE_X))


        def Palergun():
            current_dir = os.path.dirname(os.path.abspath(__file__))
            img = Image.open(os.path.join(current_dir, "Image", "Palergun.png"))
            img_tk = CTkImage(img,size=(250, 250))
            self.appImglabel.configure(image=img_tk)
            return
        
    def reset(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img = Image.open(os.path.join(current_dir, "Image", "decoupe.png"))
        img_tk = CTkImage(img,size=(250, 250))
        self.appImglabel.configure(image=img_tk)
        return
        

class Application1(CTkFrame):
    """
    En classfull uniquement, sur base d’une adresse IP et d’un masque, le 
    programme doit fournir l’adresse de réseau et l’adresse de broadcast du 
    réseau. Si une découpe en sous-réseau est réalisée, le programme doit 
    déterminer l’adresse de SR
    """

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        #Declaraction des Frames
        self.app1InputFrame = CTkFrame(self, width=INPUTFRAME_SIZE_X, height=FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)
        self.app1OutputFrame = CTkFrame(self, width=TITLE_OUTPUT_SIZE_X, height=OUTPUT_FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)
        app1TitleFrame = CTkFrame(self, width=TITLE_OUTPUT_SIZE_X, height=TITLE_FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)


        # Titre
        lblTitre = CTkLabel(app1TitleFrame, text="Application 1 : Déterminer le Réseau", font = CTkFont("Times", 21, underline=True))
        lblTitre.place(x=12, y=10)
        app1Description = "Sur base d’une IP et d’un masque (facultatif), fournit l’adresse de réseau\net le broadcast du réseau. Si une découpe en sous-réseau est réalisée,\ndétermine l’adresse du sous-réseau."
        lblExo = CTkLabel(app1TitleFrame, text_color='cyan', text=app1Description, font = CTkFont("Times", 17, slant="italic"), justify="left" )
        lblExo.place(x=10, y=40)


        # Inputs
        vcmd = (self.register(verifCaracter))

        labIntro = CTkLabel(self.app1InputFrame, text="Entrer les informations\nrequises pour l'application", text_color="gray")
        labIntro.place(y=30, x=INPUTFRAME_CENTER, anchor="center")

        labIp = CTkLabel(self.app1InputFrame, text="Adresse Ip")
        labIp.place(y=90, x=INPUTFRAME_CENTER, anchor="center")

        self.app1EntryIp = CTkEntry(self.app1InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'))
        self.app1EntryIp.place(y=120, x=INPUTFRAME_CENTER, anchor="center")
        self.app1EntryIp.bind("<Key>", self.checkEntries)

        self.labMask = CTkLabel(self.app1InputFrame, text="Masque de réseau")

        self.app1EntryMask = CTkEntry(self.app1InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'))
        self.app1EntryMask.bind("<Key>", self.checkEntries)

        # Choix d'ajouter un masque ou non
        self.hasCustomMask = StringVar()
        self.hasCustomMask.set("off")

        def checkbox_event():
            if (self.hasCustomMask.get() == "on"):
                self.labMask.place(y=200, x=INPUTFRAME_CENTER, anchor="center")
                self.app1EntryMask.place(y=230, x=INPUTFRAME_CENTER, anchor="center")
            else:
                self.labMask.place_forget()
                self.app1EntryMask.place_forget()

        checkbox = CTkCheckBox(self.app1InputFrame, text="Découpe en sous-réseaux ?", command=checkbox_event, variable=self.hasCustomMask, onvalue="on", offvalue="off")
        checkbox.place(y=160, x=INPUTFRAME_CENTER, anchor="center")
        checkbox.bind("<Button-1>", self.checkEntries)
        
        self.app1BtnCheck = CTkButton(self.app1InputFrame, text="Trouver le réseaux", cursor="hand2", command= lambda: self.trouverReseau(), state=DISABLED)
        self.app1BtnCheck.place(y=FRAME_BUTTON_Y - PAD_Y, x=INPUTFRAME_CENTER, anchor="center")

        self.app1strErr = StringVar()
        self.app1strErr.set("")
        
        labErr = CTkLabel(self.app1InputFrame, textvariable=self.app1strErr, text_color="red")
        labErr.place(y=FRAME_SIZE_Y - 3*PAD_Y, x=INPUTFRAME_CENTER, anchor="center")

        # Frame d'output
        self.app1StrOutIp = StringVar()
        self.app1StrOutIp.set("")
        self.app1StrOutMask = StringVar()
        self.app1StrOutMask.set("")
        self.app1StrOutRes = StringVar()
        self.app1StrOutRes.set("")
        self.app1StrOutBrd = StringVar()
        self.app1StrOutBrd.set("")
        self.app1StrOutSR = StringVar()
        self.app1StrOutSR.set("")

        labOutIp = CTkLabel(self.app1OutputFrame, text="Adresse IP : ")
        labOutIp.place(y=30, x=TITLE_OUTPUT_SIZE_X/2 - 120, anchor="w")

        self.app1LblOutRes = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutIp, text_color="green", justify="left")
        self.app1LblOutRes.place(y=30, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutMask = CTkLabel(self.app1OutputFrame, text="Masque de réseau : ")
        labOutMask.place(y=60, x=TITLE_OUTPUT_SIZE_X/2 - 120, anchor="w")

        self.app1LblOutMask = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutMask, text_color="green", justify="left")
        self.app1LblOutMask.place(y=60, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutRes = CTkLabel(self.app1OutputFrame, text="Adresse de réseau : ")
        labOutRes.place(y=90, x=TITLE_OUTPUT_SIZE_X/2 - 120, anchor="w")

        self.app1LblOutRes = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutRes, text_color="green", justify="left")
        self.app1LblOutRes.place(y=90, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutBrd = CTkLabel(self.app1OutputFrame, text="Adresse de broadcast : ")
        labOutBrd.place(y=120, x=TITLE_OUTPUT_SIZE_X/2 - 120, anchor="w")

        self.app1LblOutBrd = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutBrd, text_color="green", justify="left")
        self.app1LblOutBrd.place(y=120, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutSr = CTkLabel(self.app1OutputFrame, text="Adresse de sous-réseau : ")
        labOutSr.place(y=150, x=TITLE_OUTPUT_SIZE_X/2 - 120, anchor="w")

        self.app1LblOutSr = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutSR, text_color="green", justify="left")
        self.app1LblOutSr.place(y=150, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")


        #Placement des frames
        self.app1InputFrame.place(x = PAD_X, y = PAD_Y)
        app1TitleFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = PAD_Y)

    def checkEntries(self, event):
        if (self.hasCustomMask.get() == "off"):
            self.app1EntryMask.delete(0, END)
        if (self.app1EntryIp.get() == ""):
            self.app1BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app1strErr.set("(*) Champ requis : IP")
        elif (self.hasCustomMask.get() == "on" and self.app1EntryMask.get() == ""):
            self.app1BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app1strErr.set("(*) Champ requis : Masque de réseau")
        else:
            self.app1BtnCheck.configure(state=NORMAL, cursor="hand2")
            self.app1strErr.set("")

    def trouverReseau(self) -> None :
        """
        Récupere Ip, Masque. Défini le réseau et le broadcast. Défini le sous-réseau si besoin.
        """

        self.app1strErr.set("")
        self.app1OutputFrame.place_forget()

        # Un des champs est vide
        if (self.app1EntryIp.get() == ""):
            self.app1strErr.set("(*) Champ requis : IP")
            return
        elif (self.hasCustomMask.get() == "on" and self.app1EntryMask.get() == ""):
            self.app1strErr.set("(*) Champ requis : Masque de réseau")
            return
        
        
        # Instance de Reseau
        res = Reseau(self.app1EntryIp.get(), self.app1EntryMask.get())

        # Vérification des champs
        if (res.ip == "0.0.0.0"):
            self.app1strErr.set("Adresse IP non-valide")
        elif (res.masque == "0.0.0.0" and self.app1EntryMask.get() != ""):
            self.app1strErr.set("Masque Réseau non-valide")
        else:
            self.app1StrOutIp.set(res.ip)
            self.app1StrOutMask.set(res.masque)
            self.app1StrOutRes.set(res.adrReseau)
            self.app1StrOutBrd.set(res.adrBroadcast)

            self.app1OutputFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = 2*PAD_Y + TITLE_FRAME_SIZE_Y)


    # Fonction de reset de la frame
    def reset(self) -> None:
        self.app1BtnCheck.configure(state=DISABLED, cursor="tcross")
        self.hasCustomMask.set("off")
        self.app1EntryMask.delete(0, END)
        self.app1EntryIp.delete(0, END)
        self.labMask.place_forget()
        self.app1EntryMask.place_forget()
        self.app1OutputFrame.place_forget()
        self.app1strErr.set("")
        

class Application2(CTkFrame):
    """
    Sur base d’une adresse IP et de son masque et d’une adresse de réseau, le 
    programme doit déterminer si l’IP appartient au réseau ou pas. CLASSFULL
    """

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        # Frame - Données d'entrée
        self.infoFrame = CTkFrame(master=self, width=270, height=210)
        self.infoFrame.grid_propagate(0)

        # Labels - Données d'entrée
        labIp = Label(self.infoFrame, text="Adresse IP * : ", width=15).grid(row = 1, column = 0, padx = 10, pady = 10)
        labMasque = Label(self.infoFrame, text="Masque SR : ", width=15).grid(row = 2, column = 0, padx = 10, pady = 10)
        labReseau = Label(self.infoFrame, text="Adresse Réseau * : ", width=15).grid(row = 3, column = 0, padx = 10, pady = 10)

        # Entries - Données d'entrée
        vcmd = (self.register(self.verifCaracter))
        self.textIp = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textIp.grid(row = 1, column = 1, pady = 10)
        self.textMasque = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textMasque.grid(row = 2, column = 1, pady = 10)
        self.textReseau = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textReseau.grid(row = 3, column = 1, pady = 10)

        # Errors - Données d'entrée
        self.attStr = StringVar()
        self.attStr.set("")
        lblVerif = Label(self.infoFrame, textvariable=self.attStr, justify="center", fg="red")
        lblVerif.grid(row = 4, column = 0, columnspan=2, padx = 10, pady = 10)

        # Buttons - Données d'entrée
        btnCheck = Button(self.infoFrame, text="Verifier l'adresse Ip", cursor="hand2")
        btnCheck.config(command= lambda: self.checkReseau())
        btnCheck.grid(row = 5, column = 0, columnspan=2, padx = 10, pady = 10)

        # Fin de la Frame d'entrée
        self.infoFrame.place(x=30, y=30)


        # Frame - Titre
        titleFrame = CTkFrame(self, width=SIZE_X-360, height=90)
        titleFrame.grid_propagate(0)
        titleFrame.place(x=330, y=30)

        # Labels - Titre
        lblTitre = Label(titleFrame, text="Application 2 : Présence d'une IP dans le réseau", font = 'Times 14 underline' )
        lblTitre.place(x=10, y=10)
        lblExo = Label(titleFrame, fg='blue', text="Sur base d’une IP, d’une adresse de réseau (et d'un masque si découpé en sous-réseau),\nvérifie si l’adresse IP donnée appartient au réseau ou pas. ", font = 'Times 11 italic', justify="left" )
        lblExo.place(x=10, y=40)


        # Frame - Réponses
        self.repFrame = CTkFrame(master=self, width=SIZE_X-360, height=300)
        self.repFrame.grid_propagate(0)

        # Labels - Titre
        self.rep = StringVar()
        self.rep.set("OUI")
        lblVerif = Label(self.repFrame, textvariable=self.rep, justify="center", fg="red")
        lblVerif.place(x=0, y=0)


    def checkReseau(self) -> None :
        """
        Récupere Ip, Masque et Réseau entrés. Vérifie que tout soit valide. Explique si l'Ip fait partie du Réseau donné. 
        """

        self.attStr.set("")
        self.repFrame.place_forget()

        # Un des champs est vide
        if (self.textIp.get() == "" or self.textReseau.get() == ""):
            self.attStr.set("(*) Champs requis : " + ("IP" if self.textIp.get() == "" else "") + (" et " if self.textIp.get() == "" and self.textReseau.get() == "" else "") + ("Adresse de réseau" if self.textReseau.get() == "" else ""))
            return
        
        # Instance de Reseau
        res = Reseau(self.textIp.get(), self.textMasque.get(), self.textReseau.get())

        # Vérification des champs
        if (res.ip == "0.0.0.0"):
            self.attStr.set("Adresse IP non-valide")
        elif (res.masque == "0.0.0.0" and self.textMasque.get() != ""):
            self.attStr.set("Masque Réseau non-valide")
        elif (res.adrReseau == "0.0.0.0"):
            self.attStr.set("Adresse Réseau non-valide")
        elif (res.adrReseau == "-1"):
            self.rep.set("Pas dans le même réseau")
            self.repFrame.place(x=330, y=150)
        else:
            net = ipaddress.IPv4Network(res.ip + '/' + res.masque, False)
            # self.rep.set("Adresse IP  : "+res.ip+"\nMasque de réseau : "+res.masque+"\nAdresse de réseau : "+f'{net.network_address:s}'+"\nAdresse de broadcast : "+f'{net.broadcast_address:s}')
            self.rep.set("L'adresse IP appartient bien au même réseau")
            self.repFrame.place(x=330, y=150)
        
    def verifCaracter(self, P):
        if str.isdigit(P) or P == "" or P == ".":
            return True
        else:
            return False
        
    # Fonction de reset de la frame
    def reset(self) -> None:
        self.attStr.set("")
        self.textIp.delete(0, END)
        self.textMasque.delete(0, END)
        self.textReseau.delete(0, END)
        self.repFrame.place_forget()


class Application3(CTkFrame):
    """
    Sur base de la description d’un réseau (nombre de SR, nombre d’hôtes 
    dans chacun d’entre eux, IP et masque de départ), le programme doit 
    déterminer 
    - Le nombre d’hôtes total qu’il sera possible d’adresser avec l’IP et le 
    masque de départ
    - Déterminer s’il sera possible ou pas de réaliser une découpe 
    classique sur base du nombre de SR. Si la réponse est oui, le 
    programme devra fournir le plan d’adressage complet de la 
    découpe demandée. Il devra également indiquer combien de SR on 
    peut avoir au maximum dans cette découpe
    - Déterminer s’il sera possible ou pas de réaliser une découpe 
    classique sur base du nombre d’IP par SR. Si la réponse est oui, le 
    programme devra fournir le plan d’adressage complet de la 
    découpe demandée. Il devra également indiquer combien d’IPs on 
    peut avoir au maximum dans cette découpe dans chaque SR pour 
    cette découpe
    """
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        # Frame - Données d'entrée
        self.infoFrame = CTkFrame(self,width=270, height=250)
        self.infoFrame.grid_propagate(0)

        # Labels - Données d'entrée
        labReseau = Label(self.infoFrame, text="Adresse Réseau * : ", width=15).grid(row = 1, column = 0, padx = 10, pady = 10)
        labMasque = Label(self.infoFrame, text="Masque SR : ", width=15).grid(row = 2, column = 0, padx = 10, pady = 10)
        labSR = Label(self.infoFrame, text="SR souhaités * : ", width=15).grid(row = 3, column = 0, padx = 10, pady = 10)
        labHotes = Label(self.infoFrame, text="Hôtes par SR * : ", width=15).grid(row = 4, column = 0, padx = 10, pady = 10)

        
        
        # Entries - Données d'entrée
        vcmd = (self.register(self.verifCaracter))
        self.textReseau = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textReseau.grid(row = 1, column = 1, pady = 10)
        self.textMasque = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textMasque.grid(row = 2, column = 1, pady = 10)
        self.textSR = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textSR.grid(row = 3, column = 1, pady = 10)
        self.textHotes = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textHotes.grid(row = 4, column = 1, pady = 10)

        # Errors - Données d'entrée
        self.attStr = StringVar()
        self.attStr.set("")
        lblVerif = Label(self.infoFrame, textvariable=self.attStr, justify="center", fg="red")
        lblVerif.grid(row = 5, column = 0, columnspan=2, padx = 10, pady = 10)

        # Buttons - Données d'entrée
        btnCheck = Button(self.infoFrame, text="Créer les sous-réseaux", cursor="hand2")
        btnCheck.config(command= lambda: self.createSR())
        btnCheck.grid(row = 6, column = 0, columnspan=2, padx = 10, pady = 10)

        # Fin de la Frame d'entrée
        self.infoFrame.place(x=30, y=30)

        # Frame - Titre
        titleFrame = CTkFrame(self, width=SIZE_X-360, height=90)
        titleFrame.grid_propagate(0)
        titleFrame.place(x=330, y=30)

        # Labels - Titre
        lblTitre = Label(titleFrame, text="Application 3 : Création de Sous-Réseaux", font = 'Times 14 underline' )
        lblTitre.place(x=10, y=10)
        lblExo = Label(titleFrame, fg='blue', text="Sur base d’une adresse de réseau et d'informations sur les sous-résaux souhaités,\ncrée une une découpe en sous-réseau classique si possible et fournit un plan d'adressage complet.", font = 'Times 11 italic', justify="left" )
        lblExo.place(x=10, y=40)


        # Frame - Réponses
        self.repFrame = CTkFrame(self,width=SIZE_X-360, height=300)
        self.repFrame.grid_propagate(0)

        # Labels - Titre
        self.rep = StringVar()
        self.rep.set("OUI")
        lblVerif = Label(self.repFrame, textvariable=self.rep, justify="center", fg="red")
        lblVerif.place(x=0, y=0)


    def createSR(self) -> None :
        """
        Récupere Réseau et Données de SR entrés. Crée les sous-réseaux si possible.
        """

        self.attStr.set("")
        self.repFrame.place(x=330, y=150)
        self.repFrame.place_forget()
        if hasattr(self, 'tableFrame'):
            self.tableFrame.place_forget()

        #en fonction du nombre de champs requis, on redimensionne la frame
        if (self.textReseau.get() == "" and self.textSR.get() == "" and self.textHotes.get() == ""):
            self.infoFrame.configure(height=300)
        elif (self.textReseau.get() == "" and self.textSR.get() == ""):
            self.infoFrame.configure(height=290)
        elif (self.textReseau.get() == "" and self.textHotes.get() == ""):
            self.infoFrame.configure(height=290)
        elif (self.textSR.get() == "" and self.textHotes.get() == ""):
            self.infoFrame.configure(height=290)
        elif (self.textReseau.get() == "" or self.textSR.get() == "" or self.textHotes.get() == ""):
            self.infoFrame.configure(height=270)
        else:
            self.infoFrame.configure(height=250)

        if (self.textReseau.get() == "" or self.textSR.get() == "" or self.textHotes.get() == ""):
            self.attStr.set("(*) Champs requis : \n" + ("Adresse de réseau" if self.textReseau.get() == "" else "") + ("\n" if self.textReseau.get() == "" and self.textSR.get() == "" else "") + ("Nombre de SR souhaités" if self.textSR.get() == "" else "") + ("\n" if self.textSR.get() == "" and self.textHotes.get() == "" else "") + ("Nombre d'Hôtes par SR" if self.textHotes.get() == "" else ""))
            return
        
        # Instance de Reseau
        res = Reseau("0.0.0.0", self.textMasque.get(), self.textReseau.get())

        # Vérification des champs
        if (res.masque == "0.0.0.0" and self.textMasque.get() != ""):
            self.attStr.set("Masque Réseau non-valide")
        elif (res.adrReseau == "0.0.0.0"):
            self.attStr.set("Adresse Réseau non-valide")
        else:
            print(res.adrReseau + " - "  + res.masque)
            # find the number of hosts possible with the given network and mask
            net = ipaddress.IPv4Network(res.adrReseau + '/' + res.masque, False)
            nbHotes = net.num_addresses - 2

            # Déterminer s’il sera possible ou pas de réaliser une découpe 
            # classique sur base du nombre de SR. Si la réponse est oui, le 
            # programme devra fournir le plan d’adressage complet de la 
            # découpe demandée. Il devra également indiquer combien de SR on 
            # peut avoir au maximum dans cette découpe

            # Calculer le masque de sous-réseau approprié pour le nombre de sous-réseaux
            subnet_mask_length = net.prefixlen + int(self.textSR.get()).bit_length() - 1
            if subnet_mask_length > 32:
                print("Nombre de sous-réseaux souhaité trop élevé pour l'adresse IP donnée.")
            else:
                subnet = net.subnets(new_prefix=subnet_mask_length)
                subnets_list = list(subnet)

                # Afficher les informations sur les sous-réseaux créés
                print(f"Adresse IP d'origine : {net.network_address}/{net.prefixlen}")
                print(f"Masque de sous-réseau pour {int(self.textSR.get())} sous-réseaux : /{subnet_mask_length}")

                for i, sub in enumerate(subnets_list):
                    print(f"Sous-réseau {i+1} : {sub.network_address}/{subnet_mask_length}")

            #define a frame that will contian the table and scrollbar
            self.tableFrame = CTkFrame(self, width=600, height=150)
            self.tableFrame.grid_propagate(0)

            #define the table with tkinter
            self.table = ttk.Treeview(self.tableFrame, column=('Sous-Réseau', 'Masque', 'Plage', 'Broadcast', 'Hôtes'), show="headings", height=6)
            self.table.heading('#1', text='Sous-Réseau')
            self.table.heading('#2', text='Masque')
            self.table.heading('#3', text='Plage')
            self.table.heading('#4', text='Broadcast')
            self.table.heading('#5', text='Hôtes')

            self.table.column('#0', minwidth=0, width=0, stretch=False)
            self.table.column('#1', stretch=False, minwidth=100, width=100, anchor=CENTER)
            self.table.column('#2', stretch=False, minwidth=100, width=100, anchor=CENTER)
            self.table.column('#3', stretch=False, minwidth=200, width=200, anchor=CENTER)
            self.table.column('#4', stretch=False, minwidth=100, width=100, anchor=CENTER)
            self.table.column('#5', stretch=False, minwidth=100, width=100, anchor=CENTER)
            
            self.table.grid(row=0, column=0)
            
            scrollbar = Scrollbar(self.tableFrame, orient=VERTICAL, command=self.table.yview)
            self.table.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1)

            self.tableFrame.place(x=340, y=200)

            def handle_click(event):
                if self.table.identify_region(event.x, event.y) == "separator":
                    return "break"
            self.table.bind('<Button-1>', handle_click)

            #add data to the table

            for i in range(0, 25):
                self.table.insert(parent='', index='end', iid=i, text= f'{i+1}', values=(f'SR {i+1}', '255.255.255.255', '255.255.255.255 / 255.255.255.255', '255.255.255.255', '100000000'))
            










            self.repFrame.place(x=330, y=150)





    def verifCaracter(self, P):
        if str.isdigit(P) or P == "" or P == ".":
            return True
        else:
            return False
       
    # Fonction de reset de la frame
    def reset(self) -> None:
        self.attStr.set("")
        self.textMasque.delete(0, END)
        self.textReseau.delete(0, END)
        self.textSR.delete(0, END)
        self.textHotes.delete(0, END)
        self.repFrame.place_forget()

        if hasattr(self, 'tableFrame'):
            self.tableFrame.place_forget()


class Reseau():
    """
    Reprend toutes les informations et méthodes de verification/recherche/etc de réseau ou ip. 
    - Adresse Ip
    - Masque du Réseau
    - Adresse du Réseau
    - Adresse de Broadcast
    - Adresse du Sous Réseau
    """

    def __init__(self, ip: str, masque: str, adrReseau: str = "0") -> None:
        self.ip = Reseau.defineIp(self, ip)
        self.masque = Reseau.defineMasque(self, masque)
        self.adrReseau = Reseau.defineAdrReseau(self, adrReseau)
        self.adrBroadcast: str = Reseau.defineAdrBroadcast(self)

        # self.str()


    
    def str(self) -> None:
        print("Reseau : \n\tIp : " + self.ip + "\n\tMasque : " +  self.masque + "\n\tRéseau : " +  self.adrReseau + "\n\tBroadcast : " +  self.adrBroadcast)

    @staticmethod
    def defineIp(self, ip: str) -> str:
        if (Reseau.isIpValide(ip)):
            return ip
        else:
            return"0.0.0.0"

    @staticmethod
    def isIpValide(ip: str) -> bool:
        try:
            ip_object = ipaddress.ip_address(ip) 
            octets = ip.strip().lower().split('.')
            if(int(octets[0])==127 or int(octets[0])==0):
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def defineMasque(self, masque: str) -> str:
        octetsIp = self.ip.strip().lower().split('.')

        # Si le masque n'est pas donné, on le défini en fonction de l'ip
        if(masque==""):
            if(int(octetsIp[0])<127):
                return "255.0.0.0"
            elif(int(octetsIp[0])<192):
                return "255.255.0.0"
            else:
                return "255.255.255.0"
        else:
            # Si le masque est valide, on verifie qu'il est compatible avec l'ip
            if (Reseau.isMasqueValide(masque)):
                octetsMasque = masque.strip().lower().split('.')

                if(int(octetsIp[0])<127 and int(octetsMasque[0])==255):
                    return masque
                elif(int(octetsIp[0])<192 and int(octetsMasque[1])==255):
                    return masque
                elif(int(octetsMasque[2])==255):
                    return masque
                else:
                    return "0.0.0.0"
            else:
                return "0.0.0.0"

    @staticmethod
    def isMasqueValide(masque: str) -> bool:
        octets = masque.strip().lower().split('.')

        # Vérification du nombre d'octets
        if len(octets) != 4:
            print(1)
            return False
        
        # Initialisation d'un booleen pour verifier si on a des 1 contigus // Définition de l'octet précédent
        est_contigu = True

        for octet in octets:
            try:
                val_octet = int(octet)

                # Si l'octet n'est pas compris entre 0 et 255, retourner False
                if val_octet < 0 or val_octet > 255:
                    return False

                # vérifier que l'octet est contigu
                if est_contigu:
                    if val_octet != 255:
                        # Si l'octet qui n'est pas a 255 n'est pas un des octets contigus, retourner False
                        if not (val_octet in [0, 128, 192, 224, 240, 248, 252, 254, 255])  :
                            return False
                        
                        est_contigu = False
                else:
                    # Si n'est pas contigu et l'octet n'est pas 0, retourner False
                    if val_octet != 0:
                        return False
            
            # Si un octet n'est pas un entier, retourner False
            except ValueError:
                return False
            
        # Si le masque fini par des 1, retourner False
        if est_contigu:
            return False
                   
        return True

    @staticmethod
    def defineAdrReseau(self, adrReseau: str) -> str:
        net = ipaddress.IPv4Network(self.ip + '/' + self.masque, False)

        # Si pas de réseau donné, on le défini en fonction de l'ip et du masque
        if (adrReseau == "0"):
            return f'{net.network_address:s}'
        
        # Si un réseau est donné, on vérifie qu'il est valide et qu'il correspond à l'ip et au masque
        if (Reseau.reseauValide(adrReseau)):
            if(adrReseau==f'{net.network_address:s}'):
                return adrReseau
            else:
                # Return -1 pour l'application 2
                return "-1"
        else:
            return "0.0.0.0"
    
    @staticmethod
    def reseauValide(adrReseau: str) -> bool:
        try:
            ip_object = ipaddress.ip_address(adrReseau) 
            octets = adrReseau.strip().lower().split('.')
            if(int(octets[0])==127 or int(octets[0])==0):
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def defineAdrBroadcast(self) -> str:
        if (self.adrReseau != "0.0.0.0" and self.adrReseau != "-1"):
            net = ipaddress.IPv4Network(self.ip + '/' + self.masque, False)
            return f'{net.broadcast_address:s}'
        else:
            return "0.0.0.0"

    
    

    #


class Connexion(CTkFrame):
    # Init de la Frame
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        
        #Titre du Programme
        CTkLabel(self, text="Réseau - Ip : Vérificateur d'Ip", font=CTkFont("Times", 29, "bold", underline=True)).place(y=TITLE_PLACEMENT_Y, x=CENTER_WINDOW, anchor="center")


        #Declaraction des Frames
        self.inFrame = CTkFrame(master=self, width=CONNECTION_FRAME_SIZE_X, height=FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)
        self.upFrame = CTkFrame(master=self, width=SIGNUP_FRAME_SIZE_X, height=FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)


        #Label - Sous-Titre
        CTkLabel(self.inFrame, text="Connexion", font=CTkFont("Times", 26, underline=True)).place(y=30, x=CONNECTION_FRAME_CENTER, anchor="center")
        CTkLabel(self.upFrame, text="Créer un compte", font=CTkFont("Times", 26, underline=True)).place(y=30, x=SIGNUP_FRAME_CENTER, anchor="center")


        #Menu de Connexion
        labConnInfo = CTkLabel(self.inFrame, text="Connectez-vous pour accéder à l'application\net profiter de ses services.", text_color="gray")
        labConnInfo.place(y=70, x=CONNECTION_FRAME_CENTER, anchor="center")

        labConnUser = CTkLabel(self.inFrame, text="Nom d'utilisateur")
        labConnUser.place(y=120, x=CONNECTION_FRAME_CENTER, anchor="center")

        self.entryConnUser = CTkEntry(self.inFrame, width=200, placeholder_text="Identifiant")
        self.entryConnUser.place(y=150, x=CONNECTION_FRAME_CENTER, anchor="center")
        self.entryConnUser.bind("<Key>", self.checkConnection)

        labConnPassword = CTkLabel(self.inFrame, text="Mot de Passe")
        labConnPassword.place(y=200, x=CONNECTION_FRAME_CENTER, anchor="center")

        self.entryConnPassword = CTkEntry(self.inFrame, width=200, show="*", placeholder_text="Mot de passe")
        self.entryConnPassword.place(y=230, x=CONNECTION_FRAME_CENTER, anchor="center")
        self.entryConnPassword.bind("<Key>", self.checkConnection)

        self.btnCheckConn = CTkButton(self.inFrame, text="Se Connecter", cursor="hand2",command= lambda: self.connect(), state=DISABLED)
        self.btnCheckConn.place(y=FRAME_BUTTON_Y - PAD_Y, x=CONNECTION_FRAME_CENTER, anchor="center")

        self.strConnErr = StringVar()
        self.strConnErr.set("")

        lblVerifC = CTkLabel(self.inFrame, textvariable=self.strConnErr, text_color="red")
        lblVerifC.place(y=FRAME_SIZE_Y - 3*PAD_Y, x=CONNECTION_FRAME_CENTER, anchor="center")


        #Menu de Sign Up
        labSignUpInfo = CTkLabel(self.upFrame, text="Créer un compte et profiter directement des services de l'application.", text_color="gray")
        labSignUpInfo.place(y=65, x=SIGNUP_FRAME_CENTER, anchor="center")

        labSignUpUser = CTkLabel(self.upFrame, text="Nom d'utilisateur")
        labSignUpUser.place(y=120, x=SIGNUP_FRAME_CENTER - 100, anchor="center")

        self.entrySignUpUser = CTkEntry(self.upFrame, width=200, placeholder_text="Identifiant")
        self.entrySignUpUser.place(y=120, x=SIGNUP_FRAME_CENTER + 100, anchor="center")
        self.entrySignUpUser.bind("<Key>", self.checkSignUp)

        labSignUpPassword = CTkLabel(self.upFrame, text="Mot de passe")
        labSignUpPassword.place(y=170, x=SIGNUP_FRAME_CENTER - 100, anchor="center")

        self.entrySignUpPassword = CTkEntry(self.upFrame, width=200, show="*", placeholder_text="Mot de passe")
        self.entrySignUpPassword.place(y=170, x=SIGNUP_FRAME_CENTER + 100, anchor="center")
        self.entrySignUpPassword.bind("<Key>", self.checkSignUp)

        labSignUpConfirm = CTkLabel(self.upFrame, text="Confirmer le mot de passe")
        labSignUpConfirm.place(y=220, x=SIGNUP_FRAME_CENTER - 100, anchor="center")

        self.entrySignUpConfirm = CTkEntry(self.upFrame, width=200, show="*", placeholder_text="Mot de passe")
        self.entrySignUpConfirm.place(y=220, x=SIGNUP_FRAME_CENTER + 100, anchor="center")
        self.entrySignUpConfirm.bind("<Key>", self.checkSignUp)

        self.btnCheckSignUp = CTkButton(self.upFrame, text="Créer un nouveau compte", cursor="hand2", command= lambda: self.createAccount(), state=DISABLED)
        self.btnCheckSignUp.place(y=FRAME_BUTTON_Y - PAD_Y, x=SIGNUP_FRAME_CENTER, anchor="center")

        self.strSignUpErr = StringVar()
        self.strSignUpErr.set("")
        
        lblVerifU = CTkLabel(self.upFrame, textvariable=self.strSignUpErr, text_color="red")
        lblVerifU.place(y=FRAME_SIZE_Y - 3*PAD_Y, x=SIGNUP_FRAME_CENTER, anchor="center")


        #Placement des frames
        self.inFrame.place(x = PAD_X, y = FRAME_Y_ORIGIN)
        self.upFrame.place(x=2 * PAD_X + CONNECTION_FRAME_SIZE_X, y = FRAME_Y_ORIGIN)

    def checkConnection(self, event):
        if (self.entryConnUser.get() == "" or self.entryConnPassword.get() == ""):
            self.btnCheckConn.configure(state=DISABLED, cursor="tcross")
            self.strConnErr.set("(*) Tous les champs sont requis")
        else:
            self.btnCheckConn.configure(state=NORMAL, cursor="hand2")
            self.strConnErr.set("")
    
    def checkSignUp(self, event):
        if (self.entrySignUpUser.get() == "" or self.entrySignUpPassword.get() == "" or self.entrySignUpConfirm.get() == ""):
            self.btnCheckSignUp.configure(state=DISABLED, cursor="tcross")
            self.strSignUpErr.set("(*) Tous les champs sont requis")
        else:
            self.btnCheckSignUp.configure(state=NORMAL, cursor="hand2")
            self.strSignUpErr.set("")

    def createAccount(self) :
        userId = self.entrySignUpUser.get()
        userPassword = self.entrySignUpPassword.get()
        passwordConfirmation = self.entrySignUpConfirm.get()
        

        if (userId == "" or userPassword == "" or passwordConfirmation == ""):
            self.strSignUpErr.set("(*) Tous les champs sont requis")
            return
        
        if (userPassword != passwordConfirmation):
            self.strSignUpErr.set("Les mots de passe ne correspondent pas")
            return

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(userId)])
        if c.fetchall():
            self.strSignUpErr.set("Ce nom d'utilisateur existe déjà")
        else:
            hashed_password = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())

            c.execute("INSERT INTO user (username,password) VALUES (?,?)", (userId, hashed_password))
            conn.commit()
            setConnected()

        c.close()
        conn.close()
        return
        
    def connect(self):
        userId = self.entryConnUser.get()
        userPassword = self.entryConnPassword.get()
        if (userId == "" or userPassword == ""):
            self.strConnErr.set("(*) Tous les champs sont requis")
            return

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(userId)])

        result = c.fetchall()
        if result:
            if bcrypt.checkpw(userPassword.encode('utf8'), result[0][2]):
                self.strConnErr.set("Connexion réussie")
                setConnected()

            else:
                self.strConnErr.set("Mot de passe incorrect")

        else:
            self.strConnErr.set("Nom d'utilisateur incorrect")

        c.close()
        conn.close()
        return

    def reset(self):
        self.btnCheckConn.configure(state=DISABLED, cursor="tcross")
        self.btnCheckSignUp.configure(state=DISABLED, cursor="tcross")
        self.entryConnUser.delete(0, END)
        self.entryConnPassword.delete(0, END)
        self.entrySignUpUser.delete(0, END)
        self.entrySignUpPassword.delete(0, END)
        self.entrySignUpConfirm.delete(0, END)
        self.strConnErr.set("")
        self.strSignUpErr.set("")

# Start
app = MainApplication()
app.mainloop()
