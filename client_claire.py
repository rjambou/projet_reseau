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
import graphical_claire
import accueil
import interface_reseau

current_dir=os.getcwd()
os.chdir(current_dir) #le path change automatiquement                    

correct=True
blank=True
length=True
nb=True
lt=True
already_register=True
pwd=True
gr=True

def securite(password):
    if len(password)<8:
        length=False
        nb=True
        lt=True
        save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
        register_client(save[1], save[2], save[3], save [4])
        length=True
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
        nb=False
        length=True
        lt=True
        save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
        register_client(save[1], save[2], save[3], save [4])
        nb=True
        print("Your password has to contain a number.")
        return False
    if lettre==False:
        lt=False
        length=True
        nb=True
        save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
        register_client(save[1], save[2], save[3], save [4])
        print("Your password has to contain a letter.")
        lt=True
        return False
    return True

def login(username, password):
    print("Please enter your login")
    while True:
        #username = raw_input("Username: ")
        if not len(username) > 0:
            correct=False
            auth=graphical_claire.fenetreauth(correct)
            login(auth[1], auth[2])
            correct=True
            print("Username can't be blank")
        else:
            break
    while True:
        #password = getpass.getpass("Password : ")
        if not len(password) > 0:
            correct=False
            auth=graphical_claire.fenetreauth(correct)
            login(auth[1], auth[2])
            correct=True
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
        correct=False
        auth=graphical_claire.fenetreauth(correct)
        login(auth[1], auth[2])
        correct=True
        print("Invalid username or password! you redirect to home")

def register_client(username, password, password2, group):
    while True:
        #username = raw_input("New username: ")
        if not len(username) > 0:
            blank=False
            save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
            register_client(save[1], save[2], save[3], save [4])
            blank=True
            print("Username can't be blank")
            continue
        else:
            break
    while True:
        #password = getpass.getpass("Password : ")
        #password2 = getpass.getpass("Re-enter password : ")
        if password!=password2 :
            pwd=False
            print("Passwords don't match.\nPlease try again.\n")
            save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
            register_client(save[1], save[2], save[3], save [4])
            pwd=True
            continue
        if not securite(password):
            print("Please try again.\n")
            continue
        else:
            break
    while True:
        #group = raw_input("choice your group (doctor, nurse, secretary) : ")
        if not len(group) > 0:
            print("group can't be blank")
            gr=False
            save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
            register_client(save[1], save[2], save[3], save [4])
            gr=True
            continue
        else:
            break
    print("Creating account...")
    data="register " + username + " " + password + " " + group
    s.send(data)
    time.sleep(1)
    data=s.recv(BUFFER_SIZE)
    if data=="uncreated":
        already_register=False
        print("Username already use! Please recover your password or contact your administration")
        save=graphical_claire.fenetresave(blank, length, nb, lt, already_register, pwd, gr)
        register_client(save[1], save[2], save[3], save [4])
        already_register=True
        login()
    elif data == "created":
        print("User " + username + " created")
        login(username, password)

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


def shell(data):                            #Attention commande cd
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
        inter=interface_reseau.interface(current_dir, username)
        print("inter", inter)
        if message_session.split(" ")[1] == "admin":
            print("options user mail | delete mail | delete account")
        #option = raw_input(username + " > ")
        s.send(option)
        time.sleep(1)
        if inter[0]==False:
            print("Logging out...")
            break
        elif option == "view mail":
            print("Current mail:")
            nombre_mail=s.recv(BUFFER_SIZE)
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
                    terminer=raw_input("Avez vous terminez ?(oui ou non)")
                    while terminer!="oui":
                        time.sleep(1)
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
TCP_PORT = 6265
BUFFER_SIZE = 1024


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    option=accueil.accueil()
    print("Welcome to the system. Please register or login.")
    print("Options: register | login | exit")
    print option
    while True:
        if option == "login":
            auth=graphical_claire.fenetreauth(True)
            login(auth[1], auth[2])
        elif option == "register":
            save=graphical_claire.fenetresave(True, True, True, True, True, True, True)
            register_client(save[1], save[2], save[3], save [4])
        elif option == "exit":
            break
        else:
            print(option + " is not an option")


s.close()
print("received data")