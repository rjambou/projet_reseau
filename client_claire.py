#!/usr/bin/env python
#-*-coding: utf8-*
 
import socket
import time
import os
import json
import sys
import getpass
import graphical_claire

correct=True
blank=True
length=True
nb=True
lt=True

def securite(password):
    if len(password)<8:
        length=False
        nb=True
        lt=True
        auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
        register_client(auth[1], auth[2])
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
        auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
        register_client(auth[1], auth[2])
        nb=True
        print("Your password has to contain a number.")
        return False
    if lettre==False:
        lt=False
        length=True
        nb=True
        auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
        register_client(auth[1], auth[2])
        print("Your password has to contain a letter.")
        lt=True
        return False
    return True



def login(username, password):
    print("Please enter your login")
    while True:
        #username = raw_input("Username: ")
        if not len(username) > 0:
            blank=False
            correct=True
            length=True
            nb=True
            lt=True
            auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
            login(auth[1], auth[2])
            blank=True
            print("Username can't be blank")
        else:
            break
    while True:
        #password = getpass.getpass("Password : ")
        if not len(password) > 0:
            blank=False
            correct=True
            length=True
            nb=True
            lt=True
            auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
            login(auth[1], auth[2])
            blank=True
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
        blank=True
        length=True
        nb=True
        lt=True
        auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
        login(auth[1], auth[2])
        correct=True
        print("Invalid username or password! you redirect to home")

def register_client(username, password):
    while True:
        #username = raw_input("New username: ")
        if not len(username) > 0:
            blank=False
            auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
            register_client(auth[1], auth[2])
            blank=True
            print("Username can't be blank")
            continue
        else:
            break
    while True:
        #password = getpass.getpass("Password : ")
        #password2 = getpass.getpass("Re-enter password : ")
        #if password!=password2 :
        #    print("Passwords don't match.\nPlease try again.\n")
        #    continue
        if not securite(password):
            print("Please try again.\n")
            continue
        else:
            break
    print("Creating account...")
    data="register " + username + " " + password
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




def session(username):
    data="session " + username
    s.send(data)
    time.sleep(1)
    print("Welcome to your account " + username)
    print("Options: view mail | send mail | commande shell | logout")
    message_session=s.recv(BUFFER_SIZE)
    print(message_session)
    while True:
        option = raw_input(username + " > ")
        if option == "logout":
        	s.send(option)
        	time.sleep(1)
        	print("Logging out...")
        	break
        elif option == "view mail":
            print("Current mail:")
            s.send(option)
            time.sleep(1)
            nombre_mail=s.recv(BUFFER_SIZE)
            for i in range(int(nombre_mail)):
                mail=s.recv(BUFFER_SIZE)
                print(mail)
        elif option == "send mail":
        	s.send(option)
        	time.sleep(1)
        	sendmail_client(username)
        elif option == "commande shell":
        	s.send(option)
        	time.sleep(1)
        	commande=raw_input("Please enter your commande ! ")
        	s.send(commande)
        	time.sleep(1)
        	resultats=s.recv(BUFFER_SIZE)
        	print(resultats)
        # elif users[username]["group"] == "admin":
        #     if option == "user mail":
        #         print("Whos mail would you like to see?")
        #         userinfo = raw_input("> ")
        #         if userinfo in users:
        #             for mail in users[userinfo]["mail"]:
        #                 print(mail)
        #         else:
        #             print("There is no account with that username")
        #     elif option == "delete mail":
        #         print("Whos mail would you like to delete?")
        #         userinfo = raw_input("> ")
        #         if userinfo in users:
        #             print("Deleting " + userinfo + "'s mail...")
        #             users[userinfo]["mail"] = []
        #             time.sleep(1)
        #             print(userinfo + "'s mail has been deleted")
        #         else:
        #             print("There is no account with that username")
        #     elif option == "delete account":
        #         print("Whos account would you like to delete?")
        #         userinfo = raw_input("> ")
        #         if userinfo in users:
        #             print("Are you sure you want to delete " + userinfo + "'s account?")
        #             print("Options: yes | no")
        #             while True:
        #                 confirm = raw_input("> ")
        #                 if confirm == "yes":
        #                     print("Deleting " + userinfo + "'s account...")
        #                     del users[userinfo]
        #                     time.sleep(1)
        #                     print(userinfo + "'s account has been deleted")
        #                     break
        #                 elif confirm == "no":
        #                     print("Canceling account deletion...")
        #                     time.sleep(1)
        #                     print("Account deletion canceled")
        #                     break
        #                 else:
        #                     print(confirm + " is not an option")
        #         else:
        #             print("There is no account with that username")
        else:
            print(option + " is not an option")


TCP_IP = '0.0.0.0'
TCP_PORT = 6264
BUFFER_SIZE = 1024


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    auth=graphical_claire.fenetreauth(correct, blank, length, nb, lt)
    option=auth[0]
    print("Welcome to the system. Please register or login.")
    print("Options: register | login | exit")
    while True:
    # option =raw_input("> ")
        if option == "login":
            login(auth[1], auth[2])
        elif option == "register":
            register_client(auth[1], auth[2])
        elif option == "exit":
            break
        else:
            print(option + " is not an option")

s.close()
print("received data")