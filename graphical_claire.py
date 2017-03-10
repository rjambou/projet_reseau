#!/usr/bin/env python
#-*-coding: utf8-*

#Probleme
#boucle infinie si donnees entrees erronnees
#creation compte aucune reponse
#nom apparition du mdp en claire

#A faire
#Lien Pierre
#Ameliorer design

from Tkinter import *
import connexion_claire

command=""

def fenetreauth(correct, blank, length, nb, lt):
	def valider():
		global command
		global username
		global mdp
		command="login"
		username=Login_texte.get()
		mdp=Mdp_texte.get()
		return 0

	def enregistrer():
		global command
		global username
		global mdp
		command="register"
		username=Login_texte.get()
		mdp=Mdp_texte.get()
		return 0

	fenetre=Tk()		#création fenetre
	fenetre.geometry("800x600+300+0")

	champ_label = Label(fenetre, text="Authentification", fg="black", font=("Bonjour", 16), bg="white", anchor="center")
	champ_label.place(x=0, y=0)
	champ_label.pack()		#affiche le label ds la fenetre

	#Login
	Login= Label(fenetre, text="Login", fg="black", font=("Login", 12), bg="white", anchor="center")
	Login.pack()
	Login.place(x=0, y=30)

	var_text=StringVar()
	Login_texte=Entry(fenetre, textvariable=var_text, width=100)
	Login_texte.pack()
	Login_texte.place(x=0, y=60)

	#Mot de passe
	Mdp = Label(fenetre, text="Mot de passe", fg="black", font=("mdp", 12), bg="white", anchor="center")
	Mdp.pack()
	Mdp.place(x=0, y=90)

	var_text=StringVar()
	Mdp_texte=Entry(fenetre, textvariable=var_text, width=100)
	Mdp_texte.pack()
	Mdp_texte.place(x=0, y=120)

	#Valider
	bouton_valider=Button(fenetre, text="Valider", command=valider)
	bouton_valider.pack()
	bouton_valider.place(x=150, y=150)

	#Register
	bouton_register=Button(fenetre, text="Enregistrer", command=enregistrer)
	bouton_register.pack()
	bouton_register.place(x=50, y=150)

	#Quitter
	bouton_quitter=Button(fenetre, text="Quitter", command=fenetre.quit)
	bouton_quitter.pack()
	bouton_quitter.place(x=250, y=150)

	if not correct:
		authnotcorrect= Label(fenetre, text="Login ou mot de passe incorrect", fg="black", font=("Login", 12), bg="white", anchor="center")
		authnotcorrect.pack()
		authnotcorrect.place(x=0, y=200)

	if not blank:
		notblank= Label(fenetre, text="Login ou mot de passe vide", fg="black", font=("Login", 12), bg="white", anchor="center")
		notblank.pack()
		notblank.place(x=0, y=200)

	if not length:
		notlength= Label(fenetre, text="Votre mot de passe doit contenir au moins 8 caractères", fg="black", font=("Login", 12), bg="white", anchor="center")
		notlength.pack()
		notlength.place(x=0, y=200)

	if not nb:
		notnb= Label(fenetre, text="Votre mot de passe doit contenir au moins 1 nombre", fg="black", font=("Login", 12), bg="white", anchor="center")
		notnb.pack()
		notnb.place(x=0, y=200)

	if not lt:
		notlt= Label(fenetre, text="Votre mot de passe doit contenir au moins 1 lettre", fg="black", font=("Login", 12), bg="white", anchor="center")
		notlt.pack()
		notlt.place(x=0, y=200)

	fenetre.mainloop()

	return command, username, mdp