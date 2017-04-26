#!/usr/bin/python

from Tkinter import *
import accueil
import os
import tkFileDialog

option=0
ouvrir=0
nom = True
recipient=0
subject=0
context=0

def interface(current, login):
	def commande():
		print("()")
	def logout():
		global option
		option="logout"
		Mafenetre.destroy()
		return option

	def openfile():
		global rep, nom, option, ouvrir
		nom=tkFileDialog.askopenfilename(title="Ouvrir un document")
		option="rapport"
		Mafenetre.destroy()
		return option, nom

	def create():
		def valider():
			nom=nom_texte.get()
			ft2.destroy()
			return 0
		global rep, nom, option, ouvrir
		ft2=Tk()
		Nom = Label(ft2, text="Creation nouveau fichier", fg="black", font=("mdp", 14), bg="white", anchor="center")
		Nom.pack()
		Nom.place(x=0, y=90)

		var_text=StringVar()
		nom_texte=Entry(ft2, textvariable=var_text, width=100)
		nom_texte.pack()
		nom_texte.place(x=0, y=120)
			#Valider
		bouton_valider=Button(ft2, text="Valider", command=valider)
		bouton_valider.pack()
		bouton_valider.place(x=150, y=150)
		option="gestion"
		ouvrir=1
		Mafenetre.destroy()
		print("nom", str(nom))
		return option, nom, ouvrir

	def sendm():
		def valider():
			global recipient, subject, context
			recipient=A_texte.get()
			subject=Objet_texte.get()
			context=Corps_mail_texte.get()
			ft2.destroy()
			return recipient, subject, context
		ft2=Tk()
		ft2.geometry("700x500+200+0")
		ft2['bg']='bisque'
		global option, recipient, subject, context
		Envoi = Label(ft2, text="Envoyer un mail", fg="black", font=("mdp", 14), bg="white", anchor="center")
		Envoi.pack()
		Envoi.place(x=0, y=00)

		A= Label(ft2, text="A", fg="black", font=("A", 12), bg="white", anchor="center")
		A.pack()
		A.place(x=0, y=30)

		var_text=StringVar()
		A_texte=Entry(ft2, textvariable=var_text, width=100)
		A_texte.pack()
		A_texte.place(x=30, y=30)

		Objet= Label(ft2, text="Objet", fg="black", font=("Objet", 12), bg="white", anchor="center")
		Objet.pack()
		Objet.place(x=0, y=90)

		var_text=StringVar()
		Objet_texte=Entry(ft2, textvariable=var_text, width=100)
		Objet_texte.pack()
		Objet_texte.place(x=70, y=90)

		Corps_mail= Label(ft2, text="Corps mail", fg="black", font=("Corps mail", 12), bg="white", anchor="center")
		Corps_mail.pack()
		Corps_mail.place(x=0, y=120)

		var_text=StringVar()
		Corps_mail_texte=Entry(ft2, textvariable=var_text, width=100)
		Corps_mail_texte.pack()
		Corps_mail_texte.place(x=0, y=150)

		#Valider
		bouton_valider=Button(ft2, text="Valider", command=valider)
		bouton_valider.pack()
		bouton_valider.place(x=150, y=180)

		ft2.mainloop()

		option="send mail"
		return option, recipient, subject, context


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
	BoutonChangeDirectory = Button(Mafenetre, text ='Creer un fichier', command = create)
	BoutonChangeDirectory.pack()
	BoutonChangeDirectory.place(x=80, y=120)

# Creation d'un widget Visualize (bouton Vizualise)
	BoutonVisualize = Button(Mafenetre, text ='Ouvrir un fichier', command = openfile) 
	BoutonVisualize.pack()
	BoutonVisualize.place(x=80, y=160)

# Creation d'un widget Button (bouton List)
	BoutonList = Button(Mafenetre, text ='List', command = commande)
	BoutonList.pack()
	BoutonList.place( x=80, y= 200)

# Creation d'un widget Button (bouton SendMail)
	BoutonSend = Button(Mafenetre, text ='SendMail', command = sendm)
	BoutonSend.pack()
	BoutonSend.place( x=80, y= 240)

# Creation d'un widget Button (bouton ViewMail)
	BoutonView = Button(Mafenetre, text ='ViewMail', command = commande)
	BoutonView.pack()
	BoutonView.place( x=80, y= 280)

# Creation d'un widget Button (bouton Logout)
	BoutonLogout = Button(Mafenetre, text ='Logout', command = logout)
	BoutonLogout.pack()
	BoutonLogout.place( x=600, y= 50)


#Music()
	Mafenetre.mainloop()

	return option, ouvrir, nom, recipient, subject, context
#current_dir=os.getcwd()
#current=os.chdir(current_dir)
#print(interface(current, "CH"))
