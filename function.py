#LAGHISSI Hiba, MARIAULT Lee et AMMAR Fatma


# ce tag va permettre de prévenir l'utilisateur que tous les modules n'ont pas pu être importés.
tag_module=False
try:
    import itertools
    from collections import deque

    import urllib.request
    import requests
    import os, sys
    import tkinter
    from matplotlib import pyplot as plt
    from matplotlib.backends._backend_tk import NavigationToolbar2Tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import csv
    import numpy as np
    from Bio import SeqIO
    import argparse
    import numpy as np
    
    
#Cette gestion d'exception permettra l'utilisateur d'utiliser quand même le programme même si tous les modules n'ont pas été importés
except ImportError:
    tag_module=True
    print('Certains modules nécéssaires au bon fonctionnement du programme n\'ont pas pu être importés')
    pass

#Faire en sorte que le script s'adapte à python3 et python2
try:
    from tkinter import *
    # importation necessaire pour afficher des pop up
    from tkinter.messagebox import showwarning, showinfo, askyesno
    import tkinter.filedialog
    # importation necessaire pour gerer des menus + importer et enregistrer des fichiers
    from tkinter.filedialog import Menu, askopenfilename, askopenfile
except ImportError:
    import Tkinter as tkinter 
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    




URL = "https://www.uniprot.org/uniprot/"
#Variable globale qui sera utilisée par la fonction acces_fichier_UNIPROT
data1 = ""
#Variable globale qui sera utilisée par la fonction acces_fichier_FASTA
data2 = ""
#Variables globale qui sera utilisée par la fonction tk_taille
compteur=0
i = 1

#variables globales utilisées par toutes les fonctions
global sequence
sequence=""
global titre
titre=""


# Les tags suivants vont obliger la fonction à s'éxecuter qu'une seule fois, même si l'utilisateur clique plusieurs fois sur 'GO'.
# Ceci a été fait parce qu'on remarquait que les résultats s'accumulaient entre eux au fur et à mesure qu'on cliquait sur 'GO'
tag_1time_execution_taille=False
tag_1time_execution_PM=False
tag_1time_execution_occ=False
#variable booléenne globale qui sera utilisée par la fonction newfile et readFasta. Si elle est true ça voudrait dire que l'utilisateur
# a importé un fichier et qu'il faut donc le traiter localement.


# Ce tag empêchera les fonctions d'éxecuter readFasta  plusieurs fois pour récupérer la séquence si cette dernière ne change pas.
tag_read = False 

########################### Ouverture de la fenêtre principale tkinter ###########################
fenetre = Tk()
fenetre.title("BIENVENUE SUR TKINTER!")
fenetre.geometry("1500x800")
fenetre.configure(background="chocolate")
fenetre.resizable(True, True)

#Ce tag va être True si certains modules n'ont pas été importé et préviendra l'utilisateur.
if tag_module == True:
    showwarning("Message d'erreur","Attention, certains modules nécéssaires au bon fonctionnement du programme n'ont pas pu être importés")
global NA
NA = StringVar(fenetre, value="")
global message_inpute
message_inpute = Label(fenetre, text="Veuillez entrer un numéro d'accession svp", background="peach puff").place(y=20, x=495)
global inpute
inpute = Entry(fenetre, textvariable=NA, width=30, background="peach puff").place(y=50, x=545)
message_resultats = Label(fenetre, text="Résultats de la recherche :", background="peach puff").place(y=480, x=10)

#Le programme va essayer d'importer le logo de l'université mais s'il ne le trouve pas, il ne va pas planter
try:
    photo = PhotoImage(file="UCA.png")
    canvas = Canvas(fenetre,width=400, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.place(x=10,y=10)
except TclError:
    pass


################################ Accéder au fichier UNIPROT ###########################

global window1


def acces_fichier_UNIPROT():
    '''  Cette fonction va être appelée par le bouton GO : si l'utilisateur oche la case de récupération du fichier Uniprot. Il
    utilise internet et le site UNIPROT pour trouver les fiches de la protéine '''
    try:
        
        r = requests.get(URL + NA.get() + ".txt")
        global data1
        data1 = r.text
        #Si le site renvoie une erreur dont le code est entre 400 et 500 non inclus, c'est que la page n'a pas
        # été trouvée sur le site, c'est donc une erreur par rapport au numéro d'accession
        if 400 <= r.status_code < 500:
            showwarning("Message d'erreur", "Nous n'avons pas pu accéder à la fiche Uniprot, vérifiez le numéro d'accession")

        #Si le site renvoie une erreur dont le code est entre 500 et 600 non inclus, c'est que le serveur ne répond pas
        if 500 <= r.status_code < 600:
            showwarning("Message d'erreur", "Nous n'avons pas pu accéder à la fiche Uniprot,le serveur ne répond pas")

    #Le programme peut rencontrer des soucis de connexion en allant sur le site, dans ce cas il va prévenir l'utilisateur
    except OSError:
        showwarning("Message d'erreur","vérfiez votre connexion internet")
    else:
        global window1
        window1 = Tk()
        window1.title("Traitement du fichier")
        window1.geometry("500x100")
        lebal = Label(window1, text="félicitation, j'ai eu accès à la fiche UNIPROT demandé, voulez-vous l'enregistrer?")
        lebal.place(y=10, x=10)
        b1_1 = Button(window1, text="YES", width=15, command=save_file_UNIPROT)
        b1_2 = Button(window1, text="NO", width=15, command=window1.destroy)
        b1_1.place(y=30, x=150)
        b1_2.place(y=60, x=150)



def save_file_UNIPROT():
    '''  Cette fonction va être appelée par le bouton b1_1 pour qu'elle enregistre le fichier '''
    try:
        global window1
        # Une fois le choix d'enregistrer le fichier a été fait, window1 disparaît
        window1.destroy()
        # On a choisit d'utiliser tkinter.filedialog.asksaveasfile pour que l'utilisateur puisse choisir le nom et l'emplacement du fichier crée
        file_uni =  tkinter.filedialog.asksaveasfile(mode ='w', initialdir = "/",title = "Enregistrer le fichier UNIPROT",filetypes = (("text","*.txt"),("all files","*.*")))
        file_uni.write(data1)
        file_uni.close()

        showinfo("Mission effectuée","Votre fichier a bien été enregistré.")

    ######################################### GESTION D'ERREUR ################################################
    # Une erreur de type AttributeError s'affiche si l'utilisateur change d'avis et n'enregistre pas le fichier
    except AttributeError:
        pass
    # Une erreur de type PermissionError s'affiche si l'utilisateur tente d'enregistrer le fichier dans un répertoire mais qu'il n'a pas le droit de le faire
    except PermissionError:
        showwarning("Message d'erreur", "Veuillez choisir un autre répertoire pour enregistrer votre fichier")


################################ Accéder au fichier fasta ############################

global window2

def acces_fichier_FASTA():
    '''  Cette fonction va être appelée par le bouton b1 : si l'utilisateur veut récupérer le fichier FASTA  '''
    try:
        global offline_status

        #Si le fichier n'a pas été importé, offline_status sera toujours False
        if offline_status == False:
            d = requests.get(URL + NA.get() + ".fasta")
            #Si aucun problème n'est rencontré pendant l'accès à la page internet, le site renvoit un code HTTP entre 200 et 300 non inclus
            
            global data2
            data2 = d.text

            #Si le site renvoie une erreur dont le code est entre 400 et 500 non inclus, c'est que la page n'a pas
            # été trouvée sur le site, c'est donc une erreur par rapport au numéro d'accession
            if 400 <= d.status_code < 500:
                showwarning("Message d'erreur", "Nous n'avons pas pu accéder à la fiche Fasta, vérifiez le numéro d'accession")

            #Si le site renvoie une erreur dont le code est entre 500 et 600 non inclus, c'est que le serveur ne répond pas
            elif 500 <= d.status_code < 600:
                showwarning("Message d'erreur", "Nous n'avons pas pu accéder à la fiche Fasta,le serveur ne répond pas")

        #Si le fichier a été importé, l'utilisateur a déjà le fichier FASTA, donc ça ne sert à rien d'aller chercher sur internet
        elif offline_status == True:
            showwarning("Petit malin ;)", "on ne me l'a fait pas à moi, vous avez déjà le fichier sous format fasta")
    except OSError:
        showwarning("Message d'erreur","vérfiez votre connexion internet")

    else:
        global window2
        window2 = Tk()
        window2.title("Traitement du fichier")
        window2.geometry("500x100")
        lebal = Label(window2, text="félicitation, j'ai eu accès au fichier FASTA demandé, voulez-vous l'enregistrer?")
        lebal.grid()
        b2_1 = Button(window2, text="YES", width=15, command=save_file_fasta)
        b2_2 = Button(window2, text="NO", width=15, command=window2.destroy)
        b2_1.place(y=30, x=150)
        b2_2.place(y=60, x=150)



def save_file_fasta():
    ''' Cette fonction va être appelée par le bouton  pour enregistrer le fichier'''
    try:
        global window2
        window2.destroy()
        # On a choisit d'utiliser tkinter.filedialog.asksaveasfile pour que l'utilisateur puisse choisir le nom et l'emplacement du fichier crée
        file_fas =  tkinter.filedialog.asksaveasfile(mode ='w', initialdir = "/",title = "Enregistrer le fichier FASTA",filetypes = (("*.fasta","*.fas"),("text",".txt")))
        file_fas.write(data2)
        file_fas.close()

        showinfo("Mission effectuée","Votre fichier a bien été enregistré.")
    ######################################### GESTION D'ERREUR ################################################
    # Une erreur de type AttributeError s'affiche si l'utilisateur change d'avis et n'enregistre pas le fichier
    except AttributeError:
        pass
    # Une erreur de type PermissionError s'affiche si l'utilisateur tente d'enregistrer le fichier dans un répertoire mais qu'il n'a pas le droit de le faire
    except PermissionError:
        showwarning("Message d'erreur", "Veuillez choisir un autre répertoire pour enregistrer votre fichier")




############################@# Récupérer la séquence et le header ################################
global file
file = NA.get() + ".fas"
def file_change():
    ''' Cette fonction va changer la variable  globale file utilisé par la fonction readFasta, elle change selon le type de recherche offline/online '''
    global file
    # Si l'utilisateur n'importe pas de fichier
    if offline_status == False:
        # file prendra comme valeur, le numéro d'accesion écrit dans le champs de saisie
        file = NA.get() + ".fas"
    # Si l'utilisateur importe un fichier
    elif offline_status == True:
 
        # file sera le fichier multifasta
        file = name





def readFasta(file):
    """Cette fonction va vous renvoyer la séquence complète et le header de votre fichier fasta. Elle récupère la séquence protéique d'internet et les informations 
    qui vont avec, quand l'utilisateur rentre directement le code d'accesion. Par contre, s'il importe un fichier multifasta, elle va chercher les informations 
    directement du fichier importé. À part pour la fiche UNIPROT qui, dans tous les cas, nécéssite d'aller sur internet"""
    seq=""
    header=""
    global tag_read   
    global offline_status

    # Si l'utilisateur n'importe pas de fichier mais rentre directement un code d'accession alors le programme cherchera les informations sur le site UNIPROTKB
    if offline_status == False:
        try:
            tag_read=True
            d = requests.get(URL + NA.get() + ".fasta")
            if 200 <= d.status_code < 300:
                data2 = d.text
                fh = open(NA.get() + ".fas", "w")
                fh.write(data2)
                fh.close()
            elif 400 <= d.status_code < 500:
                showwarning("Message d'erreur", "Nous n'avons pas pu accéder à la fiche Fasta, vérifiez le numéro d'accession")

            elif 500 <= d.status_code < 600:
                showwarning("Message d'erreur", "Nous n'avons pas pu accéder à la fiche Fasta,le serveur ne répond pas")

        except OSError:
            showwarning("Message d'erreur","vérfiez votre connexion internet")

        else:
            if os.path.isfile(file):
                ## ouverture d'un pointeur sur fichier en mode lecture
                fh = open(file, "r")
                ## lecture de la premiere ligne du fichier.
                line = fh.readline()
                ##initialise les chaines caracteres header et seq à chaine vide

                ## initialise un tag à False pour vérifier la présence du header
                tag_header_found = False
                ## tant que la ligne n'est pas vide
                while line:
                      ## nettoyage des retours chariot de fin de ligne
                    line = line.strip()
                    ## si le header est trouvé avant dans la boucle, il s'agit d'une ligne de séquence
                    if tag_header_found == True:
                        ## Ajoute des informations de la ligne à la sequence
                        seq = seq + line
                    ## Si la ligne commence par un ">"
                    elif line[0] == ">":
                        ## on stocke les informations du header
                        header = line
                        ## on change la valeur du tag header
                        tag_header_found = True
                    ## changement de la valeur d'une variable pour continuer la boucle
                    line = fh.readline()

                ## fermeture du fichier
                fh.close()
                ## retourne un tuple avec le header et la sequence
                # return (header, seq)
            else:
                # print("Erreur : le chemin donne '{}' n'est pas valide.".format(seqFile))
                ## etant donne qu'on ne peut lire le fichier, on arrete le programme via la methode exit().
                print("Fichier introuvable")

            

    # si l'utilisateur importe le fichier
    if offline_status == True:
        global i
        global sequence  
        # Ouverture du fichier multifasta ".fas"
        try:
            tag_read=True
            fh = open(name, "r")
        except IOError:
            showwarning("Message d'erreur", "Je n'arrive pas à ouvrir le fichier, verfiez qu'il existe vraiment dans votre répertoire courant et qu'il a une extension .fas")
        else:
            lines = fh.readlines()

            tag_header_found = False

            for line in lines[rec.position[NA.get()]:]:
                ## nettoyage des retours chariot et les backslash de fin de ligne
                line = line.replace('\\', '')
                line = line.strip()
                ## Si la ligne commence par un ">"
                if line[0] == ">":
                    i += 1
                    ## on stocke les informations du header
                    header = line
                    ## on change la valeur du tag header
                    tag_header_found = True
                ## si le header est trouvé avant dans la boucle, il s'agit d'une ligne de séquence
                elif tag_header_found == True:
                    ##Si ">" n'a pas encore été trouvé 2 fois
                    if i <= 2:
                        ## Ajoute des informations de la ligne à la sequence
                        
                        seq = seq + line
                    else:
                        tag_header_found = False

                


    return (header, seq)



############################# Création d'une classe pour la gestion d'erreur ########################
class gestion_erreur():
    """ Cette classe sera utilisée par plusieurs fonctions pour alerter l'utilisateur au cas où le programme trouve des incohérences  """


    def __init__(self):
        self.AA_notpossible=['B','j','O', 'U','X','Z']
        self.longueur_sequence=0
    
    def longueur_seq(self):
        """  Cette fonction va alerter l'utilisateur si la longueur de la séquence est de 0  """
        global sequence
        self.longueur_sequence=len(sequence)
        if self.longueur_sequence==0:
            showwarning("ATTENTION", "Nous avons trouvé une taille de 0, ce n'est pas normale, vérifiez votre fichier fasta ou le numéro d'accession")
        else:
            pass
    
    def composition(self):
        """ Cette fonction va alerter l'utilisateur si elle trouve des caractères qui ne correspondent pas à des AA, par contre les caractères seront compté, quand même, pour la taille
        car des caratères peuvent être ajoutés de façon délibérées comme le 'X'  """
        for AA in sequence:
            if AA in self.AA_notpossible:
                showwarning("ATTENTION", "Il y a des caractères qui ne correspondent pas à des acides aminées.")
                break
            else:
                pass
        
GER=gestion_erreur()

######################## Taille de la protéine ######################

def tk_taille():
    """ Cette fonction est appelée par la fonction bouton_taille(), elle calcule la taille de la séquence et affiche le résultat sur la fenêtre     """
    global titre, sequence 
    if tag_read==False:
        titre,sequence = readFasta(file)
    elif tag_read == True:
        pass

    for character in sequence:
        global compteur
        compteur+=1
    global tag_1time_execution_taille
    tag_1time_execution_taille=True
    global label1
    label1=Label(bg="peach puff", text=">>> la taille de la protéine est : {}".format(compteur))
    label1.place(y=520, x=30)

def bouton_taille():
    """  Cette fonction est appelée quand la case 'récupérer la taille de la séquence' est sélectionnée """

    while tag_1time_execution_taille==False:
        tk_taille()
    ################## Gestion d'erreur ###########################
    GER.longueur_seq()
    ###############################################################

###################### POIDS MOLÉCULAIRE ############################

def PM_peptide():
    """ Cette fonction va renvoyer le poids moléculaire de la protéine ou du peptide quand l'utilisateur clique sur le bouton correspondant """
    global titre, sequence 
    if tag_read==False:
        titre,sequence = readFasta(file)
    elif tag_read == True:
        pass

    DICO_PM = {'A': 71.04, 'C': 103.01, 'D': 115.03, 'E': 129.04,
               'F': 147.07, 'G': 57.02, 'H': 137.06, 'I': 113.08,
               'K': 128.09, 'L': 113.08, 'M': 131.04, 'N': 114.04, 'P': 97.05,
               'Q': 128.06, 'R': 156.10, 'S': 87.03, 'T': 101.05, 'V': 99.07,
               'W': 186.08, 'Y': 163.06}
    
    ##################### Gestion d'erreur #########################
    GER.composition()
    GER.longueur_seq()
    ################################################################

    global PM
    PM = 0
    for character in sequence:
        if character != "\n":
            if character in DICO_PM.keys():
                PM = PM + DICO_PM[character]
    global tag_1time_execution_PM
    tag_1time_execution_PM=True



def bouton_PM():
    """ Cette fonction va renvoyer le poids moléculaire de la protéine ou du peptide quand l'utilisateur clique sur le bouton correspondant dans la fenêtre de tkinter """
    while tag_1time_execution_PM==False:
        PM_peptide()
    global label2
    label2=Label(text=">>> le poids moléculaire de votre protéine est : {}".format(PM), background="peach puff")
    label2.place(y=560, x=30)


################################## OCCURENCE #####################################
# initialisation du dictionnaire vide pour stocker l'occurence de chaque AA
dico = {}


# definition de la fonction qui va calculer les occurences de chaque acide amine de notre sequence
def occurence_aa():
    """Cette fonction va renvoyer les occurences des acides aminées, autrement dit, combien on a de chacun"""
    global titre, sequence 
    if tag_read==False:
        titre,sequence = readFasta(file)
    elif tag_read == True:
        pass

    ##################### Gestion d'erreur #########################
    GER.composition()
    GER.longueur_seq()
    ################################################################

    global tag_1time_execution_occ
    tag_1time_execution_occ=True
    global dico
    
    # pour chaque caractère dans la sequence on va faire la boucle
    for aa in sequence:
        # on verifie si le caractère se trouve deja dans le dictionnaire
        if aa in dico:
            dico[aa] += 1
        # si le caractere ne se trouve pas dans le dictionnaire alors il va créer une nouvelle clé
        else:
            dico[aa] = 1

    return dico


def bouton_occurence():
    """ Cette fonction est exécutée quand la case d'occurence a été cochée, elle propose d'enregistrer les résultats et d'afficher un graphique  """
    while tag_1time_execution_occ==False:  
        occurence_aa()
    global label3
    label3=Label(bg="peach puff",text=">>> votre protéine est composée de : {}".format(dico))
    label3.place(y=600, x=30)
    global label4
    label4=Label(bg="peach puff", text=">>> >>> cliquez sur [SAVE] pour l'enregistrer et [GRAPHIQUE] pour avoir le graphique :")
    label4.place(y=620, x=50)
    b_o = Button(fenetre, text="SAVE", width=15, command=save_occ,bg="peach puff")
    b_G = Button(fenetre, text="GRAPHIQUE", width=15, command=graph,bg="peach puff")
    b_o.place(y=625, x=720)
    b_G.place(y=625, x=820)


def save_occ():
    """ Cette fonction est appelée quand l'utilisateur clique sur le bouton SAVE de la fonction bouton_occurence pour enregistrer le résultat """
    global dico
    try:
        file_occ =  tkinter.filedialog.asksaveasfile(mode ='w', initialdir = "/",title = "Enregistrer les résultats de l'occurence",filetypes = (("*.txt","*.txt"),("all files","*.*")))
        text2save=str(dico)
        file_occ.write(titre + '\n' +  text2save)
        file_occ.close()

    ######################################### GESTION D'ERREUR ################################################
    # Une erreur de type AttributeError s'affiche si l'utilisateur change d'avis et n'enregistre pas le fichier
    except AttributeError:
        pass
    # Une erreur de type PermissionError s'affiche si l'utilisateur tente d'enregistrer le fichier dans un répertoire mais qu'il n'a pas le droit de le faire
    except PermissionError:
        showwarning("Message d'erreur", "Veuillez choisir un autre répertoire pour enregistrer votre fichier")



######## GRAPHIQUE OCCURENCE ###############################################################
def graph_occ(dico):
    """ Cette fonction est appelée quand l'utilisateur clique sur le bouton graphique de la fonction bouton_occurence pour afficher le graphique """
    # Graphique occurence
    x = list(dico.keys())
    y = list(dico.values())
    f = plt.Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.axis(xmin=0, xmax=len(x))
    a.set_title("Occurence des acides aminés dans la séquence")
    a.bar(x, y)
    a.set_xlabel("Type d'acide aminé")
    a.set_ylabel("Nombre d'occurence")
    root = tkinter.Tk()
    root.wm_title("Profil d'occurence de la séquence")
    root.geometry("700x700")
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(y=100, x=100)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().place(y=100, x=100)


def graph():
    """ Cette fonction est appelée quand l'utilisateur choisit d'afficher le graphique """
    showinfo("Astuce", "Vous pouvez enregistrer le graphique en cliquant sur l'icône de la petite disquette.")
    graph_occ(dico)


################################### Hydrophobicité ###############################

# dicionnaire qui contient les valeurs d'hydrophobicite correspondantes a chaque acide amine
KD_scale = {'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8, 'G': -0.4, 'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8,
            'M': 1.9, 'N': -3.5, 'P': -1.6, 'Q': -3.5, 'R': -4.5, 'S': -0.8, 'T': -0.7, 'V': 4.2, 'W': -0.9, 'Y': -1.3}


def hydro_save():
    """ Cette fonction va créer un fichier où l'hydrophobicité moyenne est stockée au fur à mesure """
    calculateur = hydrophobicite(n=9)
    num = 5
   
    file_hydro =  tkinter.filedialog.asksaveasfile(mode ='a', initialdir = "/",title = "Enregistrer le profil d'hydrophobicité",filetypes = (("*.txt","*.txt"),("all files","*.*")))
    file_hydro.write(titre+'\n')
    for i in calculateur:
        # print("AA numero {} -> Hydrophobicite moyenne : {} ".format(num,i))
        file_hydro.write("AA numero {} -> Hydrophobicite moyenne : {}\n".format(num, i))
        num += 1
    file_hydro.close()




def graph_hydro():
    """  Cette fonction va créer le graphique d'hydrophobicité de la séquence   """
    showinfo("Astuce", "Vous pouvez enregistrer le graphique en cliquant sur l'icône de la petite disquette.")
    hydrophobicite(n=9)
    values = []
    total_residus = len(sequence)
    # Récupération des valeurs d'hydrophobicité de chaque acide aminé de la séquence à partir du dictionnaire
    # et stockage sous forme de liste
    for aa in list(sequence):
        values.append(KD_scale[aa])
    x_plot = range(1, total_residus + 1)
    f = plt.Figure(figsize=(5, 5), dpi=100)
    a = f.add_subplot(111)
    a.axis(xmin=5, xmax=total_residus - 5)
    a.set_title("Profil d'hydrophobicité de la séquence")
    a.set_xlabel("Position des acides aminés")
    a.set_ylabel('Hydrophobicité moyenne')
    a.plot(x_plot, values)
    root = Tk()
    root.wm_title("Profil d'hydrophobicité de la séquence")
    root.geometry("1500x700")
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    root.mainloop()

def bouton_hydrophobicite():
    """  Cette fonction va être appelée par GO si l'utilisateur coche l'hydrophobicité""" 

    hydrophobicite(n=9)
    try:
        hydro_save()
    # Une erreur de type AttributeError s'affiche si l'utilisateur change d'avis et n'enregistre pas le fichier, sauf que le graphique
    # a besoin du fichier enregistré pour qu'il affiche le résultat, donc un message d'erreur s'affiche.
    except AttributeError:
        showwarning("Message d'erreur", "Il faut enregistrer le fichier si vous voulez avoir le résultat et le graphique")
    # Une erreur de type PermissionError s'affiche si l'utilisateur tente d'enregistrer le fichier dans un répertoire mais qu'il n'a pas le droit de le faire
    except PermissionError:
        showwarning("Message d'erreur", "Veuillez choisir un autre répertoire pour enregistrer votre fichier")

    else:
        global label5
        label5=Label(fenetre,bg="peach puff", text=">>> l'hydrophobicité moyenne a été calculée et enregistrée.")
        label5.place(y=660,x=30)
        global label6
        label6=Label(fenetre,bg="peach puff",text=">>> >>> cliquez sur [Graphique] pour avoir le graphique :")
        label6.place(y=680, x=50)
        b_Graph = Button(fenetre,bg="peach puff", text="Graphique", width=15, command=graph_hydro).place(y=680, x=650)



def hydrophobicite(n=9):
    '''  Cette fonction va calculer l'hydrophobicité moyenne de la sequence sur une fenetre glissante de 9AA '''
    global titre, sequence

    ##################### Gestion d'erreur #########################
    GER.composition()
    ################################################################

    if tag_read==False:
        titre,sequence = readFasta(file)
    elif tag_read == True:
        pass

    global KD_scale
    num = 5
    list_sequence = []
    for aa in list(sequence):
        for k, v in KD_scale.items():
            if k == aa:
                list_sequence.append(v)

    ## La fonction iter va lire seq 1 à 1
    it = iter(list_sequence)
    d = deque(itertools.islice(it, n - 1))
    d.appendleft(0)
    s = sum(d)
    for aa in it:
        s += aa - d.popleft()
        d.append(aa)
        yield s / n




#####################################@####### Les classes ######################################################
global grouped
grouped=False

def acces_class():
    global grouped
    if not grouped:
        try:
            u = urllib.request.urlopen(url=URL + NA.get() + ".txt")
            data_uniprot = u.readlines()
            data_uniprot_clean = []
            for line in data_uniprot:
                data_uniprot_clean.append(line.decode("utf8"))
            group(data_uniprot_clean)
            grouped=True
        except OSError:
            showwarning("Message d'erreur","Vérifiez votre connexion internet.")

liste = ('RN', 'RP', 'RC', 'RX', 'RG', 'RA', 'RT', 'RL')
info = [" ALLERGEN", " ALTERNATIVE PRODUCTS", " BIOPHYSICOCHEMICAL PROPERTIES", " BIOTECHNOLOGY", " CATALYTIC ACTIVITY",
        " CAUTION", " COFACTOR", " DEVELOPMENTAL STAGE",
        " DISEASE", " DISRUPTION PHENOTYPE", " DOMAIN", " ACTIVITY REGULATION", "FUNCTION:", " INDUCTION",
        " INTERACTION", " MASS SPECTROMETRY", " MISCELLANEOUS",
        " PATHWAY", " PHARMACEUTICAL", " POLYMORPHISM", " PTM", " RNA EDITING", " SEQUENCE CAUTION", " SIMILARITY",
        "SUBCELLULAR LOCATION", " SUBUNIT", " TISSUE SPECIFICITY",
        " TOXIC DOSE", " WEB RESOURCE"]


class Protein():
    ''' cette classe va contenir des objets qui correspondent aux différentes lignes sur UNIPROT'''

    def __init__(self):
        self.AC = ""
        self.DT = ""
        self.ID = ""
        self.DE = ""
        self.OX = ""
        self.GN = ""
        self.OH = ""
        self.OS = ""
        self.OG = ""
        self.OC = ""
        self.reference = ""
        self.CC = ""
        self.DR = []
        self.FT = []
        self.SQ = ""
        self.KW = ""
        self.PE = ""

    def CC_list(self):
        # On va créer une liste en enlevant les "-!-""
        protCC = prot.CC.split("-!-")
        resultat = ""
        for elem in protCC:
            for character in info:
                if elem.startswith(character):
                    resultat += elem + "\n"
        return resultat

    # fonctions qui vont servir à organiser la présentation des classes
    def OS_list(self):
        for toto in prot.OS:
            yield ("\t- {}".format(toto))

    def presenter_listDR(self):
        finalResult = ""
        for thing in prot.DR:
            finalResult += "  - " + thing + "\n"  # là, pour chaque element trouvé, il print cet élément et szulzmznt lui
        return finalResult

    def presenter_listFT(self):
        dict = {}
        curretItem = ""
        for element in prot.FT:
            if element[0:16].replace(" ", "") != "":
                curretItem = element[0:16]
                dict[curretItem] = element[16:]
            else:
                dict[curretItem] = dict[curretItem] + "#" + element
        finalResult = ""
        for k, v in dict.items():
            finalResult += k
            values = v.split("#")
            for val in values:
                finalResult += val + "\n"
        return finalResult


# fonction qui va récupérer les informations recherchees dans la fiche uniprot
def group(data_uniprot_clean):
    for line in data_uniprot_clean:
        if line.startswith("ID"):
            ID = line[5:]
            prot.ID += ID
        elif line.startswith("DE"):
            DE = line[5:]
            prot.DE += DE
        elif line.startswith("AC"):
            AC = line[5:]
            prot.AC += AC
        elif line.startswith("DT"):
            DT = line[5:]
            prot.DT += DT
        elif line.startswith("GN"):
            GN = line[5:]
            prot.GN += GN
        elif line.startswith("OS"):
            OS = line[5:]
            prot.OS += OS
        elif line.startswith("OG"):
            OG = line[5:]
            prot.OG += OG
        elif line.startswith("OC"):
            OC = line[5:]
            prot.OC += OC
        elif line.startswith(liste):
            prot.reference = prot.reference + line
        elif line.startswith("OX"):
            OX = line[5:]
            prot.OX += OX
        elif line.startswith("OH"):
            OH = line[5:]
            prot.OH += OH
        elif line.startswith("CC"):
            prot.CC += line[5:]
        elif line.startswith("DR"):
            line = line.strip()
            line = line.split("DR")
            line.remove("")
            prot.DR += line
        elif line.startswith("PE"):
            PE = line[5:]
            prot.PE += PE
        elif line.startswith("KW"):
            KW = line[5:]
            prot.KW += KW
        elif line.startswith("SQ"):
            SQ = line[5:]
            prot.SQ += SQ
        elif line.startswith("FT"):
            line = line.strip()
            line = line.split("FT")
            line.remove("")
            prot.FT += line
        elif line.startswith(" "):
            prot.SQ += line[5:]


prot = Protein()


################################### TRI #################################@
name = ""


def tri_multifasta_id():
    '''une fonction qui va récupérer les informations dans le fichier multifasta puis elle fait le tri(selon le ID de biopython ce qui signifie le numéro d'accession) et stocker ces informations dans un nouveau fichier multifasta'''

    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")

    elif offline_status==True:
        try:

            handle = open(name, "rU")
            #lecture des informations dans une variable l
            l = SeqIO.parse(handle, "fasta")
            #creation d'un nouveau fichier
            file_FASTA = open(name[:-4] + "_tri_ID.fas", "w")
            #la fonction sorted tri les informations dans l selon le key(l.id)
            sortedList = [f for f in sorted(l, key=lambda x: x.id)] 
	    #ecriture des informations triées dans le nouveau ficher
            file_FASTA = open(name + "triID.fas", "w")
            sortedList = [f for f in sorted(l, key=lambda x: x.id)]
            #ecriture des informations triées dans le nouveau ficher
            for s in sortedList:
                file_FASTA.write(s.description + '\n')
                file_FASTA.write(str(s.seq) + '\n')
            #fermeture du fichier et affichage d'un message de succès
            file_FASTA.close()

            showinfo("Mission effectuée",
                     "Votre fichier a été crée et été enregistré sous format .fas sur votre répértoire courant.")
        #gestion d'erreur
        except:
            showinfo("erreur",
                     "Vous devez ouvrir un fichier multifasta pour pouvoir effectuer le tri de ID")


def tri_multifasta_gn():
    '''une fonction qui va récupérer les informations dans le fichier multifasta puis elle fait le tri(selon le GN) et stocker ces informations dans un nouveau fichier multifasta'''
    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")


    elif offline_status==True:
        try:

            handle = open(name, "rU")
            l = SeqIO.parse(handle, "fasta")
            file_FASTA = open(name[:-4] + "_tri_GN.fas", "w")
            #la fonction sorted tri les informations dans l selon le key("GN") qui est recupérer en utilisant la fonction .split() 
            sortedList = [f for f in sorted(l, key=lambda x: x.description.split("GN=")[1].split(" ")[0].upper())] #on utilise upper() pour trier dans le bon ordre sans prendre en complte les minuscules et les mettres tous en majuscules avant

            for s in sortedList:
                file_FASTA.write(s.description + '\n')
                file_FASTA.write(str(s.seq) + '\n')

            file_FASTA.close()

            showinfo("Mission effectuée",
                     "Votre fichier a été crée et été enregistré sous format .fas.")

        #gestion d'erreur
        except:
            showinfo("erreur",
                     "Vous devez ouvrir un fichier multifasta pour pouvoir effectuer le tri de GN")


def tri_multifasta_os():
    '''une fonction qui va récupérer les informations dans le fichier multifasta puis elle fait le tri(selon OS de biopython ce qui signifie le numéro d'accession) et stocker ces informations dans un nouveau fichier multifasta'''

    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")


    elif offline_status==True:

        try:
            handle = open(name, "rU")
            l = SeqIO.parse(handle, "fasta")
            file_FASTA = open(name[:-4] + "_tri_OS.fas", "w")
            #la fonction sorted tri les informations dans l selon le key("OS") qui est recupérer en utilisant la fonction .split() 
            sortedList = [f for f in sorted(l, key=lambda x: x.description.split("OS=")[1].split(" ")[0].upper())]

            for s in sortedList:
                file_FASTA.write(s.description + '\n')
                file_FASTA.write(str(s.seq) + '\n')

            file_FASTA.close()

            showinfo("Mission effectuée",
                     "Votre fichier a été crée et été enregistré sous format .fas.")


        #gestion d'erreur
        except:
            showinfo("erreur",
                     "Vous devez ouvrir un fichier multifasta pour pouvoir effectuer le tri de OS")


def tri_multifasta_taille():
    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")


    elif offline_status==True:

        try:

            handle = open(name, "rU")
            l = SeqIO.parse(handle, "fasta")
            file_FASTA = open(name[:-4]+"_tri_taille.fas", "w")
            sortedList = [f for f in sorted(l, key=lambda x: len(x.seq))]

            for s in sortedList:
                file_FASTA.write(s.description + '\n')
                file_FASTA.write(str(s.seq) + '\n')

            file_FASTA.close()

            showinfo("Mission effectuée",
                     "Votre fichier a été crée et été enregistré sous format .fas sur votre répértoire courant.")
        except:
            showinfo("erreur",
                     "Vous devez ouvrir un fichier multifasta pour pouvoir effectuer le tri de la taille de la séquence")
############################################# FIlTRE #################################@
     
def fil_multifasta_oxsup(x):
    """cette fonction va récupérer les informations d'un fichier multifasta puis va le filtrer en fontion de OX et le stockage ces informations dans un nouveau fichier multifasta"""
    try:

        handle = open(name, "rU")
        #lecture des informations dans une variable l
        l = SeqIO.parse(handle, "fasta")
        #creation d'un nouveau fichier
        file_FASTA = open(name[:-4]+"_filtre_OX_sup.fas", "w")
        #on fait le filtre en fonction de OX des informations recupérer et on les stockes dans sortedList, comme expliquer dans la fonction tri 
        sortedList = [f for f in sorted(l, key=lambda x: int(x.description.split("OX=")[1].split()[0]))]
        #on parcourt sorted list et on elimine toutes les lignes où OX est supérieur à une valeur donnée X par l'utilisateur
        sortedList = [f for f in sortedList if int(f.description.split("OX=")[1].split()[0]) > x.get()] 
        #écriture des informations filtrées dans le nouveau ficher
        for s in sortedList:
            file_FASTA.write(s.description + '\n')
            file_FASTA.write(str(s.seq) + '\n')
					
		#fermeture du fichier et affichage d'un message de succès
        file_FASTA.close()

        showinfo("Mission effectuée",
                 "Votre fichier a été crée et été enregistré sous format .fas sur votre répértoire courant.")
	#gestion d'erreur
    except:
        showinfo("erreur",
                 "Vous devez ouvrir un fichier multifasta pour pouvoir effectuer le filtre en fonction de l'Organism taxonom")

def fil_multifasta_pesup(x):
    """cette fonction va récupérer les informations d'un fichier multifasta puis va le filtrer en fontion de PE et le stockage ces informations dans un nouveau fichier multifasta"""
    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")


    elif offline_status==True:

        handle = open(name, "rU")
        l = SeqIO.parse(handle, "fasta")
        file_FASTA = open(name[:-4]+"_filtre_PE_sup.fas", "w")
        sortedList = [f for f in sorted(l, key=lambda x: int(x.description.split("PE=")[1].split()[0]))]
        #on parcourt sorted list et on elimine toutes les lignes où PE est supérieur à une valeur donnée X par l'utilisateur
        sortedList = [f for f in sortedList if int(f.description.split("PE=")[1].split()[0]) > x.get()]
        for s in sortedList:
            file_FASTA.write(s.description + '\n')
            file_FASTA.write(str(s.seq) + '\n')

        file_FASTA.close()

        showinfo("Mission effectuée",
                 "Votre fichier a été crée et été enregistré sous format .fas sur votre répértoire courant.")



def fil_multifasta_oxinf(x):
    """cette fonction va récupérer les informations d'un fichier multifasta puis va le filtrer en fontion de OX et le stockage ces informations dans un nouveau fichier multifasta"""
    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")


    elif offline_status==True:

        handle = open(name, "rU")
        l = SeqIO.parse(handle, "fasta")
        file_FASTA = open(name[:-4]+"_filtre_OX_inf.fas", "w")
        sortedList = [f for f in sorted(l, key=lambda x: int(x.description.split("OX=")[1].split()[0]))]
        #on parcourt sorted list et on elimine toutes les lignes où OX est inférieur à une valeur donnée X par l'utilisateur
        sortedList = [f for f in sortedList if int(f.description.split("OX=")[1].split()[0]) < x.get()]
 
        for s in sortedList:
            file_FASTA.write(s.description + '\n')
            file_FASTA.write(str(s.seq) + '\n')

        file_FASTA.close()

        showinfo("Mission effectuée",
                 "Votre fichier a été crée et été enregistré sous format .fas sur votre répértoire courant.")



def fil_multifasta_peinf(x):
    """cette fonction va récupérer les informations d'un fichier multifasta puis va le filtrer en fontion de PE et le stockage ces informations dans un nouveau fichier multifasta"""
    if offline_status==False:
        showwarning("Message d'erreur", "les options tri/filtre ne sont fonctionnelles qu'avec les fichiers multifasta")


    elif offline_status==True:
        handle = open(name, "rU")
        l = SeqIO.parse(handle, "fasta")
        file_FASTA = open(name[:-4]+"_filtre_PE_inf.fas", "w")
        sortedList = [f for f in sorted(l, key=lambda x: int(x.description.split("PE=")[1].split()[0]))]
        #on parcourt sorted list et on elimine toutes les lignes où PE est inferieur à une valeur donnée X par l'utilisateur
        sortedList = [f for f in sortedList if int(f.description.split("PE=")[1].split()[0]) < x.get()]
        for s in sortedList:
            file_FASTA.write(s.description + '\n')
            file_FASTA.write(str(s.seq) + '\n')

        file_FASTA.close()

        showinfo("Mission effectuée",
                 "Votre fichier a été crée et été enregistré sous format .fas sur votre répértoire courant.")


################## Demander quel code traiter ############################

class utile():
    """  Cette classe récupère les numéros d'accession dans le fichier multifasta """

    def __init__(self):
        self.list_NA = []
        self.position={}

rec = utile()


###################################### fichier offline ##############################################

offline_status=False
def newfile():
    """ Cette fonction va ouvrir le fichier offline et récupérer les codes d'accessions   """
    global offline_status
    offline_status = True
    try:
        j=0
        offline_file = askopenfile(mode='r', title="Ouvrir un nouveau fichier fasta", filetypes=[('FAS file', '.fas')])
        global name
        # Ici je lui dis de stocker le nom du fichier dans la variable name
        name = os.path.basename(offline_file.name)
        for line in offline_file.readlines():
            j+=1
            if line.startswith(">"):
                rec.position[line[4:10]]=j-1
                rec.list_NA.append(line[4:10])
        Label(
            text="votre fichier Fasta contient les protéines suivantes, copier/coller un numéro d'accession dans le champs de saisie pour commencer le traitement:{}".format(
                rec.list_NA), background="peach puff").place(y=500, x=30)
     
        offline_file.close()
        global message_inpute
        message_inpute = Label(fenetre, text="Veuillez saisir le numéro d'accession qui vous intéresse parmi ceux du fichier multifasta svp.", background="peach puff").place(y=20, x=500)

    #Quand l'utilisateur annule l'importation du fichier Fasta, ceci induit une erreur d'attribution, car name se retroune avec aucun nom de fichier
    # Si ça arrive, il n'y aura pas de message d'erreur sur le shell
    except AttributeError:
        offline_status = False
        pass 



#################################### Alignement global #################################################@

global match 
global mismatch
global MIN
global A
global B
global E
global F
global G

score = 0
A   = -10.
B   = -1.
match = 1.
mismatch = -0.
MIN = -float("inf")
# il prend des matrices dont les valeurs sont nul (none)
E=None
F=None
G=None

def read_blosum():
   #il a ouvert le fichier de la matrice de substitution et il a nommé f 
    with open('BLOSUM62.txt') as f:
        #il va parcourir les lignes
        lines = f.readlines()
    #il va ouvrir une variable global qui s'appelle alignment_score
    global alignment_score
    #declare la variable comme etant une liste vide 
    alignment_score = []
    # pour i allant de 1 à la longuer des lignes
    for i in range (1, len(lines)):
        #il fractionne les lignes de chaque i en une liste où chaque ligne est un élément de la liste et on l'est stockes dans la variable globale 
        alignment_score = alignment_score + [ lines[i].split() ]  
    #  On a stocké tous les score dans une liste de listes
    alignment_score = [line[1:] for line in alignment_score]

    global alignmentIndices
    # on stocke la première ligne dans alignement indices
    alignmentIndices = lines[0].split()


read_blosum()

def get_score(a, b):
    ''' Cette fonction va permettre d'obtenir le score entre deux acides aminées'''
    indice_a = -1
    indice_b = -1
    for i in range(0, len(alignmentIndices)):
        # si a se trouve dans ma liste des AA de la première ligne alors on stocke sa position
        if (a == alignmentIndices[i]):
            indice_a = i
        # si b se trouve dans ma liste des AA de la première ligne alors on stocke sa position aussi
        if (b == alignmentIndices[i]):
            indice_b = i
    # Ici, vu que les AA sont rangés de la même façon verticalement et horizentalement, alors si a est à la position 2 alors b sera autant plus loin horizentalement que verticalement
    return int(alignment_score[indice_a][indice_b])


#print(get_score('A','F'))



def initialisation_x(i, j):
    if i > 0 and j == 0:
        return MIN
    else: 
        if j > 0:
            return -10 + (-0.5 * j)
        else:
            return 0



def initialisation_y(i, j):
    if j > 0 and i == 0:
        return MIN
    else:
        if i > 0:
            return -10 + (-0.5 * i)
        else:
            return 0




def initialisation_m(i, j):
    #print("i est égale à : {} et j est égale à : {}". format(i,j))
    if j == 0 and i == 0:
        return 0
    else:
        if j == 0 or i == 0:
            #MIN= -float("inf")
            return MIN
        else:
            return 0




def matrice_distance(s, t):
    ''' Cette fonction va créer une matrice de distance pour l'utiliser dans la programmation dynamique   '''
    #j est de 0 à taille de la sequence s, i est 0 à la taille de sequence t
    global E
    global F
    global G
    E = [[initialisation_x(i, j) for j in range(0, len(s) + 1)] for i in range(0, len(t) + 1)]
    #print("E c'est : {}". format(E))
    F = [[initialisation_y(i, j) for j in range(0, len(s) + 1)] for i in range(0, len(t) + 1)]
    #print("F c'est : {}". format(F))
    G = [[initialisation_m(i, j) for j in range(0, len(s) + 1)] for i in range(0, len(t) + 1)]
    #print("G c'est : {}". format(G))
    for j in range(1, len(s) + 1):
        for i in range(1, len(t) + 1):
            E[i][j] = max((A + B + G[i][j-1]), (B + E[i][j-1]), (A + B + F[i][j-1]))
            F[i][j] = max((A + B + G[i-1][j]), (A + B + E[i-1][j]), (B + F[i-1][j]))
            G[i][j] = max(get_score(t[i - 1], s[j - 1]) + G[i-1][j-1], E[i][j], F[i][j])
    return [E, F, G]



def backtracking(s, t, E, F, G):
    seq1 = ''
    seq2 = ''
    i = len(t)
    j = len(s)
    score = G[i][j]
    while (i>0 or j>0):
        if (i>0 and j>0 and G[i][j] == G[i-1][j-1] + get_score(t[i - 1], s[j - 1])):
            seq1 += s[j-1]
            seq2 += t[i-1]
            i -= 1; j -= 1
        elif (i>0 and G[i][j] == F[i][j]):
            seq1 += '_'
            seq2 += t[i-1]
            i -= 1
        elif (j>0 and G[i][j] == E[i][j]):
            seq1 += s[j-1]
            seq2 += '_'
            j -= 1

    seq1r = ' '.join([seq1[j] for j in range(-1, -(len(seq1)+1), -1)])
    seq2r = ' '.join([seq2[j] for j in range(-1, -(len(seq2)+1), -1)])

    return [seq1r, seq2r, score]


##################################### Alignement local #######################################################


def populateScoreDictionary(scoreLines):
    """ Cette fonction retourne un dictionnaire construit à partir de la matrice importé BLOSUM62 et qui contient la valeur des scores 
    pour chaque combinaison de paires d'acides aminées """
    scoringDictionary = {}
    
    seqList = scoreLines[0]
    seqList = seqList.split()
    
    i = 1
    j = 1
    for i in range(1, len(scoreLines) - 1, 1):
        row = scoreLines[i]
        row = row.split()
        
        for matchValue in row[1:len(scoreLines) - 1]:
            scoringDictionary[seqList[i-1], seqList[j-1]] = int(matchValue)
            j += 1
        
        j = 1
    
    return scoringDictionary


    
def populateScoreMatrix(scoreMatrix, numRow, numCol, scoreDictionary, refSeq, querySeq, openGap, extGap):
    """ Cette fonction crée une matrice avec des valeurs selon l'algorithme de Smith-Waterman. Cela se fait en itérant de (1,1) dans scoreMatrix à (numRow - 1, numCol - 1)
    Une valeur de scoreMatrix[i][j] est déterminée par les paramètres suivants:
        scoreMatrix[i][j] = max(scoreMatrix[i-1][j-1] + matschore[i][j],
                            max(scoreMatrix[i][j - k] - gapCost),
                            max(scoreMatrix[i - k][j] - gapCost),
                            0)
                        où 1 <= k < numCol, 1 <= l < numRow, et
                              gapCost = openGap - n * extGap où n = k (or l) - 1"""
    


    #On ignore la colonne 0 de la ligne 0
    for i in range(1, numRow, 1):
        for j in range(1, numCol, 1):
        
            #Initialisation de la matrice initiale qui stocke les positions des 4 valeurs possibles qui peuvent être assignées à la matrice[i][j]
                #maxValue[0] correspond à la valeur obtenue, diagonalement, à partir d'en haut à gauche (match/mismatch)
                #maxValue[1] correspond à la valeur obtenue à partir d'en haut (insertions)
                #maxValue[2] correspond à la valeur obtenue à partir de gauche (deletions)
                #maxValue[3] est 0
            maxValues = np.zeros(4, np.int)
                 
            #Récupérer le score de match/mismatch de scoringDictionary
            matchscore = scoreDictionary[refSeq[i - 1], querySeq[j - 1]]
            maxValues[0] = matchscore + scoreMatrix[i -1][j - 1]
        
        
            #itérer les lignes de i - 1 à zéro dans la colonne j et trouver la valeur maximale - gapCost
            #numGap garde une trace du nombre de gaps qui ont été introduites afin que la pénalité extGapCost puisse être appliquée
            numGap = 0
            maxAbovePosition_ij = 0  
                  
            for k in range(i - 1, 0, -1):
                temp = scoreMatrix[k][j] + openGap + (numGap * extGap)
                  
                if temp > maxAbovePosition_ij:
                    maxAbovePosition_ij = temp
                      
                numGap += 1
            
        
            maxValues[1] = maxAbovePosition_ij

              
            numGap = 0
            maxLeftPosition_ij = 0
        
            for m in range(j - 1, 0, -1):
                temp = scoreMatrix[i][m] + openGap + (numGap * extGap)
                  
                if temp > maxLeftPosition_ij:
                    maxLeftPosition_ij = temp
                      
                numGap += 1
              
            maxValues[2] = maxLeftPosition_ij
            

            #stocke la valeur maximale calculée
            scoreMatrix[i][j] = np.max(maxValues)



def traceback(optimalPath, scoreMatrix, i, j):
    """ Cette fonction Trouve les prochains indices des chemins optimaux dans l'alignement de scoreMatrix à partir d'une coordonnée de départ dans 
    scorMatrix 
    # La position optimale qui suit dans l'alignement local est déterminée par les paramètres suivants: 
        nextPostion = scoreMatrix indices at max(scoreMatrix[i - 1][j - 1], scoreMatrix[i][j - 1], scoreMatrix[i - 1][j])

    PS: si scoreMatrix[i - 1][j - 1] == scoreMatrix[i][j - 1] == scoreMatrix[i - 1][j],
            alors scoreMatrix[i - 1][j - 1] va être choisi comme le prochain chemin optimal (matches/mismatches sont prioritaires par rapport aux insertions/deletions) 

        si scoreMatrix[i - 1][j - 1] < scoreMatrix[i][j - 1] == scoreMatrix[i - 1][j],
            alors scoreMatrix[i][j - 1] va petre choisi comme le prochain chemin optimal (deletions sont prioritaires par rapport aux insertions)
 """

    if scoreMatrix[i][j] > 0:
        ############################voir figure dans le rapport pour une meilleure visualisation ##################
        #Stockage des valeur du prochain chemin possible 
        #nextPositionValues[0] correspond au diagonal d'en haut à gaiche de la position actuelle (match/mismatch)
        #nextPositionValues[1] correspond à la gauche de la position actuelle (deletion)
        #nextPositionValues[2] correspond au dessus de la position actuelle (insertion)
        
        nextPositionValues = np.array([scoreMatrix[i - 1][j - 1], scoreMatrix[i][j-1], scoreMatrix[i -1][j]])
    
        #Vérfier si une position avec une valeur de 0 est rencontré, sinon trouver la prochaine valeur maximale
        #PS: argmax trouve la première position de max, ainsi les mismatches vont être prioritisés par rapport aux gaps
        if np.min(nextPositionValues) == 0:
            index = np.argmin(nextPositionValues)
        else:
            index = np.argmax(nextPositionValues)
    
                #determiner les coordonées dans la matrice
        if index == 0:
            i2 = i - 1
            j2 = j - 1
    
        elif index == 1:
            i2 = i
            j2 = j - 1
        else:
            i2 = i -1
            j2 = j
    
        #Ajouter les coordonnées de la prochaine position dans la matrice du chemin optimal 
        optimalPath = np.vstack((optimalPath, [i2, j2]))
        
        #appeler récursivement la fonction et stocker les résultats
        optimalPath = traceback(optimalPath, scoreMatrix, i2, j2)
            
    return(optimalPath)




def printScoreMatrix(scoreMatrix, refSeq, querySeq, file_local_align):
    """ Cette fonction va servir à bien présenter les données"""    
    
    rowInScoreMatrix = ['', '']
    
    for j in range(0, len(querySeq) - 1, 1):
        rowInScoreMatrix.append(querySeq[j])
    
    rowString = '\t'.join(rowInScoreMatrix)
    
    file_local_align.write(rowString + '\n')
    
    #Print the second row, which has no label and contains only zero values
    rowInScoreMatrix = [' ']
    for j in range(0, len(querySeq), 1):
        
        matrixValue = str(scoreMatrix[0][j])
        rowInScoreMatrix.append(matrixValue)
    
    rowString = '\t'.join(rowInScoreMatrix)
    
    file_local_align.write(rowString + '\n')
    
    
 
    for i in range(0, len(refSeq), 1):
        
   
        rowInScoreMatrix = [refSeq[i], '0']
        

        for j in range(1, len(querySeq), 1):
            
            matrixValue = str(scoreMatrix[i + 1][j])
            rowInScoreMatrix.append(matrixValue)
            
        rowString = '\t'.join(rowInScoreMatrix)
    
        file_local_align.write(rowString + '\n')

    file_local_align.write('\n')



def printAlignment(optimalPath, refSeq, querySeq, file_local_align):
    """ Cette fonction sert à Aligner les caractère de querySeq à refSeq selon les coordonnées de optimalPath"""
    
    #rotation de optimalPath pour que l'alignement se fasse de gauche à droite
    optimalPath = np.flip(optimalPath, 0)
    
    #Convertir la séquence en liste pour faciliter l'accès 
    rSeq = list(refSeq)
    qSeq = list(querySeq)


    #Listes pour l'alignement  
    alignQ = []
    alignRef = []
    alignMatch = []
    
    #Si l'alignement contient des indels/mismatches
    
    if optimalPath[0][0] > 1 or optimalPath[0][1] > 1:
        num = abs(optimalPath[0][0] - optimalPath[0][1])
        
        #Si l'alignement contient des INDELS
        if num > 0:
            insertion = optimalPath[0][0] < optimalPath[0][1]
            
            if insertion:
                for i in range(0, num, 1):
                    alignQ.append(qSeq.pop(0))
                    alignRef.append(' ')
                    alignMatch.append(' ')
            
            #Sinon c'est une délétion
            else:
                for i in range(0, num, 1):
                    alignQ.append(' ')
                    alignRef.append(rSeq.pop(0))
                    alignMatch.append(' ')               
    
        
        
        for i in range(num, max(optimalPath[0,:])):
                    alignQ.append(qSeq.pop(0))
                    alignRef.append(rSeq.pop(0))
                    alignMatch.append(' ')
    

    alignQ.append('(')
    alignRef.append('(')
    alignMatch.append(' ')
    
    
    for i in range(0, np.size(optimalPath, 0) - 1, 1):
        
        #Vérifier l'insertion
        if optimalPath[i][0] == optimalPath[i + 1][0]:
            alignQ.append(qSeq.pop(0))
            alignRef.append('-')
            alignMatch.append(' ')
        
        #Vérifier la délétion 
        elif optimalPath[i][1] == optimalPath[i + 1][1]:
            alignQ.append('-')
            alignRef.append(rSeq.pop(0))
            alignMatch.append(' ')
        
        #Sinon match/mismatch
        else:
            alignQ.append(qSeq.pop(0))
            alignRef.append(rSeq.pop(0))
            
            #If match
            if alignQ[-1] == alignRef[-1]:
                alignMatch.append('|')
            else:
                alignMatch.append(' ')

    #L'alignement local est terminé
    alignQ.append(')')
    alignRef.append(')')
    alignMatch.append(' ')
    
    
    #Print les deletions/insertions/mismatches qui sont après local alignment
    while len(qSeq) > 0:
        alignQ.append(qSeq.pop(0))
    
    while len(rSeq) > 0:
        alignRef.append(rSeq.pop(0))
    
    
    #Convertir la liste en string pour les afficher dans le fichier résultat
    queryAlignment = ''.join(alignQ)
    matchAlignment = ''.join(alignMatch)
    refAlignment = ''.join(alignRef)
    
    #Wécrire les résultats
    file_local_align.write(queryAlignment + '\n')
    file_local_align.write(matchAlignment + '\n')
    file_local_align.write(refAlignment + '\n')





def runSW(seq1,seq2, scoreFile, openGap, extGap):
  
    querySeq = seq1
    refSeq = seq2


    
    
    #R2cupération des scores de la matrice Blosum62
    inputScoreFile = open(scoreFile, 'r')
    scoreLines = inputScoreFile.readlines()
    inputScoreFile.close()
    
    #Creation de dictionnaire à partir de la matrice 
    scoreDictionary = populateScoreDictionary(scoreLines)
    
    #Initialisation de la matrice de scores (n + 1, m + 1)
    #Les lignes correspondent à seq1
    #Les colonnes correspondent à seq2
    numRow = len(refSeq) + 1
    numCol = len(querySeq) + 1
    scoreMatrix = np.zeros((numRow, numCol), np.int)
    
    #Calculer et remplir les valeurs de scoreMatrix 
    populateScoreMatrix(scoreMatrix, numRow, numCol, scoreDictionary, refSeq, querySeq, openGap, extGap)
    


    #Trouver les coordonnées de la valeur maximale et la stocker dans un tableau
    maxValueInScoreMatrix = scoreMatrix.argmax()
    maxValueCoordinates = np.asarray(np.unravel_index(maxValueInScoreMatrix, (numRow, numCol)))

    #Traceback : trouve le chemin optimal
    optimalPath = traceback(maxValueCoordinates, scoreMatrix, maxValueCoordinates[0], maxValueCoordinates[1])
    
    file_local_align =  tkinter.filedialog.asksaveasfile(mode ='w', initialdir = "/",title = "Enregistrer les résultats de l'alignement",filetypes = (("*.txt","*.txt"),("all files","*.*")))
    file_local_align.write("----------------------------------------------------\n")
    file_local_align.write("|    Sequences                                     |\n")
    file_local_align.write("----------------------------------------------------\n")

    file_local_align.write("sequence1\n")
    file_local_align.write(querySeq + '\n')
    file_local_align.write("sequence2\n")
    file_local_align.write(refSeq + '\n')

    file_local_align.write("----------------------------------------------------\n")
    file_local_align.write("|    Score Matrix                                  |\n")
    file_local_align.write("----------------------------------------------------\n")
    file_local_align.write('\n')
    printScoreMatrix(scoreMatrix, refSeq, querySeq, file_local_align)


    file_local_align.write("----------------------------------------------------\n")
    file_local_align.write("|    Best Local Alignment                          |\n")
    file_local_align.write("----------------------------------------------------\n") 
    file_local_align.write('\n')
    file_local_align.write("Alignment Score:    " + str(np.max(scoreMatrix)) + "\n")
    
    printAlignment(optimalPath, refSeq, querySeq, file_local_align)
    
    file_local_align.close()



import argparse
import numpy as np


parser = argparse.ArgumentParser(description='Smith-Waterman Algorithm')
parser.add_argument('-o', '--opengap', help='open gap', required=False, default=-10)
parser.add_argument('-e', '--extgap', help='extension gap', required=False, default=-0.5)
args = parser.parse_args()






###############################################################################################################
global s
global t

def align_global():
    """ Cette fonction est appelée par le bouton 'ALIGN' pour avoir le résultat de l'alignement """
    global s
    global t
    s=seqs.get()
    t=seqt.get()
    matrice_distance(s,t)
    seq1, seq2, align_score=backtracking(s,t,E,F,G)
    try:
        file_align =  tkinter.filedialog.asksaveasfile(mode ='w', initialdir = "/",title = "Enregistrer les résultats de l'alignement",filetypes = (("*.txt","*.txt"),("all files","*.*")))
        file_align.write( ('le résultat de cet alignement donne un score de {}'.format(align_score))+ '\n' +  seq1 +'\n'+ '\n'+seq2)
        file_align.close()

    except PermissionError:
        showwarning("Message d'erreur", "Veuillez choisir un autre répertoire pour enregistrer votre fichier")
    


        



global seqs
global seqt
global alignement
def align_seq():
    """ Cette fonction est appelée quand l'utilisateur clique sur alignement global. Elle affiche une nouvelle fenêtre où il faut rentrer les 2 séquences à aligner """
    global alignement
    alignement=Tk()
    alignement.title("ALIGNEMENT GLOBAL")
    alignement.geometry("1500x400")
    alignement.configure(bg='cornflower blue')
    global seqs
    global seqt
    seqs=StringVar(alignement, value="")
    seqt=StringVar(alignement, value="")
    message = Label(alignement, text="Veuillez insérer les 2 séquences que vous voulez aligner svp").place(y=70, x=450)
    seq_1=Label(alignement, text="sequence 1 :", width=10, anchor='w', bg='cornflower blue').place(y=100, x=200)
    inpute1 = Entry(alignement, textvariable=seqs, width=80).place(y=100, x=300)
    seq_2=Label(alignement, text="sequence 2 :", width=10, anchor='w', bg='cornflower blue').place(y=150, x=200)
    inpute2 = Entry(alignement, textvariable=seqt, width=80).place(y=150, x=300)
    global_align=Button(alignement, text="Alignement global", width=15, command=align_global, background="peach puff")
    global_align.place(y=200, x=400)
    local_align=Button(alignement, text="Alignement local", width=15, command=align_local, background="peach puff")
    local_align.place(y=200, x=700)



def align_local():
    seq1=seqs.get()
    seq2=seqt.get()
    runSW(seq1,seq2,'Blosum62.txt', args.opengap, args.extgap)






















































