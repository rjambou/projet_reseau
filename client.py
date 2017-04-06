#!/usr/bin/env python
#-*-coding: utf8-*
import subprocess as sub
import commands as cmd
import socket
import time
import os
import json
import sys
import getpass
import signal

current_dir=os.getcwd()
os.chdir(current_dir) #le path change automatiquement                    


def securite(password):
    if len(password)<8:
        print("Your password is not long enough. (8 caracters min.)")
        return False 
    chiffre=False
    lettre=False
    for i in password:
        if i.isdigit():
            chiffre=True
    for i in password:
        if i.isalpha():
            lettre=True
    if chiffre==False:
        print("Your password has to contain a number.")
        return False
    if lettre==False:
        print("Your password has to contain a letter.")
        return False
    return True



def login():
    print("Please enter your login")
    while True:
        username = raw_input("Username: ")
        s.send(username)
        username_exists=s.recv(BUFFER_SIZE)
        if username_exists=="true":
            break
        else:
            print("Invalid username, please try again.")
            continue
    while True:
        password = getpass.getpass("Password : ")
        if not len(password) > 0:
            print("Password can't be blank")
        else:
            break
    data = "login " + username + " " + password
    s.send(data)
    time.sleep(1)
    data=s.recv(BUFFER_SIZE)
    if data=="true":
        return session(username)
    elif data == "false":
        print("Invalid username or password! you redirect to home")

def register_client():
    continuer=True
    while continuer:
        username = raw_input("New username: ")
        if not len(username) > 0:
            print("Username can't be blank")
            continue
        else:
            s.send(username)
            verify=s.recv(BUFFER_SIZE)
            if verify=="true":
                continuer=False
            else:
                print("Username already in use. Please try again.")
    while True:
        password = getpass.getpass("Password : ")
        password2 = getpass.getpass("Re-enter password : ")
        if password!=password2 :
            print("Passwords don't match.\nPlease try again.\n")
            continue
        if not securite(password):
            print("Please try again.\n")
            continue
        else:
            break
    while True:
        liste_groupes=["doctor","nurse","secretary"] #liste des groupes disponibles : l'utilisateur devra réessayer tant qu'il n'entre pas un de ceux-là
        group = raw_input("choice your group (doctor, nurse, secretary) : ").lower() #avec .lower() la casse n'a pas d'importance
        if group not in liste_groupes:
            print("Ce groupe est invalide.")
            continue
        else:
            break
    print("Creating account...")
    data="register " + username + " " + password + " " + group
    s.send(data)
    time.sleep(1)
    data=s.recv(BUFFER_SIZE)
    if data=="uncreated":
        print("Username already use! Please recover your password or contact your administration")
        login()
    elif data == "created":
    	print("User " + username + " created")
    	login()

#arefaire


def sendmail_client(username):
    while True:
        recipient = raw_input("Recipient > ")
        if not len(recipient) > 0:
            print("Recipient can't be blank")
            continue
        s.send(recipient)
        time.sleep(1)
        valid=s.recv(BUFFER_SIZE)
        if valid=="false":
        	print("There is no account with that username")
        	continue
        else:
            break
    while True:
        subject = raw_input("Subject > ")
        if not len(subject) > 0:
            print("Subject can't be blank")
            continue
        else:
            break
    while True:
        context = raw_input("Context > ")
        if not len(context) > 0:
            print("Context can't be blank")
        else:
            break
    print("Sending mail...")
    s.send(subject)
    time.sleep(1)
    s.send(context)
    time.sleep(1)
    print("Mail has been sent to " + recipient)


def shell(data):                           
    a=sub.check_output(data, shell=True)
    if (a==''):
        a='commande reussie'
    return a

def sending(file):
    f=open(file,"rb")
    l = f.read(1024)
    while (l):
        print 'Sending...'
        s.send(l)
        l = f.read(1024)
    f.close()
    print "Done Sending"

def receiving(file):
    try:
        f=open(file,"w")
    except IOError :
        sub.call("touch " + file, shell=True )
    finally:
        l = s.recv(1024)
        while(l):
            print "receiving"
            f.write(l)
            l=s.recv(BUFFER_SIZE)
        f.close()


def session(username):
    current_dir=os.getcwd()
    os.chdir(current_dir) #le path change automatiquement                        
    data="session " + username
    s.send(data)
    time.sleep(1)
    print("Welcome to your account " + username)
    message_session=s.recv(BUFFER_SIZE)
    print(message_session)
    while True:
        print("Options: view mail | send mail | commande shell | gestion de fichier | logout")
        option = raw_input(username + " > ")
        s.send(option)
        time.sleep(1)
        if option == "logout":
        	print("Logging out...")
        	break
        elif option == "view mail":
            print("Current mail:")
            nombre_mail=s.recv(BUFFER_SIZE)
            print nombre_mail
            for i in range(int(nombre_mail)):
                mail=s.recv(BUFFER_SIZE)
                print(mail)
        elif option == "send mail":
        	sendmail_client(username)
        elif option == "commande shell":
        	commande=raw_input("Please enter your commande ! ")
        	s.send(commande)
        	time.sleep(1)
        	resultats=s.recv(BUFFER_SIZE)
        	print(resultats)
        elif option == "gestion de fichier":
            while True:
                print("Options: creer un rapport | lire un rapport | retour")
                option_fichier=raw_input(username + " > ")
                s.send(option_fichier)
                time.sleep(1)
                if option_fichier=="creer un rapport":#le fichier est enregister chez le client......a modifier
                    title=raw_input("Enter your title of file : ")
                    title=title+".odt"
                    s.send(title)
                    fichier=open(title,'w')
                    fichier.close()
                    data="libreoffice " + title
                    data=shell(data)
                    terminer=raw_input("Are you finished ? (Yes(Y) or No(N))")
                    while terminer!="Y":
                        time.sleep(1)
                        terminer=raw_input("Are you finished ? (Yes(Y) or No(N))")
                    sending(title)
                elif option_fichier=="lire un rapport":#le fichier est chez le client ...a modifier
                    commande=raw_input("Please enter your filename : ")
                    data="libreoffice " + commande + "*"
                    data=sub.call(data, shell=True)
                elif option_fichier=="retour":
                    break

        elif message_session.split(" ")[1] == "admin":
            if option == "user mail":
                print("Whos mail would you like to see?")
                userinfo = raw_input("> ")
                s.send(userinfo)
                time.sleep(1)
                info=s.recv(BUFFER_SIZE)
                if info=="true":
                    nombre_mail=s.recv(BUFFER_SIZE)
                    for i in range(int(nombre_mail)):
                        mail=s.recv(BUFFER_SIZE)
                        print(mail)
                else:
                    print("There is no account with that username")
                time.sleep(1)
           
            elif option == "delete mail":
                print("Whos mail would you like to delete?")
                userinfo = raw_input("> ")
                s.send(userinfo)
                time.sleep(1)
                info=s.recv(BUFFER_SIZE)
                if info=="true":
                    print("Deleting " + userinfo + "'s mail...")
                    time.sleep(1)
                    print(userinfo + "'s mail has been deleted")
                else:
                    print("There is no account with that username")
                time.sleep(1)

            elif option == "delete account":
                print("Whos account would you like to delete?")
                userinfo = raw_input("> ")
                s.send(userinfo)
                time.sleep(1)
                info=s.recv(BUFFER_SIZE)
                if info=="true":
                    print("Are you sure you want to delete " + userinfo + "'s account?")
                    print("Options: yes | no")
                    while True:
                        confirm=raw_input(" > ")
                        s.send(confirm)
                        time.sleep(1)
                        response=s.recv(BUFFER_SIZE)
                        print(response)
                        break
                else:
                    print("There is no account with that username")
                time.sleep(1)

        else:
            print(option + " is not an option")


TCP_IP = '0.0.0.0'
TCP_PORT = 6263
BUFFER_SIZE = 1024


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    print("Welcome to the system. Please register or login.")
    print("Options: register | login | exit")
    while True:
        option =raw_input("> ")
        if option == "login":
            login()
        elif option == "register":
            register_client()
        elif option == "exit":
            break
        else:
            print(option + " is not an option")

s.close()
print("received data")


