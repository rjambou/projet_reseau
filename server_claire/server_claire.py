#!/usr/bin/env python
# coding: utf-8
import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import subprocess as sub
import commands as cmd
import time
import os
import json
import sys
import getpass
from os.path import expanduser


DEFAULT_FILEPATH = 'comptes.json'
#all accounts
users = {
    "root": {
        "password": "gucci-mane",
        "group": "admin",
        "mail": []
    }
}

current_dir=os.getcwd()
os.chdir(current_dir)                       

def serialize_dico( dico_to_serialize, filepath): #met a jour un dictionnaire
    try:
        with open(filepath, 'w') as output_file:
            output_file.write( json.dumps( dico_to_serialize, indent = 2 ) )
    except IOError:
        print "serialize_dico > Impossible d'ouvrir le fichier"
    
def deserialize_dico( filepath ): #cree un dictionnaire
    try:
        with open(filepath, 'r') as input_file:
            return json.loads( input_file.read() )
    except IOError:
        print "deserialize_dico > Impossible d'ouvrir le fichier"

users=deserialize_dico('comptes.json')
permissions=deserialize_dico('permissions.json')

def ajout_permissions (chaine, title,username) : #donne les permissions ou non sur un fichier aux differentes classes
    os.chdir("../")
    if chaine[0]=="y":
        permissions["doctor"]["fichiers"].append(title)
    if chaine[1]=="y":
        permissions["nurse"]["fichiers"].append(title)
    if chaine[2]=="y":
        permissions["secretary"]["fichiers"].append(title)
    serialize_dico(permissions, 'permissions.json')
    classe=users[username]["group"]
    os.chdir(classe)

def check_droits(classe, nom_fichier): #verifie si la classe "classe" a acces au fichier "nom_fichier"
    if nom_fichier in permissions[classe]["fichiers"]:
        return "true"
    else:
        return "false"

def loginauth(username, password): #verifie si le mot de passe de "username" est bien "password"
    if username in users:
        if password == users[username]["password"]:
            print("Login successful")
            return True
    return False
    
def verify(username): #verifie si "username" existe dans users
    if users.has_key(username)==True:
        return "false"
    else:
        return "true"
    
def create(username, password,group): #cree un utilisateur "username" avec le mot de passe "password" appartenant au groupe "group"
    users[username] = {}
    users[username]["password"] = password
    users[username]["group"] = group
    users[username]["mail"] = []
    time.sleep(1)
    print("Account has been created")
    serialize_dico(users,'comptes.json')

#arefaire
def username_valid(recipient): #verifie si "username" existe dans users
    if users.has_key(recipient):
        return "true"
    else:
        print("There is no account with that username")
        return "false"

def shell(data):                           
    a=sub.check_output(data, shell=True)
    if (a==''):
        a='commande reussie'
    return a


def sendmail_server(username, recipient,subject,context): #envoie un mail de "username" à "recipient" avec le sujet "subject" et le texte "context"
    print("Sending mail...")
    users[recipient]["mail"].append(["Sender: " + username, "Subject: " + subject, "Context: " + context])
    os.chdir("../")
    serialize_dico(users, 'comptes.json')
    os.chdir(users[username]["group"])
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
            while True:
                username=conn.recv(1024)
                print username
                if verify(username):
                    username_exists="true"
                    conn.send(username_exists)
                    break
                else:
                    username_exists="false"
                    conn.send(username_exists)
            data=conn.recv(1024)
            print("data : "+data)
            #if not data: break
            commande = data.split(" ")
            print(commande)

#login

            if (commande[0]=="login"):
                username=commande[1]
                password=commande[2]
                if loginauth(username, password):
                    data="true"
                    print("login auth true")
                else:
                    data="false"
                    print("login auth false")

#register

            if (commande[0]=="register"):
                username=commande[1]
                password=commande[2]
                group=commande[3]
                if verify(username):
                    create(username, password, group)
                    data="created"
                else:
                    data="uncreated"

#session

            if commande[0] == "session":
                username=commande[1]
                print("u", username)
                if users[username]["group"] == "admin":
                    data="role: admin"
                    conn.send(data)
                else:
                    data="role: users as " + users[username]["group"]
                    conn.send(data)
                if users[username]["group"]=="doctor":
                    os.chdir("doctor")
                if users[username]["group"]=="nurse":
                    os.chdir("nurse")
                if users[username]["group"]=="secretary":
                    os.chdir("secretary")            
                while True:

    #logout

                    option=conn.recv(BUFFER_SIZE)
                    if option == "logout":
                        print(username + " logout")
                        break

    #view mail

                    if option == "view mail":
                        print(str(len(users[username]["mail"])))
                        conn.send(str(len(users[username]["mail"])))
                        time.sleep(1)
                        for mail in users[username]["mail"]:
                            mail=str(mail)
                            conn.send(mail)

    #send mail

                    if option == "send mail":
                        recipient=conn.recv(BUFFER_SIZE)
                        print("r", recipient)
                        validity=username_valid(recipient)
                        conn.send(validity)
                        time.sleep(1)
                        while validity=="false":
                            recipient=conn.recv(BUFFER_SIZE)
                            validity=username_valid(recipient)
                            conn.send(validity)
                            time.sleep(1)
                        subject = conn.recv(BUFFER_SIZE)
                        time.sleep(1)
                        context = conn.recv(BUFFER_SIZE)
                        sendmail_server(username,recipient,subject,context)

    #commande shell

                    if option == "commande shell":
                        commande_shell=conn.recv(BUFFER_SIZE) #string
                        tab_commande=commande_shell.split(' ')
                        print(tab_commande)
                        if tab_commande[0]=='cd':
                            if len (tab_commande) == 1:
                                home=expanduser("~")
                                os.chdir(home)
                                data=shell('pwd')
                                conn.send(data)
                            else:
                                new_path=tab_commande[1]
                                saved_path = os.getcwd()
                                try:
                                    os.chdir(new_path)
                                except OSError:
                                    print("Error : Command cancelled.")
                                    print("Error : Command cancelled.")
                                data=shell('pwd')
                                conn.send(data)
                        else:
                            data=shell(commande_shell)
                            conn.send(data)

    #gestion de fichier

                    if option == "rapport":
                        ls=sub.check_output("ls")
                        conn.send(str(ls))
                        title=conn.recv(BUFFER_SIZE)
                        time.sleep(1)
                        test="false"
                        for i in permissions:
                            for j in permissions[i].values():
                                if title in j:
                                    test="true"
                        if test=="true":
                            conn.send("true")
                            data=sub.check_call(["vim " + title], stdout=conn, stdin=conn, shell=True)
                            conn.send("endVim")
                            time.sleep(1)
                        else:
                            conn.send("false")
                            file_access=conn.recv(BUFFER_SIZE)
                            ajout_permissions(file_access,title,username)
                            print("loading...")
                            data=sub.check_call(["vim " + title], stdout=conn, stdin=conn, shell=True)
                            conn.send("endVim")
                            time.sleep(1)
                        if users[username]["group"]=="doctor":
                            if check_droits("nurse",title)=="true":
                                shell("cp "+title+" ../nurse/")
                            if check_droits("secretary",title)=="true":
                                shell("cp "+title+" ../secretary/")
                        if users[username]["group"]=="nurse":
                            if check_droits("doctor",title)=="true":
                                shell("cp "+title+" ../doctor/")
                            if check_droits("secretary",title)=="true":
                                shell("cp "+title+" ../secretary/")
                        if users[username]["group"]=="doctor":
                            if check_droits("nurse",title)=="true":
                                shell("cp "+title+" ../nurse/")
                            if check_droits("secretary",title)=="true":
								shell("cp "+title+" ../secretary/")

                    if users[username]["group"] == "admin":
                        if option == "user mail":
                            userinfo=conn.recv(BUFFER_SIZE)
                            if userinfo in users:
                                info="true"
                                conn.send(info)
                                time.sleep(1)
                                conn.send(str(len(users[userinfo]["mail"])))
                                time.sleep(1)
                                for mail in users[userinfo]["mail"]:
                                    mail=str(mail)
                                    conn.send(mail)
                            else:
                                info="false"
                                conn.send(info)

                        elif option == "delete mail":
                            userinfo=conn.recv(BUFFER_SIZE)
                            if userinfo in users:
                                info="true"
                                conn.send(info)
                                users[userinfo]["mail"] = []
                                serialize_dico(users,"comptes.json")
                                time.sleep(1)
                                print(userinfo + "'s mail has been deleted")
                            else:
                                info="false"
                                conn.send(info)
                        elif option == "delete account":
                            userinfo=conn.recv(BUFFER_SIZE)
                            if userinfo in users:
                                info="true"
                                conn.send(info)
                                while True:
                                    confirm=conn.recv(BUFFER_SIZE)
                                    if confirm == "yes":
                                        print("Deleting " + userinfo + "'s account...")
                                        del users[userinfo]
                                        os.chdir("../")
                                        serialize_dico(users,"comptes.json")
                                        os.chdir(users[username]["group"])
                                        time.sleep(1)
                                        conn.send(userinfo + "'s account has been deleted")
                                        break
                                    elif confirm == "no":
                                        print("Canceling account deletion...")
                                        time.sleep(1)
                                        conn.send("Account deletion canceled")
                                        break
                                    else:
                                        conn.send(confirm + " is not an option")
                                        break
                            else:
                                info="false"
                                conn.send(info)
            print("received data:", data)
            conn.sendall(data)

def shell(data):                            
    a=sub.check_output(data, shell=True)
    if (a==''):
        a='commande reussie'
    return a


TCP_IP = '0.0.0.0'
TCP_PORT = 6264
BUFFER_SIZE = 1024

##prevoir un systeme de fermeture de connexion si fermeture du client (on supprime le thread)
##prevoir un systeme de fermeture de connexion si erreur ernno 32 broken pipe


tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcpsock.bind((TCP_IP,TCP_PORT))
threads=[]

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn,(ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
