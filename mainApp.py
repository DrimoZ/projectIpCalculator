from constants import *
from reseau import Reseau

from tkinter import ttk
from tkinter import *
from customtkinter import *


import webbrowser
import sqlite3
import bcrypt
import os
from PIL import Image
    
### GROUPE 5 ###
set_appearance_mode("dark") 
set_default_color_theme("green")


# Gestion du statut de connexion
isConnected = False

def getConnected():
    global isConnected
    return isConnected

def setConnected():
    global isConnected
    isConnected = True
    app.returnButton.configure(state= NORMAL, cursor="hand2")
    app.disconnectButton.configure(state= NORMAL, cursor="hand2", command=setDisconnected)
    app.show_frame(HomePage)

def setDisconnected():
    global isConnected
    isConnected = False
    app.returnButton.configure(state= DISABLED, cursor="tcross")
    app.disconnectButton.configure(state= DISABLED, cursor="tcross")
    app.show_frame(Connexion)

# Check Inputs - Allow only Digits or "."
def verifCaracter(P):
    if str.isdigit(P) or P == "" or P == ".":
        if P == "²" or P == "³":
            return False
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
        quitButton = CTkButton(self, text="Quitter l'application", command=self.destroy, cursor="hand2", fg_color=BUTTON_FG_COLOR, bg_color='#333232').place(x=SIZE_X-150, y=SIZE_Y-35)
        githubButton = CTkButton(self, text="GitHub", command=self.ouvrir_github, cursor="hand2", fg_color=BUTTON_FG_COLOR, bg_color='#333232').place(x=SIZE_X-300, y=SIZE_Y-35)

        self.disconnectButton = CTkButton(self, text="Se Déconnecter", cursor="hand2", fg_color=BUTTON_FG_COLOR, bg_color='#333232')
        self.disconnectButton.configure(state= DISABLED, cursor="tcross")
        self.disconnectButton.place(x=160, y=SIZE_Y-35)

        self.returnButton = CTkButton(self, text="Retourner au menu", command=lambda : self.show_frame(HomePage), fg_color=BUTTON_FG_COLOR, bg_color='#333232')
        self.returnButton.configure(state= DISABLED, cursor="tcross")
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
            img = Image.open(os.path.join(current_dir, "images", list[i][1]))

            # Cree une image Tkinter a partir de l'image PIL
            img_tk = CTkImage(img,size=(250, 250))
            # Montre l'image dans un label
            self.appImglabel = CTkLabel(appFrame,image=img_tk,width=250,height=250,text="")

            # Label de description de l'application
            appDescLabel = CTkLabel(appFrame, text=list[i][2], text_color="gray", justify="center")

            # Bouton d'accès à l'application
            appButton = CTkButton(appFrame, text=list[i][0], fg_color=BUTTON_FG_COLOR)

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
            img = Image.open(os.path.join(current_dir, "images", "Palergun.png"))
            img_tk = CTkImage(img,size=(250, 250))
            self.appImglabel.configure(image=img_tk)
            return
        
    def reset(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img = Image.open(os.path.join(current_dir, "images", "decoupe.png"))
        img_tk = CTkImage(img,size=(250, 250))
        self.appImglabel.configure(image=img_tk)
        return
        
# Application 1
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

        self.app1DataIp = StringVar()
        self.app1DataIp.set("")
        app1EntryIp = CTkEntry(self.app1InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'), textvariable=self.app1DataIp)
        app1EntryIp.place(y=120, x=INPUTFRAME_CENTER, anchor="center")
        app1EntryIp.bind("<Key>", self.checkEntries)

        self.labMask = CTkLabel(self.app1InputFrame, text="Masque de réseau")

        self.app1DataMask = StringVar()
        self.app1DataMask.set("")
        self.app1EntryMask = CTkEntry(self.app1InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'), textvariable=self.app1DataMask)
        self.app1EntryMask.bind("<Key>", self.checkEntries)

        # Choix d'ajouter un masque ou non
        self.hasCustomMask = StringVar()
        self.hasCustomMask.set("off")

        def checkbox_event():
            if (self.hasCustomMask.get() == "on"):
                self.app1DataMask.set("")
                self.labMask.place(y=200, x=INPUTFRAME_CENTER, anchor="center")
                self.app1EntryMask.place(y=230, x=INPUTFRAME_CENTER, anchor="center")
            else:
                self.app1DataMask.set("")
                self.labMask.place_forget()
                self.app1EntryMask.place_forget()

        checkbox = CTkCheckBox(self.app1InputFrame, text="Découpé en sous-réseaux ?", command=checkbox_event, variable=self.hasCustomMask, onvalue="on", offvalue="off")
        checkbox.place(y=160, x=INPUTFRAME_CENTER, anchor="center")
        checkbox.bind("<Button-1>", self.checkEntries)
        
        self.app1BtnCheck = CTkButton(self.app1InputFrame, text="Trouver le réseaux", cursor="hand2", command= lambda: self.trouverReseau(), state=DISABLED, fg_color=BUTTON_FG_COLOR)
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

        labOutTitre = CTkLabel(self.app1OutputFrame, text="Résultats", font = CTkFont("Times", 21, underline=True))
        labOutTitre.place(y=30, x=TITLE_OUTPUT_SIZE_X/2, anchor="center")

        labOutIp = CTkLabel(self.app1OutputFrame, text="Adresse IP : ")
        labOutIp.place(y=70, x=TITLE_OUTPUT_SIZE_X/2 - 130, anchor="w")

        self.app1LblOutRes = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutIp, text_color="green", justify="left")
        self.app1LblOutRes.place(y=70, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutMask = CTkLabel(self.app1OutputFrame, text="Masque de réseau : ")
        labOutMask.place(y=100, x=TITLE_OUTPUT_SIZE_X/2 - 130, anchor="w")

        self.app1LblOutMask = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutMask, text_color="green", justify="left")
        self.app1LblOutMask.place(y=100, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        self.labOutRes = CTkLabel(self.app1OutputFrame, text="Adresse de réseau : ")
        self.labOutRes.place(y=130, x=TITLE_OUTPUT_SIZE_X/2 - 130, anchor="w")

        self.app1LblOutRes = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutRes, text_color="green", justify="left")
        self.app1LblOutRes.place(y=130, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutBrd = CTkLabel(self.app1OutputFrame, text="Adresse de broadcast : ")
        labOutBrd.place(y=160, x=TITLE_OUTPUT_SIZE_X/2 - 130, anchor="w")

        self.app1LblOutBrd = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutBrd, text_color="green", justify="left")
        self.app1LblOutBrd.place(y=160, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")

        labOutSr = CTkLabel(self.app1OutputFrame, text="Découpe en Sous-Réseau : ")
        labOutSr.place(y=190, x=TITLE_OUTPUT_SIZE_X/2 - 130, anchor="w")

        self.app1LblOutSr = CTkLabel(self.app1OutputFrame, textvariable=self.app1StrOutSR, text_color="green", justify="left")
        self.app1LblOutSr.place(y=190, x=TITLE_OUTPUT_SIZE_X/2 + 50, anchor="w")


        #Placement des frames
        self.app1InputFrame.place(x = PAD_X, y = PAD_Y)
        app1TitleFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = PAD_Y)

    def checkEntries(self, event):
        if (self.hasCustomMask.get() == "off"):
            self.app1DataMask.set("")

        if (self.app1DataIp.get() == ""):
            self.app1BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app1strErr.set("(*) Champ requis : IP")
        elif (self.hasCustomMask.get() == "on" and self.app1DataMask.get() == ""):
            self.app1BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app1strErr.set("(*) Champ requis : Masque de réseau")
        else:
            self.app1BtnCheck.configure(state=NORMAL, cursor="hand2")
            self.app1strErr.set("")

    def trouverReseau(self) -> None :
        """
        Récupere Ip, Masque. Défini le réseau et le broadcast. Défini le sous-réseau si besoin.
        """

        if (self.hasCustomMask.get() == "off"):
            self.app1DataMask.set("")

        self.app1strErr.set("")
        self.app1OutputFrame.place_forget()

        # Un des champs est vide
        if (self.app1DataIp.get() == ""):
            self.app1strErr.set("(*) Champ requis : IP")
            return
        elif (self.hasCustomMask.get() == "on" and self.app1DataMask.get() == ""):
            self.app1strErr.set("(*) Champ requis : Masque de réseau")
            return
        
        
        # Instance de Reseau
        res = Reseau(self.app1DataIp.get(), self.app1DataMask.get() if self.hasCustomMask.get() == "on" else "")

        # Vérification des champs
        if (res.ip == DEFAULT_NET_IP):
            self.app1strErr.set("Adresse IP non-valide ou réservée")
        elif (res.netMask == DEFAULT_NET_IP and self.app1DataMask.get() != ""):
            self.app1strErr.set("Masque Réseau non-valide")
        else:
            self.app1StrOutIp.set(res.ip)
            self.app1StrOutMask.set(res.netMask)
            self.app1StrOutRes.set(res.netAddress)
            self.app1StrOutBrd.set(res.netBroadcast)

            if (self.hasCustomMask.get() == "on"):
                self.app1StrOutSR.set("Oui")
                self.labOutRes.configure(text="Adresse du Sous-Réseau : ")
            else:
                self.app1StrOutSR.set("Non")
                self.labOutRes.configure(text="Adresse du Réseau : ")
            self.app1OutputFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = 2*PAD_Y + TITLE_FRAME_SIZE_Y)

    # Fonction de reset de la frame
    def reset(self) -> None:
        self.app1BtnCheck.configure(state=DISABLED, cursor="tcross")
        self.hasCustomMask.set("off")
        self.app1DataMask.set("")
        self.app1DataIp.set("")


        self.labMask.place_forget()
        self.app1EntryMask.place_forget()
        self.app1OutputFrame.place_forget()

        self.app1strErr.set("") 

# Application 2
class Application2(CTkFrame):
    """
    Sur base d’une adresse IP et de son masque et d’une adresse de réseau, le 
    programme doit déterminer si l’IP appartient au réseau ou pas. CLASSFULL
    """

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        #Declaraction des Frames
        self.app2InputFrame = CTkFrame(self, width=INPUTFRAME_SIZE_X, height=FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)
        self.app2OutputFrame = CTkFrame(self, width=TITLE_OUTPUT_SIZE_X, height=OUTPUT_FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)
        app2TitleFrame = CTkFrame(self, width=TITLE_OUTPUT_SIZE_X, height=TITLE_FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)


        # Titre
        lblTitre = CTkLabel(app2TitleFrame, text="Application 2 : Présence d'une IP dans le réseau", font = CTkFont("Times", 21, underline=True))
        lblTitre.place(x=12, y=10)
        app2Description = "Sur base d’une IP et d’une adresse de réseau (ainsi que d'un masque si\ndécoupé en sous-réseau), vérifie si l’adresse IP donnée appartient au\nréseau ou pas."
        lblExo = CTkLabel(app2TitleFrame, text_color='cyan', text=app2Description, font = CTkFont("Times", 17, slant="italic"), justify="left" )
        lblExo.place(x=10, y=40)

        # Inputs
        vcmd = (self.register(verifCaracter))

        labIntro = CTkLabel(self.app2InputFrame, text="Entrer les informations\nrequises pour l'application", text_color="gray")
        labIntro.place(y=30, x=INPUTFRAME_CENTER, anchor="center")

        labIp = CTkLabel(self.app2InputFrame, text="Adresse Ip")
        labIp.place(y=70, x=INPUTFRAME_CENTER, anchor="center")

        self.app2EntryIp = CTkEntry(self.app2InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'))
        self.app2EntryIp.place(y=100, x=INPUTFRAME_CENTER, anchor="center")
        self.app2EntryIp.bind("<Key>", self.checkEntries)

        labReseau = CTkLabel(self.app2InputFrame, text="Adresse du Réseau")
        labReseau.place(y=140, x=INPUTFRAME_CENTER, anchor="center")

        self.app2EntryRes = CTkEntry(self.app2InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'))
        self.app2EntryRes.place(y=170, x=INPUTFRAME_CENTER, anchor="center")
        self.app2EntryRes.bind("<Key>", self.checkEntries)

        self.labMask = CTkLabel(self.app2InputFrame, text="Masque de réseau")

        self.app2EntryMask = CTkEntry(self.app2InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'))
        self.app2EntryMask.bind("<Key>", self.checkEntries)


        self.hasCustomMask = StringVar()
        self.hasCustomMask.set("off")

        def checkbox_event():
            if (self.hasCustomMask.get() == "on"):
                self.labMask.place(y=250, x=INPUTFRAME_CENTER, anchor="center")
                self.app2EntryMask.place(y=280, x=INPUTFRAME_CENTER, anchor="center")
            else:
                self.app2EntryMask.delete(0, END)
                self.labMask.place_forget()
                self.app2EntryMask.place_forget()

        checkbox = CTkCheckBox(self.app2InputFrame, text="Découpé en sous-réseaux ?", command=checkbox_event, variable=self.hasCustomMask, onvalue="on", offvalue="off")
        checkbox.place(y=210, x=INPUTFRAME_CENTER, anchor="center")
        checkbox.bind("<Button-1>", self.checkEntries)
        
        self.app2BtnCheck = CTkButton(self.app2InputFrame, text="Trouver le réseaux", cursor="hand2", command= lambda: self.checkReseau(), state=DISABLED, fg_color=BUTTON_FG_COLOR)
        self.app2BtnCheck.place(y=FRAME_BUTTON_Y - PAD_Y, x=INPUTFRAME_CENTER, anchor="center")

        self.app2strErr = StringVar()
        self.app2strErr.set("")
        
        labErr = CTkLabel(self.app2InputFrame, textvariable=self.app2strErr, text_color="red")
        labErr.place(y=FRAME_SIZE_Y - 3*PAD_Y, x=INPUTFRAME_CENTER, anchor="center")

        # Frame d'output
        labOutTitre = CTkLabel(self.app2OutputFrame, text="Résultats", font = CTkFont("Times", 21, underline=True))
        labOutTitre.place(y=30, x=TITLE_OUTPUT_SIZE_X/2, anchor="center")

        self.app2StrOut = StringVar()
        self.app2StrOut.set("")

        self.app2LblOutSr = CTkLabel(self.app2OutputFrame, textvariable=self.app2StrOut, justify="left")
        self.app2LblOutSr.place(y=OUTPUT_FRAME_SIZE_Y/2, x=TITLE_OUTPUT_SIZE_X/2, anchor="center")

        #Placement des frames
        self.app2InputFrame.place(x = PAD_X, y = PAD_Y)
        app2TitleFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = PAD_Y)


    def checkEntries(self, event):
        if (self.hasCustomMask.get() == "off"):
            self.app2EntryMask.delete(0, END)

        if (self.app2EntryIp.get() == "" and self.app2EntryRes.get() == ""):
            self.app2BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app2strErr.set("(*) Champ requis : IP et Adresse de réseau")
        elif (self.app2EntryIp.get() == "" ):
            self.app2BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app2strErr.set("(*) Champ requis : IP")
        elif (self.app2EntryRes.get() == ""):
            self.app2BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app2strErr.set("(*) Champ requis : Adresse de réseau")
        elif (self.hasCustomMask.get() == "on" and self.app2EntryMask.get() == ""):
            self.app2BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app2strErr.set("(*) Champ requis : Masque de réseau")
        else:
            self.app2BtnCheck.configure(state=NORMAL, cursor="hand2")
            self.app2strErr.set("")

    def checkReseau(self) -> None :
        """
        Récupere Ip, Masque et Réseau entrés. Vérifie que tout soit valide. Explique si l'Ip fait partie du Réseau donné. 
        """

        self.app2strErr.set("")
        self.app2OutputFrame.place_forget()

        # Un des champs est vide
        if (self.app2EntryIp.get() == "" and self.app2EntryRes.get() == ""):
            self.app2strErr.set("(*) Champ requis : IP et Adresse de réseau")
            return
        elif (self.app2EntryIp.get() == "" ):
            self.app2strErr.set("(*) Champ requis : IP")
            return
        elif (self.app2EntryRes.get() == ""):
            self.app2strErr.set("(*) Champ requis : Adresse de réseau")
            return
        elif (self.hasCustomMask.get() == "on" and self.app2EntryMask.get() == ""):
            self.app2strErr.set("(*) Champ requis : Masque de réseau")
            return
        
        # Instance de Reseau
        res = Reseau(self.app2EntryIp.get(), self.app2EntryMask.get() if self.hasCustomMask.get() == "on" else "", self.app2EntryRes.get())

        # Vérification des champs
        if (res.ip == "0.0.0.0"):
            self.app2strErr.set("Adresse IP non-valide ou réservée")
        elif (res.netMask == "0.0.0.0" and self.app2EntryMask.get() != ""):
            self.app2strErr.set("Masque Réseau non-valide")
        elif (res.netAddress == "0.0.0.0"):
            self.app2strErr.set("Adresse Réseau non-valide")
        elif (res.netAddress == "-1"):
            self.app2StrOut.set("L'adresse IP n'appartient pas au réseau donné.")
            self.app2LblOutSr.configure(text_color="red")
            self.app2OutputFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = 2*PAD_Y + TITLE_FRAME_SIZE_Y)

        else:
            self.app2StrOut.set("L'adresse IP appartient au réseau donné.")
            self.app2LblOutSr.configure(text_color="green")
            self.app2OutputFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = 2*PAD_Y + TITLE_FRAME_SIZE_Y)

    # Fonction de reset de la frame
    def reset(self) -> None:
        self.app2BtnCheck.configure(state=DISABLED, cursor="tcross")
        self.hasCustomMask.set("off")
        self.app2EntryMask.delete(0, END)
        self.app2EntryIp.delete(0, END)
        self.app2EntryRes.delete(0, END)

        self.labMask.place_forget()
        self.app2EntryMask.place_forget()

        self.app2OutputFrame.place_forget()

        self.app2strErr.set("")

# Application 3
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

        #Declaraction des Frames
        self.app3InputFrame = CTkFrame(self, width=INPUTFRAME_SIZE_X, height=FRAME_SIZE_Y + 2 * PAD_Y, corner_radius=FRAME_CORNER_RADIUS)
        self.app3OutputFrame = CTkFrame(self, width=TITLE_OUTPUT_SIZE_X, height=OUTPUT_FRAME_SIZE_Y  + 2 * PAD_Y, corner_radius=FRAME_CORNER_RADIUS)
        app3TitleFrame = CTkFrame(self, width=TITLE_OUTPUT_SIZE_X, height=TITLE_FRAME_SIZE_Y, corner_radius=FRAME_CORNER_RADIUS)


        # Titre
        lblTitre = CTkLabel(app3TitleFrame, text="Application 3 : Création de Sous-Réseaux", font = CTkFont("Times", 21, underline=True))
        lblTitre.place(x=12, y=10)
        app3Description = "Sur base d’une adresse de réseau et d'informations sur les sous-résaux\nsouhaités, crée une une découpe en sous-réseau classique si possible\net fournit un plan d'adressage complet."
        lblExo = CTkLabel(app3TitleFrame, text_color='cyan', text=app3Description, font = CTkFont("Times", 17, slant="italic"), justify="left" )
        lblExo.place(x=10, y=40)

        # Inputs
        vcmd = (self.register(verifCaracter))

        labIntro = CTkLabel(self.app3InputFrame, text="Entrer les informations\nrequises pour l'application", text_color="gray")
        labIntro.place(y=30, x=INPUTFRAME_CENTER, anchor="center")


        labReseau = CTkLabel(self.app3InputFrame, text="Adresse du Réseau")
        labReseau.place(y=70, x=INPUTFRAME_CENTER, anchor="center")

        self.app3dataRes = StringVar()
        self.app3dataRes.set("")
        app3EntryRes = CTkEntry(self.app3InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'), textvariable=self.app3dataRes)
        app3EntryRes.place(y=100, x=INPUTFRAME_CENTER, anchor="center")
        app3EntryRes.bind("<Key>", self.checkEntries)
        

        self.labHotes = CTkLabel(self.app3InputFrame, text="Nombre d'hôtes souhaités par SR")
        self.labHotes.place(y=140, x=INPUTFRAME_CENTER, anchor="center")
        
        self.app3dataHotes = StringVar()
        self.app3dataHotes.set("")
        app3EntryHotes = CTkEntry(self.app3InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'), textvariable=self.app3dataHotes)
        app3EntryHotes.place(y=170, x=INPUTFRAME_CENTER, anchor="center")
        app3EntryHotes.bind("<Key>", self.checkEntries)
        

        self.labSr = CTkLabel(self.app3InputFrame, text="Nombre de sous-réseaux souhaités")
        self.labSr.place(y=210, x=INPUTFRAME_CENTER, anchor="center")
        
        self.app3dataSr = StringVar()
        self.app3dataSr.set("")
        app3EntrySr = CTkEntry(self.app3InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'), textvariable=self.app3dataSr)
        app3EntrySr.place(y=240, x=INPUTFRAME_CENTER, anchor="center")
        app3EntrySr.bind("<Key>", self.checkEntries)


        self.labMask = CTkLabel(self.app3InputFrame, text="Masque de Sous-Réseau")

        self.app3dataMask = StringVar()
        self.app3dataMask.set("")
        self.app3EntryMask = CTkEntry(self.app3InputFrame, width=200, validate="key", validatecommand=(vcmd, '%S'), textvariable=self.app3dataMask)
        self.app3EntryMask.bind("<Key>", self.checkEntries)

        self.hasCustomMask = StringVar()
        self.hasCustomMask.set("off")
    
        def checkbox_event():
            if (self.hasCustomMask.get() == "on"):
                self.labMask.place(y=310, x=INPUTFRAME_CENTER, anchor="center")
                self.app3EntryMask.place(y=340, x=INPUTFRAME_CENTER, anchor="center")
            else:
                self.app3dataMask.set("")
                self.labMask.place_forget()
                self.app3EntryMask.place_forget()

        checkbox = CTkCheckBox(self.app3InputFrame, text="Découpé en sous-réseaux ?", command=checkbox_event, variable=self.hasCustomMask, onvalue="on", offvalue="off")
        checkbox.place(y=280, x=INPUTFRAME_CENTER, anchor="center")
        checkbox.bind("<Button-1>", self.checkEntries)
        
        self.app3BtnCheck = CTkButton(self.app3InputFrame, text="Trouver le réseaux", cursor="hand2", command= lambda: self.createSR(), state=DISABLED, fg_color=BUTTON_FG_COLOR)
        self.app3BtnCheck.place(y=FRAME_BUTTON_Y + PAD_Y, x=INPUTFRAME_CENTER, anchor="center")

        self.app3strErr = StringVar()
        self.app3strErr.set("")
        labErr = CTkLabel(self.app3InputFrame, textvariable=self.app3strErr, text_color="red")
        labErr.place(y=FRAME_SIZE_Y - PAD_Y - 10, x=INPUTFRAME_CENTER, anchor="center")

        # Frame d'output
        labOutTitre = CTkLabel(self.app3OutputFrame, text="Résultats", font = CTkFont("Times", 21, underline=True))
        labOutTitre.place(y=30, x=TITLE_OUTPUT_SIZE_X/2, anchor="center")
        self.labOutResult = CTkLabel(self.app3OutputFrame, text="Impossible de créer un sous-réseau avec les données entrées.", text_color="red")
        # Frame de la table/buttons
        self.app3frameSubnets = CTkFrame(self.app3OutputFrame, width=519, height=215)
        # self.app3frameSubnets.place(x=25, y=70)

        # Choix du paramètre de création des SR (Hotes ou nb de Sr) si besoin
        self.app3btnPrefSr = CTkButton(self.app3frameSubnets, text="Prioriser la découpe par nombre de SR", cursor="hand2", width=(TITLE_OUTPUT_SIZE_X - 50)/2, height=30,
                                corner_radius=0, fg_color=BUTTON_FG_COLOR)
        
        self.app3btnPrefHotes = CTkButton(self.app3frameSubnets, text="Prioriser la découpe par nombre d'hôtes par SR", cursor="hand2", width=(TITLE_OUTPUT_SIZE_X - 50)/2, height=30,
                                corner_radius=0, fg_color=BUTTON_FG_COLOR)
        
        

        #Placement des frames
        self.app3InputFrame.place(x = PAD_X, y = PAD_Y)
        app3TitleFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = PAD_Y)

        # Temporary
        self.app3OutputFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = 2*PAD_Y + TITLE_FRAME_SIZE_Y)

    def checkEntries(self, event):
        if (self.hasCustomMask.get() == "off"):
            self.app3dataMask.set("")
        
        if (self.app3dataRes.get() == "" or self.app3dataHotes.get() == "" or self.app3dataSr.get() == "" or (self.hasCustomMask.get() == "on" and self.app3dataMask.get() == "")):
            self.app3BtnCheck.configure(state=DISABLED, cursor="tcross")
            self.app3strErr.set("(*) Tous les champs sont requis.")
        else:
            self.app3BtnCheck.configure(state=NORMAL, cursor="hand2")
            self.app3strErr.set("")

    
    def createSR(self) -> None :
        """
        Récupere Réseau et Données de SR entrés. Crée les sous-réseaux si possible.
        """

        self.app3strErr.set("")
        self.app3OutputFrame.place_forget()

        # Un des champs est vide
        if (self.app3dataRes.get() == "" or self.app3dataHotes.get() == "" or self.app3dataSr.get() == "" or (self.hasCustomMask.get() == "on" and self.app3dataMask.get() == "")):
            self.app3strErr.set("(*) Tous les champs sont requis.")
            return
        
        # Instance de Reseau
        res = Reseau(DEFAULT_NET_IP, self.app3EntryMask.get() if self.hasCustomMask.get() == "on" else "", self.app3dataRes.get(), True, int(self.app3dataSr.get()), int(self.app3dataHotes.get()))

        # Vérification des champs
        print(res.netAddress)
        if (res.netMask == DEFAULT_NET_IP and self.app3dataMask.get() != ""):
            self.app3strErr.set("Masque Réseau non-valide")
        elif (res.netAddress == DEFAULT_NET_IP) or (res.netAddress == "-1"):
            self.app3strErr.set("Adresse Réseau non-valide ou réservée")
        else:
            self.table = ttk.Treeview(self.app3frameSubnets, column=('N° SR', 'Adresse SR', 'Broadcast', 'Plage Ip', 'Pas', 'Hôtes'), show="headings", height=8)
            self.table.heading('#1', text='N° SR')
            self.table.heading('#2', text='Adresse SR')
            self.table.heading('#3', text='Broadcast')
            self.table.heading('#4', text='Plage IP')
            self.table.heading('#5', text='Pas')
            self.table.heading('#6', text='Hôtes')

            self.table.column('#0', minwidth=0, width=0, stretch=False)
            self.table.column('#1', stretch=False, minwidth=50, width=50, anchor=CENTER)
            self.table.column('#2', stretch=False, minwidth=100, width=100, anchor=CENTER)
            self.table.column('#3', stretch=False, minwidth=100, width=100, anchor=CENTER)
            self.table.column('#4', stretch=False, minwidth=170, width=170, anchor=CENTER)
            self.table.column('#5', stretch=False, minwidth=50, width=50, anchor=CENTER)
            self.table.column('#6', stretch=False, minwidth=49, width=49, anchor=CENTER)

            self.table.place(x=0, y=30)
            
            scrollbar = Scrollbar(self.app3frameSubnets, orient=VERTICAL, command=self.table.yview)
            self.table.configure(yscroll=scrollbar.set)

            def handle_click(event):
                if self.table.identify_region(event.x, event.y) == "separator":
                    return "break"
            self.table.bind('<Button-1>', handle_click)


            # Vérification de la possibilité de découper le réseau en fonction des 2 parametres
            if (res.subnets != []):
                # Liste renvoyée par la fonction de découpage non-vide
                
                pass
            elif (res.subnets == [] and not res.canCreateFromHosts and not res.canCreateFromSubnets): 
                #Pas possible de creer un quelconque sous-réseau avec les données entrées
                
                labOutResult.place(y=OUTPUT_FRAME_SIZE_Y/2, x=TITLE_OUTPUT_SIZE_X/2, anchor="center")



            #add data to the table
            for i, sub in enumerate(res.subnets):
                self.table.insert(parent='', index='end', iid=i, text= f'{i+1}', values=(
                # Numéro
                f'{i+1}', 
                # Adresse sr
                f'{sub.network_address}/{sub.prefixlen}',
                # Broadcast
                f'{sub.network_address+res.maxNetHosts+1}',
                # Plage
                f'{sub.network_address+1} - {sub.network_address+res.maxNetHosts}',
                # Pas
                f'{res.maxNetHosts+2}',
                # Hôtes
                f'{res.maxNetHosts}'))
            
            self.app3OutputFrame.place(x=2 * PAD_X + INPUTFRAME_SIZE_X, y = 2*PAD_Y + TITLE_FRAME_SIZE_Y)

    
    
    # Fonction de reset de la frame
    def reset(self) -> None:
        self.app3BtnCheck.configure(state=DISABLED, cursor="tcross")
        self.hasCustomMask.set("off")

        self.app3dataRes.set("192.168.23.0")
        self.app3dataMask.set("")
        self.app3dataHotes.set("12")
        self.app3dataSr.set("12")

        self.labMask.place_forget()
        self.app3EntryMask.place_forget()

        self.app3OutputFrame.place_forget()
        self.labOutResult.place_forget()

        self.app3strErr.set("")

# Page de Connexion
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

        self.btnCheckConn = CTkButton(self.inFrame, text="Se Connecter", cursor="hand2",command= lambda: self.connect(), state=DISABLED, fg_color=BUTTON_FG_COLOR)
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

        self.btnCheckSignUp = CTkButton(self.upFrame, text="Créer un nouveau compte", cursor="hand2", command= lambda: self.createAccount(), state=DISABLED, fg_color=BUTTON_FG_COLOR)
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
