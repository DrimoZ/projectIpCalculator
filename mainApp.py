from tkinter import *

### GROUPE 5 

H_PADDING = 175
V_PADDING = 100
  
class MainApplication(Tk):
    """
    Main Application Class - Root
    """ 

    def __init__(self, *args, **kwargs):
         
        Tk.__init__(self, *args, **kwargs)
        self.geometry("1280x720")
        self.title("Réseau - Vérificateur d'IP")
         
        # creating a container
        container = Frame(self) 
        container.pack(anchor=CENTER, fill = "both", expand = True, padx=H_PADDING, pady=V_PADDING)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        quitButton = Button(self, text="Quitter l'application", command=self.destroy).place(x=1145, y=680)
        returnButton = Button(self, text="Retourner au menu", command=lambda : self.show_frame(HomePage)).place(x=15, y=680)

        self.frames = {} 
        for F in (HomePage, Application1, Application2, Application3):
  
            frame = F(container, self)
            frame.config(highlightbackground="blue", highlightthickness=2)

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
            frame.grid(row = 1, column = i, padx = 10, pady = 10)


            label = Label(frame, text = list[i][1], font = 'Verdana 9', borderwidth=1, relief="solid", justify="center")
            label.grid(row = 1, column = 0, padx = 10, pady = 10)

            appButton = Button(frame, text =list[i][0], borderwidth=1, relief="solid")
            if (i == 0):
                appButton.config(command = lambda : controller.show_frame(Application1))
            elif (i == 1):
                appButton.config(command = lambda : controller.show_frame(Application2))
            elif (i == 2):
                appButton.config(command = lambda : controller.show_frame(Application3))

            appButton.grid(row = 2, column = 0, padx = 10, pady = 10)

        
  
        ## button to show frame 2 with text layout2
        # button2 = Button(self, text ="Application 2",
        # command = lambda : controller.show_frame(HomePage),borderwidth=1, relief="solid")
        # button2.grid(row = 1, column = 1, padx = 10, pady = 10)

        ## button to show frame 3 with text layout1
        # button2 = Button(self, text ="Application 2",
        # command = lambda : controller.show_frame(HomePage),borderwidth=1, relief="solid")
        # button2.grid(row = 1, column = 2, padx = 10, pady = 10)


  
class Application1(Frame):
    """
    En classfull uniquement, sur base d’une adresse IP et d’un masque, le 
    programme doit fournir l’adresse de réseau et l’adresse de broadcast du 
    réseau. Si une découpe en sous-réseau est réalisée, le programme doit 
    déterminer l’adresse de SR
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)




class Application2(Frame):
    """
    Sur base d’une adresse IP et de son masque et d’une adresse de réseau, le 
    programme doit déterminer si l’IP appartient au réseau ou pas. 
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)




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



class Reseau():
    """
    Reprend toutes les informations et méthodes de verification/recherche/etc de réseau ou ip. 
    - Adresse Ip
    - Masque du Réseau
    - Adresse du Réseau
    - Adresse de Broadcast
    - Adresse du Sous Réseau
    """

    def __init__(self, ip, masque) -> None:
        if (Reseau.ipValide(ip)):
            self.ip = ip
        else:
            self.ip = "0.0.0.0"
        if (Reseau.masqueValide(masque)):
            self.masque = masque
        else:
            self.masque = "0.0.0.0"
        
        self.adrReseau = "0.0.0.0"
        self.adrBroadCast = "0.0.0.0"
        self.adrSR = "0.0.0.0"
        
    def ipValide(ip) -> bool:
        pass

    def masqueValide(masque) -> bool:
        pass
    

  
# Start
app = MainApplication()
app.mainloop()