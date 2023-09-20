import tkinter as tk
import webbrowser

# Fonction pour ouvrir une URL dans un navigateur
def ouvrir_url():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Remplacez ceci par l'URL que vous souhaitez ouvrir
    webbrowser.open(url)

# Fonctions pour afficher différentes pages
def afficher_page1():
    canvas.delete("page")
    canvas.delete("special")
    canvas.create_text(150, 50, text="Page 1", font=("Helvetica", 24), tags="page")

    bouton=tk.Button(canvas, text="Cliquez-moi", command=ouvrir_url)
    canvas.create_window(150, 100, window=bouton, tags="special")

def afficher_page2():
    canvas.delete("page")
    canvas.delete("special")
    canvas.create_text(150, 50, text="Page 2", font=("Helvetica", 24), tags="page")

def afficher_page3():
    canvas.delete("page")
    canvas.delete("special")
    canvas.create_text(150, 50, text="Page 3", font=("Helvetica", 24), tags="page")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Interface avec 3 pages")

# Créer un canevas pour afficher les pages
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Créer les boutons pour chaque page
button1 = tk.Button(root, text="Page 1", command=afficher_page1)
button2 = tk.Button(root, text="Page 2", command=afficher_page2)
button3 = tk.Button(root, text="Page 3", command=afficher_page3)

# Placer les boutons dans la fenêtre
button1.pack()
button2.pack()
button3.pack()

# Afficher la page par défaut (page 1)
afficher_page1()

# Lancer la boucle principale
root.mainloop()