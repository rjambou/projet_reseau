#!/usr/bin/python

from Tkinter import *
import accueil
import os
import tkFileDialog

logo=True
gestion=True
ouvrir=True
nom = True

def interface(current, login):
	def commande() :
		print()
	def logout():
		global logo
		logo=False
		Mafenetre.destroy()
		return logo

	def openfile():
		global rep, nom, gestion, ouvrir
		rep=tkFileDialog.askopenfilename(title="gestionnaire de fichier", nitialdir=current, initialfile="", multiple=True, filetypes=[("All","*")], parent=Mafenetre)
		rep1=rep[0].split("/")
		nom=rep1[-1]
		gestion=False
		ouvrir=False
		Mafenetre.destroy()
		return gestion, ouvrir, nom


# Creation de la fenetre principale (main window)
	Mafenetre = Tk()

	Mafenetre.geometry("800x600+300+0")
	Mafenetre.title("Client")
	Mafenetre['bg']='bisque'

#menu

	menubar = Menu(Mafenetre)

	menu1 = Menu(menubar, tearoff=0)
	menu1.add_command(label="Créer", command=alert)
	menu1.add_command(label="Editer", command=alert)
	menu1.add_separator()
	menu1.add_command(label="Quitter", command=fenetre.quit)
	menubar.add_cascade(label="Fichier", menu=menu1)

	menu2 = Menu(menubar, tearoff=0)
	menu2.add_command(label="Couper", command=alert)
	menu2.add_command(label="Copier", command=alert)
	menu2.add_command(label="Coller", command=alert)
	menubar.add_cascade(label="Editer", menu=menu2)

	menu3 = Menu(menubar, tearoff=0)
	menu3.add_command(label="A propos", command=alert)
	menubar.add_cascade(label="Aide", menu=menu3)

	fenetre.config(menu=menubar)


#Affichage du login  
	Label_login = Label(Mafenetre, text = login, fg = 'black',relief=GROOVE,  font = ("login",16), bg="white")
	Label_login['bg']='bisque'
	Label_login.pack()
	Label_login.place(x=80, y=40)

# Creation d'un widget Button (bouton Change Directory)
	BoutonChangeDirectory = Button(Mafenetre, text ='Change Directory', command = commande)
	BoutonChangeDirectory.pack()
	BoutonChangeDirectory.place(x=80, y=120)

# Creation d'un widget Visualize (bouton Vizualise)
	BoutonVisualize = Button(Mafenetre, text ='Visualize file', command = openfile) 
	BoutonVisualize.pack()
	BoutonVisualize.place(x=80, y=160)

# Creation d'un widget Button (bouton List)
	BoutonList = Button(Mafenetre, text ='List', command = commande)
	BoutonList.pack()
	BoutonList.place( x=80, y= 200)

# Creation d'un widget Button (bouton SendMail)
	BoutonList = Button(Mafenetre, text ='SendMail', command = commande)
	BoutonList.pack()
	BoutonList.place( x=80, y= 240)

# Creation d'un widget Button (bouton ViewMail)
	BoutonList = Button(Mafenetre, text ='ViewMail', command = commande)
	BoutonList.pack()
	BoutonList.place( x=80, y= 280)

# Creation d'un widget Button (bouton Logout)
	BoutonList = Button(Mafenetre, text ='Logout', command = logout)
	BoutonList.pack()
	BoutonList.place( x=600, y= 50)


#Music()
	Mafenetre.mainloop()

	envoyer=current_dir+"/"+nom
	#fichier=open(nom, "r")
	#envoyer=fichier.readlines()
	#print(envoyer)
	return logo, gestion, ouvrir, envoyer
current_dir=os.getcwd()
current=os.chdir(current_dir)
print(interface(current, "CH"))