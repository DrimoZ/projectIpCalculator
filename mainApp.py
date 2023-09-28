from tkinter import ttk
from tkinter import *

import ipaddress
import webbrowser
import sqlite3
import bcrypt
import os
from PIL import ImageTk, Image

### GROUPE 5 

PAD_X = 30
PAD_Y = 30
SIZE_X = 1000
SIZE_Y = 560

isConnected = False

def setConnected():
    global isConnected
    isConnected = True
    app.returnButton.config(state= NORMAL, cursor="hand2")
    app.disconnectButton.config(state= NORMAL, cursor="hand2", command=setDisconnected)
    app.show_frame(HomePage)

def getConnected():
    global isConnected
    return isConnected

def setDisconnected():
    global isConnected
    isConnected = False
    app.returnButton.config(state= DISABLED, cursor="tcross")
    app.disconnectButton.config(state= DISABLED, cursor="tcross")
    app.show_frame(Connexion)


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
        container = Frame(self, cursor="tcross") 
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
            if (not isinstance(frame, HomePage)):
                frame.reset()
            frame.tkraise()
        else:
            frame = self.frames[Connexion]
            frame.reset()
            frame.tkraise()

    def ouvrir_github(self):
        webbrowser.open("https://github.com/DrimoZ/projectIpCalculator")
        
  
# Page d'acceuil
class HomePage(Frame):
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
        Frame.__init__(self, parent)

        label = Label(self, text ="Application en Python pour le cours de Reseau/IP - 2023/2024", font = 'Times 19', borderwidth=1, relief="solid")
        label.grid(row = 0, column = 0,  columnspan = 3, padx = 10, pady = 10)

        list = [
            ["Application 1", "IPFinder.png"],
            ["Application 2", "IPFinder.png"],
            ["Application 3", "IPFinder.png"],
        ]

        for i in range(0, len(list)):
            self.grid_columnconfigure(i, weight=1)
            frame = Frame(self, highlightbackground="red", highlightthickness=1)

            # Convert the image data into a PIL Image
            current_dir = os.path.dirname(os.path.abspath(__file__))
            img = Image.open(os.path.join(current_dir, "Image", list[i][1]))

            # Create a Tkinter PhotoImage object from the PIL Image
            img_tk = ImageTk.PhotoImage(img)

            # Resize the image to your desired dimensions (e.g., 300x300 pixels)
            img = img.resize((700, 700), Image.Resampling.LANCZOS)


            # , borderwidth=1, relief="solid", justify="center", width=200,height=200
            label = Label(frame,image=img_tk,width=300,height=300)
            
            # Display the image in a Label widget
            label.config(image=img_tk)
            label.image = img_tk
                
            label.grid(row = 1, column = 0)

            appButton = Button(frame, text =list[i][0], borderwidth=1, relief="solid", cursor="hand2")
            if (i == 0):
                appButton.config(command = lambda : controller.show_frame(Application1))
            elif (i == 1):
                appButton.config(command = lambda : controller.show_frame(Application2))
            elif (i == 2):
                appButton.config(command = lambda : controller.show_frame(Application3))

            appButton.grid(row = 2, column = 0, padx = 10, pady = 10)
            frame.grid(row = 1, column = i, padx = 10, pady = 10)
  
class Application1(Frame):
    """
    En classfull uniquement, sur base d’une adresse IP et d’un masque, le 
    programme doit fournir l’adresse de réseau et l’adresse de broadcast du 
    réseau. Si une découpe en sous-réseau est réalisée, le programme doit 
    déterminer l’adresse de SR
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Frame - Données d'entrée
        self.infoFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        self.infoFrame.grid_propagate(0)
        self.infoFrame.config(width=270, height=170)

        # Labels
        labIp = Label(self.infoFrame, text="Adresse Ip * : ", width=15)
        labIp.grid(row = 1, column = 0, padx = 10, pady = 10)
        labMasque = Label(self.infoFrame, text="Masque SR : ", width=15)
        labMasque.grid(row = 2, column = 0, padx = 10, pady = 10)

        # Entries
        vcmd = (self.register(self.verifCaracter))
        self.textIp = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textIp.grid(row = 1, column = 1, pady = 10)
        self.textMasque = Entry(self.infoFrame, width=20, validate="key", validatecommand=(vcmd, '%S'))
        self.textMasque.grid(row = 2, column = 1, pady = 10)

        # Label d'erreur
        self.attStr = StringVar()
        self.attStr.set("")
        lblVerif = Label(self.infoFrame, textvariable=self.attStr, justify="center", fg="red")
        lblVerif.grid(row = 4, column = 0, columnspan=2, padx = 10, pady = 10)

        # Bouton de vérification
        btnCheck = Button(self.infoFrame, text="Trouver le réseau", cursor="hand2") 
        btnCheck.config(command= lambda: self.trouverReseau())
        btnCheck.grid(row = 5, column = 0, columnspan=2, padx = 10, pady = 10)

        # Fin de la Frame d'entrée
        self.infoFrame.place(x=30, y=30)


        #Frame de Titre
        titleFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=90)
        titleFrame.grid_propagate(0)
        titleFrame.place(x=330, y=30)

        #Labels - Titre
        lblTitre = Label(titleFrame, text="Application 1 : Détermination du Réseau", font = 'Times 14 underline' )
        lblTitre.place(x=10, y=10)
        lblExo = Label(titleFrame, fg='blue', text="Sur base d’une IP et d’un masque (facultatif), fournit l’adresse de réseau et le broadcast\ndu réseau. Si une découpe en sous-réseau est réalisée, détermine l’adresse du sous-réseau.", font = 'Times 11 italic', justify="left" )
        lblExo.place(x=10, y=40)

        #Frame - Reponses
        self.repFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=300)
        self.repFrame.grid_propagate(0)

        self.rep = StringVar()
        lblVerif = Label(self.repFrame, textvariable=self.rep, justify="center", fg="red")
        lblVerif.place(x=0, y=0)

    def trouverReseau(self) -> None :
        """
        Récupere Ip, Masque. Défini le réseau et le broadcast. Défini le sous-réseau si besoin.
        """

        self.attStr.set("")
        self.repFrame.place_forget()

        # Champ d'IP vide
        if (self.textIp.get() == ""):
            self.attStr.set("(*) Champ requis : IP" )
            return
        
        # Instance de Reseau
        res = Reseau(self.textIp.get(), self.textMasque.get())

        # Vérification des champs
        if (res.ip == "0.0.0.0"):
            self.attStr.set("Adresse IP non-valide")
        elif (res.masque == "0.0.0.0" and self.textMasque.get() != ""):
            self.attStr.set("Masque Réseau non-valide")
        else:
            host = ipaddress.IPv4Address(res.ip)
            net = ipaddress.IPv4Network(res.ip + '/' + res.masque, False)
            self.rep.set("Adresse IP  : "+res.ip+"\nMasque de réseau : "+res.masque+"\nAdresse de réseau : "+f'{ipaddress.IPv4Address(int(host) & int(net.netmask)):s}'+"\nAdresse de broadcast : "+f'{net.broadcast_address:s}')
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
        self.repFrame.place_forget()
        




class Application2(Frame):
    """
    Sur base d’une adresse IP et de son masque et d’une adresse de réseau, le 
    programme doit déterminer si l’IP appartient au réseau ou pas. 
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Frame - Données d'entrée
        self.infoFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        self.infoFrame.grid_propagate(0)
        self.infoFrame.config(width=270, height=210)

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
        titleFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=90)
        titleFrame.grid_propagate(0)
        titleFrame.place(x=330, y=30)

        # Labels - Titre
        lblTitre = Label(titleFrame, text="Application 2 : Présence d'une IP dans le réseau", font = 'Times 14 underline' )
        lblTitre.place(x=10, y=10)
        lblExo = Label(titleFrame, fg='blue', text="Sur base d’une IP, d’une adresse de réseau (et d'un masque si découpé en sous-réseau),\nvérifie si l’adresse IP donnée appartient au réseau ou pas. ", font = 'Times 11 italic', justify="left" )
        lblExo.place(x=10, y=40)


        # Frame - Réponses
        self.repFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=300)
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
        else:
            # TODO  : Vérification de l'appartenance de l'ip au réseau
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


class Application3(Frame):
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
        Frame.__init__(self, parent)

        # Frame - Données d'entrée
        self.infoFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        self.infoFrame.grid_propagate(0)
        self.infoFrame.config(width=270, height=250)

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
        titleFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=90)
        titleFrame.grid_propagate(0)
        titleFrame.place(x=330, y=30)

        # Labels - Titre
        lblTitre = Label(titleFrame, text="Application 3 : Création de Sous-Réseaux", font = 'Times 14 underline' )
        lblTitre.place(x=10, y=10)
        lblExo = Label(titleFrame, fg='blue', text="Sur base d’une adresse de réseau et d'informations sur les sous-résaux souhaités,\ncrée une une découpe en sous-réseau classique si possible et fournit un plan d'adressage complet.", font = 'Times 11 italic', justify="left" )
        lblExo.place(x=10, y=40)


        # Frame - Réponses
        self.repFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=300)
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
        self.repFrame.place_forget()
        if hasattr(self, 'tableFrame'):
            self.tableFrame.place_forget()

        #en fonction du nombre de champs requis, on redimensionne la frame
        if (self.textReseau.get() == "" and self.textSR.get() == "" and self.textHotes.get() == ""):
            self.infoFrame.config(height=300)
        elif (self.textReseau.get() == "" and self.textSR.get() == ""):
            self.infoFrame.config(height=290)
        elif (self.textReseau.get() == "" and self.textHotes.get() == ""):
            self.infoFrame.config(height=290)
        elif (self.textSR.get() == "" and self.textHotes.get() == ""):
            self.infoFrame.config(height=290)
        elif (self.textReseau.get() == "" or self.textSR.get() == "" or self.textHotes.get() == ""):
            self.infoFrame.config(height=270)
        else:
            self.infoFrame.config(height=250)

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
            # TODO  :  Création des sous-réseaux
            self.repFrame.place(x=330, y=150)


            #define a frame that will contian the table and scrollbar
            self.tableFrame = Frame(self, width=600, height=150)
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

    def __init__(self, ip: str, masque: str = "-1", adrReseau: str = "0.0.0.0") -> None:
        if (Reseau.ipValide(ip)):
            self.ip: str = ip
        else:
            self.ip: str = "0.0.0.0"
        if (Reseau.masqueValide(masque)):
            self.masque: str = masque
        else:
            self.masque: str = "0.0.0.0"
        if (Reseau.reseauValide(adrReseau)):
            self.adrReseau: str = adrReseau
        else:
            self.adrReseau: str = "0.0.0.0"
        
        self.adrBroadCast: str = "0.0.0.0"
        self.adrSR: str = "0.0.0.0"

        print(self.ip, self.masque, self.adrReseau, self.adrBroadCast, self.adrSR)
        
    def ipValide(ip: str) -> bool:
        try:
            ip_object = ipaddress.ip_address(ip) 
            octets = ip.strip().lower().split('.')
            if(octets[0]=="127" or octets[0]=="0" or octets[0]>="224"):
                return False
            return True
        except ValueError:
            return False

    def masqueValide(masque: str) -> bool:
        octets = masque.strip().lower().split('.')

        # Check if there are exactly 4 octets
        if len(octets) != 4:
            return False
        
        # Initialize a flag to track contiguous 1s
        contiguous_ones = True

        for octet in octets:
            try:
                # Convert the octet to an integer
                octet_value = int(octet)

                # Check if the octet is within the valid range [0, 255]
                if octet_value < 0 or octet_value > 255:
                    return False
                
                # Check if the octet is 255 (contiguous 1s)
                if contiguous_ones:
                    if octet_value != 255:
                        i=1
                        while(i!=512):
                            if(256-i!=octet_value):
                                i+=i
                            else:
                                break
                        if(i==512):
                            return False
                        contiguous_ones = False
                else:
                    # Check if the octet is 0 (contiguous 0s)
                    if octet_value != 0:
                        return False
                    
            except ValueError:
                # If an octet is not a valid integer, return False
                return False
            
        # Check if there is at least one octet with contiguous 0s
        if contiguous_ones:
            return False
        
        return True

    def convertMasque(masque: str) -> str:
        octets = masque.strip().lower().split('.')
        total=0
        for o in octets:
            if o == 255:
                total+=8
            elif o == 0:
                pass
            else:
                match o:
                    case 128:
                        total+=1
                    case 192:
                        total+=2
                    case 224:
                        total+=3
                    case 240:
                        total+=4
                    case 248:
                        total+=5
                    case 252:
                        total+=6
                    case 254:
                        total+=7
        return "/"+str(total)
            
    def reseauValide(adrReseau: str) -> bool:
        return True
    

class Connexion(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Frame - Connexion
        self.inFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        self.inFrame.grid_propagate(0)
        self.inFrame.config(width=270, height=253)

        # Labels - Connexion
        labnomC = Label(self.inFrame, text="Connexion", font = 'Times 14 underline' ).grid(row = 0, column = 0, columnspan=2, padx = 10, pady = 10)

        labIdC = Label(self.inFrame, text="Identifiant * : ", width=15).grid(row = 2, column = 0, padx = 10, pady = 10)
        labPassC = Label(self.inFrame, text="Mot de passe * : ", width=15).grid(row = 3, column = 0, padx = 10, pady = 10)

        # Entries - Connexion
        self.textIdC = Entry(self.inFrame, width=20)
        self.textIdC.grid(row = 2, column = 1, pady = 10)
        self.textPassC = Entry(self.inFrame, width=20, show="*")
        self.textPassC.grid(row = 3, column = 1, pady = 10)

        # Errors - Connexion
        self.attStrC = StringVar()
        self.attStrC.set("")
        lblVerifC = Label(self.inFrame, textvariable=self.attStrC, justify="center", fg="red")
        lblVerifC.grid(row = 4, column = 0, columnspan=2, padx = 10, pady = 10)

        # Buttons - Connexion
        btnCheckC = Button(self.inFrame, text="Se Connecter", cursor="hand2")
        btnCheckC.config(command= lambda: self.connect())
        btnCheckC.grid(row = 5, column = 0, columnspan=2, padx = 10, pady = 10)

        self.inFrame.place(x=30, y=30)

        # Frame - Sign Up
        self.upFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        self.upFrame.grid_propagate(0)
        self.upFrame.config(width=270, height=253)

        # Labels - Sign Up
        labPassU = Label(self.upFrame, text="Creation de compte", font = 'Times 14 underline' ).grid(row = 0, column = 0, columnspan=2, padx = 10, pady = 10)

        labIdU = Label(self.upFrame, text="Identifiant * : ", width=15).grid(row = 2, column = 0, padx = 10, pady = 10)
        labPassU = Label(self.upFrame, text="Mot de passe * : ", width=15).grid(row = 3, column = 0, padx = 10, pady = 10)
        labPassU = Label(self.upFrame, text="Réécrire le MDP * : ", width=15).grid(row = 4, column = 0, padx = 10, pady = 10)

        # Entries - Sign Up
        self.textIdU = Entry(self.upFrame, width=20)
        self.textIdU.grid(row = 2, column = 1, pady = 10)
        self.textPassU = Entry(self.upFrame, width=20, show="*")
        self.textPassU.grid(row = 3, column = 1, pady = 10)
        self.textVerifU = Entry(self.upFrame, width=20, show="*")
        self.textVerifU.grid(row = 4, column = 1, pady = 10)

        # Errors - Sign Up
        self.attStrU = StringVar()
        self.attStrU.set("")
        lblVerifU = Label(self.upFrame, textvariable=self.attStrU, justify="center", fg="red")
        lblVerifU.grid(row = 5, column = 0, columnspan=2, padx = 10, pady = 10)

        # Buttons - Sign Up
        btnCheck = Button(self.upFrame, text="Créer un compte", cursor="hand2")
        btnCheck.config(command= lambda: self.createAccount())
        btnCheck.grid(row = 6, column = 0, columnspan=2, padx = 10, pady = 10)

        self.upFrame.place(x=330, y=30)

    def createAccount(self) :
        userId = self.textIdU.get()
        userPassword = self.textPassU.get()
        passwordConfirmation = self.textVerifU.get()
        

        if (userId == "" or userPassword == "" or passwordConfirmation == ""):
            self.attStrU.set("(*) Tous les champs sont requis")
            return
        
        if (userPassword != passwordConfirmation):
            self.attStrU.set("Les mots de passe ne correspondent pas")
            return

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(userId)])
        if c.fetchall():
            self.attStrU.set("Ce nom d'utilisateur existe déjà")
        else:
            hashed_password = bcrypt.hashpw(userPassword.encode('utf8'), bcrypt.gensalt())

            c.execute("INSERT INTO user (username,password) VALUES (?,?)", (userId, hashed_password))
            conn.commit()
            setConnected()

        c.close()
        conn.close()
        return
        
    def connect(self):
        userId = self.textIdC.get()
        userPassword = self.textPassC.get()
        if (userId == "" or userPassword == ""):
            self.attStrC.set("(*) Tous les champs sont requis")
            return

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(userId)])

        result = c.fetchall()
        if result:
            if bcrypt.checkpw(userPassword.encode('utf8'), result[0][2]):
                self.attStrC.set("Connexion réussie")
                setConnected()

            else:
                self.attStrC.set("Mot de passe incorrect")

        else:
            self.attStrC.set("Nom d'utilisateur incorrect")

        c.close()
        conn.close()
        return

    def reset(self):
        self.textIdC.delete(0, END)
        self.textPassC.delete(0, END)
        self.textIdU.delete(0, END)
        self.textPassU.delete(0, END)
        self.textVerifU.delete(0, END)
        self.attStrC.set("")
        self.attStrU.set("")

# Start
app = MainApplication()
app.mainloop()

