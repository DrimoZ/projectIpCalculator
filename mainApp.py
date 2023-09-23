from tkinter import *
import ipaddress

### GROUPE 5 

PAD_X = 30
PAD_Y = 30
SIZE_X = 1000
SIZE_Y = 560

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
        returnButton = Button(self, text="Retourner au menu", command=lambda : self.show_frame(HomePage), cursor="hand2").place(x=10, y=SIZE_Y-35)

        self.frames = {} 
        for F in (HomePage, Application1, Application2, Application3):
  
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(HomePage)
  
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
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
            ["Application 1", "aelskdbsdoilbkjsdbfjkqswbdfn\n <e<sljd<bfzeoimlwbfdjghzioqermdfbwljgv\n <osurdjlwfxbgs\n sfngxoubjrlsdfxcmiho<sbjl:dwxfc\n fhid os<mlfheoioi\n fhfi hdm<ifnogbd"],
            ["Application 2", "aelskdbsdoilbkjsdbfjkqswbdfn\n <e<sljd<bfzeoimlwbfdjghzioqermdfbwljgv\n <osurdjlwfxbgs\n sfngxoubjrlsdfxcmiho<sbjl:dwxfc\n fhid os<mlfheoioi\n fhfi hdm<ifnogbd"],
            ["Application 3", "aelskdbsdoilbkjsdbfjkqswbdfn\n <e<sljd<bfzeoimlwbfdjghzioqermdfbwljgv\n <osurdjlwfxbgs\n sfngxoubjrlsdfxcmiho<sbjl:dwxfc\n fhid os<mlfheoioi\n fhfi hdm<ifnogbd"]
        ]

        for i in range(0, len(list)):
            self.grid_columnconfigure(i, weight=1)
            frame = Frame(self, highlightbackground="red", highlightthickness=1)


            label = Label(frame, text = list[i][1], font = 'Verdana 9', borderwidth=1, relief="solid", justify="center")
            label.grid(row = 1, column = 0, padx = 10, pady = 10)

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
        infoFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        infoFrame.grid_propagate(0)
        infoFrame.config(width=270, height=170)

        # Labels
        labIp = Label(infoFrame, text="IP * : ", justify="left").grid(row = 1, column = 0, padx = 10, pady = 10)
        labMasque = Label(infoFrame, text="Masque : ", justify="left").grid(row = 2, column = 0, padx = 10, pady = 10)

        # Entries
        textIp = Entry(infoFrame, width=25)
        textIp.grid(row = 1, column = 1, padx = 10, pady = 10)
        textIp.insert(0, "0.0.0.0")
        textMasque = Entry(infoFrame, width=25)
        textMasque.grid(row = 2, column = 1, padx = 10, pady = 10)
        textMasque.insert(0, "0.0.0.0")

        # Label d'erreur
        attStr = StringVar()
        attStr.set("")
        lblVerif = Label(infoFrame, textvariable=attStr, justify="center", fg="red")
        lblVerif.grid(row = 4, column = 0, columnspan=2, padx = 10, pady = 10)

        # Bouton de vérification
        btnCheck = Button(infoFrame, text="Trouver le réseau", cursor="hand2") 
        #btnCheck.config(command= lambda: checkReseau())
        btnCheck.grid(row = 5, column = 1, padx = 10, pady = 10)

        # Fin de la Frame d'entrée
        infoFrame.place(x=30, y=30)


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
        repFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=300)
        repFrame.grid_propagate(0)

        rep = StringVar()
        rep.set("OUI")
        lblVerif = Label(repFrame, textvariable=rep, justify="center", fg="red")
        lblVerif.place(x=0, y=0)




        # Fonction de reset de la frame
        def reset(self) -> None:
            pass
        




class Application2(Frame):
    """
    Sur base d’une adresse IP et de son masque et d’une adresse de réseau, le 
    programme doit déterminer si l’IP appartient au réseau ou pas. 
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Frame - Données d'entrée
        infoFrame = Frame(self, highlightbackground="black", highlightthickness=1)
        infoFrame.grid_propagate(0)
        infoFrame.config(width=270, height=210)

        # Labels - Données d'entrée
        labIp = Label(infoFrame, text="IP * : ", justify="left").grid(row = 1, column = 0, padx = 10, pady = 10)
        labMasque = Label(infoFrame, text="Masque : ", justify="left").grid(row = 2, column = 0, padx = 10, pady = 10)
        labReseau = Label(infoFrame, text="Réseau * : ", justify="left").grid(row = 3, column = 0, padx = 10, pady = 10)

        # Entries - Données d'entrée
        textIp = Entry(infoFrame, width=25)
        textIp.grid(row = 1, column = 1, padx = 10, pady = 10)
        textIp.insert(0, "0.0.0.0")
        textMasque = Entry(infoFrame, width=25)
        textMasque.grid(row = 2, column = 1, padx = 10, pady = 10)
        textMasque.insert(0, "0.0.0.0")
        textReseau = Entry(infoFrame, width=25)
        textReseau.grid(row = 3, column = 1, padx = 10, pady = 10)
        textReseau.insert(0, "0.0.0.0")

        # Errors - Données d'entrée
        attStr = StringVar()
        attStr.set("")
        lblVerif = Label(infoFrame, textvariable=attStr, justify="center", fg="red")
        lblVerif.grid(row = 4, column = 0, columnspan=2, padx = 10, pady = 10)

        # Buttons - Données d'entrée
        btnCheck = Button(infoFrame, text="Verifier l'adresse Ip", cursor="hand2")
        btnCheck.config(command= lambda: checkReseau())
        btnCheck.grid(row = 5, column = 1, padx = 10, pady = 10)

        # Fin de la Frame d'entrée
        infoFrame.place(x=30, y=30)


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
        repFrame = Frame(self, highlightbackground="black", highlightthickness=1, width=SIZE_X-360, height=300)
        repFrame.grid_propagate(0)

        # Labels - Titre
        rep = StringVar()
        rep.set("OUI")
        lblVerif = Label(repFrame, textvariable=rep, justify="center", fg="red")
        lblVerif.place(x=0, y=0)


        def checkReseau() -> None :
            """
            Récupere Ip, Masque et Réseau entrés. Vérifie que tout soit valide. Explique si l'Ip fait partie du Réseau donné. 
            """
            attStr.set("")
            repFrame.place_forget()

            # Un des champs est vide
            if (textIp.get() == ""):
                attStr.set("(*) Veuillez entrer une adresse IP")
                return
            elif (textReseau.get() == ""):
                attStr.set("(*) Veuillez entrer une adresse de réseau")
                return

            # Instance de Reseau
            res = Reseau(textIp.get(), textMasque.get(), textReseau.get())

            # Vérification des champs
            if (res.ip == "0.0.0.0"):
                attStr.set("Adresse IP non-valide")
            elif (res.masque == "0.0.0.0"):
                attStr.set("Masque Réseau non-valide")
            elif (res.adrReseau == "0.0.0.0"):
                attStr.set("Adresse Réseau non-valide")
            else:
                repFrame.place(x=330, y=150)
        
        # Fonction de reset de la frame
        def reset(self) -> None:
            attStr.set("")
            textIp.delete(0, END)
            textMasque.delete(0, END)
            textReseau.delete(0, END)


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





        # Fonction de reset de la frame
        def reset(self) -> None:
            pass


class Reseau():
    """
    Reprend toutes les informations et méthodes de verification/recherche/etc de réseau ou ip. 
    - Adresse Ip
    - Masque du Réseau
    - Adresse du Réseau
    - Adresse de Broadcast
    - Adresse du Sous Réseau
    """

    def __init__(self, ip, masque, adrReseau="0.0.0.0") -> None:
        if (Reseau.ipValide(ip)):
            self.ip = ip
        else:
            self.ip = "0.0.0.0"
        if (Reseau.masqueValide(masque)):
            self.masque = masque
        else:
            self.masque = "0.0.0.0"
        if (Reseau.reseauValide(adrReseau)):
            self.adrReseau = adrReseau
        else:
            self.adrReseau = "0.0.0.0"
        
        self.adrBroadCast = "0.0.0.0"
        self.adrSR = "0.0.0.0"
        
    def ipValide(ip) -> bool:
        return True

    def masqueValide(masque) -> bool:
        return True
#         octets = subnet_mask.split('.')

#     # Check if there are exactly 4 octets
#     if len(octets) != 4:
#         return False

#     # Initialize a flag to track contiguous 1s
#     contiguous_ones = True

#     for octet in octets:
#         try:
#             # Convert the octet to an integer
#             octet_value = int(octet)

#             # Check if the octet is within the valid range [0, 255]
#             if octet_value < 0 or octet_value > 255:
#                 return False

#             # Check if the octet is 255 (contiguous 1s)
#             if contiguous_ones:
#                 if octet_value != 255:
#                     contiguous_ones = False
#             else:
#                 # Check if the octet is 0 (contiguous 0s)
#                 if octet_value != 0:
#                     return False
#         except ValueError:
#             # If an octet is not a valid integer, return False
#             return False

#     # Check if there is at least one octet with contiguous 0s
#     if contiguous_ones:
#         return False

#     return True

# # Get the subnet mask from the user
# subnet_mask = input("Enter a subnet mask in the format xxx.xxx.xxx.xxx: ")

# # Remove leading and trailing spaces and convert to lowercase for case-insensitivity
# subnet_mask = subnet_mask.strip().lower()

# # Check if it's a valid subnet mask
# if is_valid_subnet_mask(subnet_mask):
#     print("Valid subnet mask")
# else:
#     print("Invalid subnet mask")


    def reseauValide(adrReseau) -> bool:
        return True
    
  
# Start
app = MainApplication()
app.mainloop()