#!/usr/bin/python

from Tkinter import *
import accueil
import os

def interface(current, login):
	def commande() :
		print()
	def logout():
		global logo
		logo=False
		return logo

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

#Affichage du repertoire courant 
	current=str(current)
	Label_current_dir= Label(Mafenetre, text="current directory : "+ current, fg="black", font=("Login", 14), bg="white", anchor="center")
	Label_current_dir['bg']='bisque'
	Label_current_dir.pack()
	Label_current_dir.place(x=500, y=120)
	#str_current_dir= StringVar()
	#str_current_dir.set("current directory : " + current)
	#Label_current_dir = Label(Mafenetre, textvariable = str_current_dir, fg='black')
	#Label_current_dir['bg']='bisque'
	#Label_current_dir.pack()
	#Label_current_dir.place(x=600, y=120)



# Creation d'un widget Button (bouton Change Directory)
	BoutonChangeDirectory = Button(Mafenetre, text ='Change Directory', command = commande)
	BoutonChangeDirectory.pack()
	BoutonChangeDirectory.place(x=80, y=120)

# Creation d'un widget Visualize (bouton Vizualise)
	BoutonVisualize = Button(Mafenetre, text ='Visualize file', command = commande) 
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

	return logo, True
#current_dir=os.getcwd()
#current=os.chdir(current_dir)
#print(interface(current, "CH"))