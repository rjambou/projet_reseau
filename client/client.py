#!/usr/bin/env python
# coding: utf-8
import subprocess as sub
import commands as cmd
import socket
import time
import os
import json
import sys
import getpass
import signal
from filemanagement import *


current_dir=os.getcwd()
os.chdir(current_dir) #le path change automatiquement                    

def droits(): #gere les droits d'un fichier
    access_string=""
    print("Can doctors access your files ? Yes(Y) or No(N) ?")
    while True :
        doctor_access=raw_input("> ")
        if doctor_access.lower() in ["y","n"]:
            access_string+=doctor_access.lower()
            break
        else:
            print("Invalid response. Please try again.")
            continue
    print("Can nurses access your files ? Yes(Y) or No(N) ?")
    while True :
        nurse_access=raw_input("> ")
        if doctor_access.lower() in ["y","n"]:
            access_string+=nurse_access.lower()
            break
        else:
            print("Invalid response. Please try again.")
            continue
    print("Can secretaries access your files ? Yes(Y) or No(N) ?")
    while True :
        secretary_access=raw_input("> ")
        if secretary_access.lower() in ["y","n"]:
            access_string+=secretary_access.lower()
            break
        else:
            print("Invalid response. Please try again.")
            continue
    return access_string #Exemple : "YYN"

def securite(password): #oblige a avoir un mdp safe
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
        s.send("session"+" "+str(username))
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




def session(username):
    current_dir=os.getcwd()
    os.chdir(current_dir) #le path change automatiquement                        
    shell("cd ../client")
    data="session " + username
    s.send(data)
    time.sleep(1)
    print("Welcome to your account " + username)
    message_session=s.recv(BUFFER_SIZE)
    print(message_session)
    while True:
        print("Options: view mail | send mail | commande shell | rapport | logout")
        option = raw_input(username + " > ")
        s.send(option)
        time.sleep(1)

#logout

        if option == "logout":
        	print("Logging out...")
        	break

#view mail

        elif option == "view mail":
            print("Current mail:")
            nombre_mail=s.recv(BUFFER_SIZE)
            print nombre_mail
            for i in range(int(nombre_mail)):
                mail=s.recv(BUFFER_SIZE)
                print(mail)

#send mail

        elif option == "send mail":
        	sendmail_client(username)

#commande shell

        elif option == "commande shell":
            commande=raw_input("Please enter your commande ! ")
            s.send(commande)
            time.sleep(1)
            resultats=s.recv(BUFFER_SIZE)
            print(resultats)

#gestion de fichier

        elif option == "rapport":
            while True:
                ls=s.recv(BUFFER_SIZE)
                print(ls)
                title=raw_input("fileName: ")
                s.send(title)
                time.sleep(1)
                test=s.recv(BUFFER_SIZE)
                if test=="false":
                    file_access=droits()
                    s.send(file_access)
                time.sleep(1)
                s.settimeout(None)
                connemission = Emission(s)
                connrecep = Reception(s, connemission)

                connemission.start()
                connrecep.start()

                connemission.join()
                connrecep.join()
                
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
TCP_PORT = 6264
BUFFER_SIZE = 1024


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    print("Welcome to the system. Please register or login.")
    while True:
        sferm="true"
        print("Options: register | login | exit")
        option =raw_input("> ")
        if option == "login":
            login()
        elif option == "register":
            register_client()
        elif option == "exit":
            s.close
            sferm="false"
            break
        else:
            print(option + " is not an option")
    if sferm=="false":
        break
s.close()
print("received data")


