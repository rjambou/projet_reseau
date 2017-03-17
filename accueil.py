#!/usr/bin/env python
#-*-coding: utf8-*

from Tkinter import *
import graphical_claire

def accueil():
	fenetre=Tk()		#création fenetre
	fenetre.geometry("800x600+300+0")

	champ_label = Label(fenetre, text="Accueil", fg="black", font=("Bonjour", 20), bg="white", anchor="center")
	champ_label.place(x=0, y=0)
	champ_label.pack()

	def connexion():
		graphical_claire.fenetreauth(True)
		return 0

	def enregistrement():
		graphical_claire.fenetresave(True, True, True, True, True)
		return 0

#bouton "Se connecter"
	bouton_valider=Button(fenetre, text="Se connecter", command=connexion, font=16)
	bouton_valider.pack()
	bouton_valider.place(x=150, y=100)

#bouton "S'enregistrer"
	bouton_valider=Button(fenetre, text="S'enregistrer", command=enregistrement, font= 16)
	bouton_valider.pack()
	bouton_valider.place(x=500, y=100)

	fenetre.mainloop()

	return 0

print accueil()