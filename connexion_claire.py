#!/usr/bin/env python
#-*-coding: utf8-*

import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import subprocess as sub
import commands as cmd
import time
import os
import json
import sys

DEFAULT_FILEPATH = 'comptes.json'
#all accounts
users = {
    "root": {
        "password": "gucci-mane",
        "group": "admin",
        "mail": []
    }
}

#save account in file
os.chdir("/promo2019/chamonet/Insa/projetreseau/projet_reseau") #a changer en fonction de l'installation                       

def serialize_dico( dico_to_serialize, filepath = DEFAULT_FILEPATH ):
    try:
        with open(filepath, 'w') as output_file:
            output_file.write( json.dumps( dico_to_serialize, indent = 2 ) )
    except IOError:
        print "serialize_dico > Impossible d'ouvrir le fichier"

def deserialize_dico( filepath = DEFAULT_FILEPATH ):
    try:
        with open(filepath, 'r') as input_file:
            return json.loads( input_file.read() )
    except IOError:
        print "deserialize_dico > Impossible d'ouvrir le fichier"

users=deserialize_dico()

def loginauth(username, password):
    if username in users:
        if password == users[username]["password"]:
            print("Login successful")
            return True
    return False
    
def verify(username):
    if users.has_key(username)==True:
        return False
    else:
        return True
    
def create(username, password):  
    users[username] = {}
    users[username]["password"] = password
    users[username]["group"] = "user"
    users[username]["mail"] = []    #a completer
    time.sleep(1)
    print("Account has been created")
    serialize_dico(users)

#arefaire
def username_valid(recipient):
    if users.has_key(recipient):
        return "true"
    else:
        print("There is no account with that username")
        return "false"

def sendmail_server(username, recipient,subject,context):
    print("Sending mail...")
    users[recipient]["mail"].append(["Sender: " + username, "Subject: " + subject, "Context: " + context])
    serialize_dico(users)
    time.sleep(1)
    print("Mail has been sent to " + recipient)


class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip=ip
        self.port=port
        print("[+] New thread started for "+ip+":"+str(port))


    def run(self):
        while True:
            data=conn.recv(1024)
            #if not data: break
            commande = data.split(" ")
            print(commande)
            if (commande[0]=="login"):
                username=commande[1]
                password=commande[2]
                if loginauth(username, password):
                    data="true"
                else:
                    data="false"
            if (commande[0]=="register"):
                username=commande[1]
                password=commande[2]
                if verify(username):
                    create(username, password)
                    data="created"
                else:
                    data="uncreated"
            if commande[0] == "session":
                username=commande[1]
                if users[username]["group"] == "admin":
                    data="role: admin"
                    conn.send(data)
                else:
                    data="role: user"
                    conn.send(data)
                while True:
                    option=conn.recv(BUFFER_SIZE)
                    if option == "logout":
                        print(username + " logout")
                        break
                    if option == "view mail":
                        conn.send(str(len(users[username]["mail"])))
                        time.sleep(1)
                        for mail in users[username]["mail"]:
                            mail=str(mail)
                            conn.send(mail)
                    if option == "send mail":
                        recipient=conn.recv(BUFFER_SIZE)
                        validity=username_valid(recipient)
                        conn.send(validity)
                        time.sleep(1)
                        subject = conn.recv(BUFFER_SIZE)
                        time.sleep(1)
                        context = conn.recv(BUFFER_SIZE)
                        sendmail_server(username,recipient,subject,context)
                    if (option == "commande shell"):
                        commande_shell=conn.recv(BUFFER_SIZE)
                        data=shell(commande_shell)
                        conn.send(data)


            print("received data:", data)
            conn.sendall(data)

def shell(data):                            #Attention commande cd
    a=sub.check_output(data, shell=True)
    if (a==''):
        a='commande reussie'
    return a