#!/usr/bin/python

from Tkinter import *
import accueil
import os
import tkFileDialog

logo=True
gestion=True
ouvrir=0
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
		rep=tkFileDialog.askopenfilename(title="gestionnaire de fichier", initialdir=current, initialfile="", multiple=True, filetypes=[("All","*")])
		rep1=rep[0].split("/")
		nom=rep1[-1]
		gestion=False
		ouvrir=1
		fenetre.destroy()
		return gestion, ouvrir, nom


# Creation de la fenetre principale (main window)
	Mafenetre = Tk()

	Mafenetre.geometry("800x600+300+0")
	Mafenetre.title("Client")
	Mafenetre['bg']='bisque'


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
	print(logo)
	print(gestion)
	print(ouvrir)
	print(nom)
	return logo, gestion, ouvrir, nom
#current_dir=os.getcwd()
#current=os.chdir(current_dir)
#print(interface(current, "CH"))