#!/usr/bin/env python
#-*-coding: utf8-*

#To do list
#boucle infinie si donnees entrees erronnees
#gerer erreur mdp/login login()
##Lien Pierre
#Ameliorer design

from Tkinter import *
import connexion_claire

command=""

def fenetreauth(correct):

	def valider():
		global command
		global username
		global mdp
		command="login"
		username=Login_texte.get()
		mdp=Mdp_texte.get()
		fenetre.quit
		return 0

	fenetre=Tk()		#création fenetre
	fenetre.geometry("800x600+300+0")

	champ_label = Label(fenetre, text="Authentification", fg="black", font=("Bonjour", 16), bg="white", anchor="center")
	champ_label.place(x=0, y=0)
	champ_label.pack()		#affiche le label ds la fenetre

	#Login
	Login= Label(fenetre, text="Login", fg="black", font=("Login", 14), bg="white", anchor="center")
	Login.pack()
	Login.place(x=0, y=30)

	var_text=StringVar()
	Login_texte=Entry(fenetre, textvariable=var_text, width=100)
	Login_texte.pack()
	Login_texte.place(x=0, y=60)

	#Mot de passe
	Mdp = Label(fenetre, text="Mot de passe", fg="black", font=("mdp", 14), bg="white", anchor="center")
	Mdp.pack()
	Mdp.place(x=0, y=90)

	var_text=StringVar()
	Mdp_texte=Entry(fenetre, textvariable=var_text, width=100, show="*")
	Mdp_texte.pack()
	Mdp_texte.place(x=0, y=120)

	#Valider
	bouton_valider=Button(fenetre, text="Valider", command=valider)
	bouton_valider.pack()
	bouton_valider.place(x=150, y=150)

	#Quitter
	bouton_quitter=Button(fenetre, text="Quitter", command=fenetre.quit)
	bouton_quitter.pack()
	bouton_quitter.place(x=250, y=150)

	if not correct:
		authnotcorrect= Label(fenetre, text="Login ou mot de passe incorrect", fg="black", font=("Login", 12), bg="white", anchor="center")
		authnotcorrect.pack()
		authnotcorrect.place(x=0, y=200)

	fenetre.mainloop()

	return command, username, mdp






def fenetresave(blank, length, nb, lt, already_register, pwd, gr):

	def enregistrer():
		global command
		global username
		global mdp
		global mdp2
		global selection
		command="register"
		username=Login_texte.get()
		mdp=Mdp_texte.get()
		mdp2=Mdp2_texte.get()
		selection=tab_group[liste_group.curselection()[0]]
		fenetre.quit
		return 0

	fenetre2=Tk()		#création fenetre
	fenetre2.geometry("800x600+300+0")

	champ_label = Label(fenetre2, text="Enregistrement", fg="black", font=("Bonjour", 20), bg="white", anchor="center")
	champ_label.place(x=0, y=0)
	champ_label.pack()		#affiche le label ds la fenetre

	#Login
	Login= Label(fenetre2, text="Login", fg="black", font=("Login", 14), bg="white", anchor="center")
	Login.pack()
	Login.place(x=0, y=30)

	var_text=StringVar()
	Login_texte=Entry(fenetre2, textvariable=var_text, width=100)
	Login_texte.pack()
	Login_texte.place(x=0, y=60)

	#Mot de passe
	Mdp = Label(fenetre2, text="Mot de passe", fg="black", font=("mdp", 14), bg="white", anchor="center")
	Mdp.pack()
	Mdp.place(x=0, y=90)

	var_text=StringVar()
	Mdp_texte=Entry(fenetre2, textvariable=var_text, width=100, show="*")
	Mdp_texte.pack()
	Mdp_texte.place(x=0, y=120)

	#Mot de passe verification
	Mdp2 = Label(fenetre2, text="Vérification du mot de passe", fg="black", font=("mdp", 12), bg="white", anchor="center")
	Mdp2.pack()
	Mdp2.place(x=0, y=160)

	var_text=StringVar()
	Mdp2_texte=Entry(fenetre2, textvariable=var_text, width=100, show="*")
	Mdp2_texte.pack()
	Mdp2_texte.place(x=0, y=200)

	#Group
	group = Label(fenetre2, text="Group", fg="black", font=("mdp", 14), bg="white", anchor="center")
	group.pack()
	group.place(x=0, y=240)

	liste_group=Listbox(fenetre2)
	liste_group.pack()
	liste_group.place(x=0, y=270)
	tab_group=["doctor", "nurse", "secretary"]
	liste_group.insert(0, "Docteur")
	liste_group.insert(1, "Infirmier")
	liste_group.insert(2, "Secrétaire")

	#Register
	bouton_register=Button(fenetre2, text="Enregistrer", command=enregistrer)
	bouton_register.pack()
	bouton_register.place(x=50, y=400)

	#Quitter
	bouton_quitter=Button(fenetre2, text="Quitter", command=fenetre2.quit)
	bouton_quitter.pack()
	bouton_quitter.place(x=250, y=400)

	if not blank:
		notblank= Label(fenetre2, text="Login ou mot de passe vide", fg="black", font=("Login", 12), bg="white", anchor="center")
		notblank.pack()
		notblank.place(x=0, y=450)

	if not length:
		notlength= Label(fenetre2, text="Votre mot de passe doit contenir au moins 8 caractères", fg="black", font=("Login", 12), bg="white", anchor="center")
		notlength.pack()
		notlength.place(x=0, y=450)

	if not nb:
		notnb= Label(fenetre2, text="Votre mot de passe doit contenir au moins 1 nombre", fg="black", font=("Login", 12), bg="white", anchor="center")
		notnb.pack()
		notnb.place(x=0, y=450)

	if not lt:
		notlt= Label(fenetre2, text="Votre mot de passe doit contenir au moins 1 lettre", fg="black", font=("Login", 12), bg="white", anchor="center")
		notlt.pack()
		notlt.place(x=0, y=450)

	if not already_register:
		notlt= Label(fenetre2, text="Ces identifiants sont déjà utilisés", fg="black", font=("Login", 12), bg="white", anchor="center")
		notlt.pack()
		notlt.place(x=0, y=450)

	if not pwd:
		notpwd= Label(fenetre2, text="Mot de passe incorrect", fg="black", font=("Login", 12), bg="white", anchor="center")
		notpwd.pack()
		notpwd.place(x=0, y=450)

	if not gr:
		notgr= Label(fenetre2, text="Vous devez selectionner un groupe", fg="black", font=("Login", 12), bg="white", anchor="center")
		notgr.pack()
		notgr.place(x=0, y=450)

	fenetre2.mainloop()

	return command, username, mdp, mdp2, selection
#print fenetresave(True, True, True, True, True)
#print fenetreauth(True)