#LAGHISSI Hiba, MARIAULT Lee et AMMAR Fatma

# coding: utf-8
from tkinter import Tk
from tabulate import tabulate
from function import *
from tkinter import *
import os

############################## Liste de variables utiles #########################

###### Variables utilisées pour les premiers boutons qui apparaissent
check1 = IntVar()
check2 = IntVar()
check3 = IntVar()
check4 = IntVar()
check5 = IntVar()
check6 = IntVar()
check7 = IntVar()
check8 = IntVar()
check9 = IntVar()

choice1 = IntVar()
choice2 = IntVar()
choice3 = IntVar()
choice4 = IntVar()
choice5 = IntVar()
choice6 = IntVar()
choice7 = IntVar()
choice8 = IntVar()
choice9 = IntVar()
choice10 = IntVar()
choice11 = IntVar()
choice12 = IntVar()
choice13 = IntVar()
choice14 = IntVar()
choice15 = IntVar()
choice16 = IntVar()
choice17 = IntVar()


###### Variables utilisées pour les deuxièmes boutons (de classes) qui apparaissent

choix1 = IntVar()
choix2 = IntVar()
choix3 = IntVar()
choix4 = IntVar()
choix5 = IntVar()
choix6 = IntVar()
choix7 = IntVar()
choix8 = IntVar()
choix9 = IntVar()
choix10 = IntVar()
choix11 = IntVar()
choix12 = IntVar()
choix13 = IntVar()
choix14 = IntVar()
choix15 = IntVar()
choix16 = IntVar()
choix17 = IntVar()
choix18 = IntVar()
choix19 = IntVar()
choix20 = IntVar()
choix21 = IntVar()
choix22 = IntVar()
choix23 = IntVar()
choix24 = IntVar()
choix25 = IntVar()

oxsup = IntVar()
pesup = IntVar()
oxinf = IntVar()
peinf = IntVar()
r = IntVar()



global offline_status

############################ Bouton de démarrage go #############################################
# code est Q59297 ty 
def go():
    ''' Cette fonction est appelée par le bouton go, elle-même appelle d'autres fonctions selon la case coché'''


      
    file_change()
    if check1.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            acces_fichier_UNIPROT()
    if check2.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            acces_fichier_FASTA()
    if check3.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            bouton_hydrophobicite()        
    if check4.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            bouton_occurence()
    if check5.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            bouton_taille()
    if check6.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            bouton_PM()
    if check7.get() == 1:
        if NA.get()=="":
            showwarning("Message d'erreur", "Veuillez insérer un numéro d'accession svp.")
        else:
            autre_choix()
    if check8.get() == 1:  
        autre_choix()
    if check9.get() == 1:  
        autre_choix()
    if choix18.get() == 1:  
        tri_multifasta_id()
    if choix19.get() == 1:  
        tri_multifasta_gn()
    if choix20.get() == 1:  
        tri_multifasta_os()
    if choix25.get() == 1:  
        tri_multifasta_taille()


def Intercepte():
    showinfo("Au plaisir de vous revoir","à la prochaine !")
    fenetre.destroy()
    
fenetre.protocol("WM_DELETE_WINDOW", Intercepte)





######################### Fonction appelé par la case "plus d'infos" pour afficher les différentes possibilités à cocher #########################
def autre_choix():
    ''' cette fonction prend en charge le bouton "Infos plus spécifiques" si l'utilisateur clique dessus et genère 17 autres choix selon l'info'''
    if check7.get() == 1:
        button = Button(fenetre, text="Afficher", width=30, command=afficher).place(y=420, x=900)
        choice1 = Checkbutton(fenetre, text="ID : Identification", width=30, variable=choix1, anchor="w", bg='chocolate').place(y=80,x=900)
        choice2 = Checkbutton(fenetre, text="AC : Accession number", width=30, variable=choix2, anchor="w", bg='chocolate').place(y=100,x=900)
        choice3 = Checkbutton(fenetre, text="DT : Date", width=30, variable=choix3, anchor="w", bg='chocolate').place(y=120, x=900)
        choice4 = Checkbutton(fenetre, text="DE : Description", width=30, variable=choix4, anchor="w", bg='chocolate').place(y=140,x=900)
        choice5 = Checkbutton(fenetre, text="GN : Gene Name", width=30, variable=choix5, anchor="w", bg='chocolate').place(y=160, x=900)
        choice6 = Checkbutton(fenetre, text="OS : Organism Species", width=30, variable=choix6, anchor="w", bg='chocolate').place(y=180,x=900)                                                                                                                
        choice7 = Checkbutton(fenetre, text="OG : Organelle", width=30, variable=choix7, anchor="w", bg='chocolate').place(y=200, x=900)
        choice8 = Checkbutton(fenetre, text="OC : Organism Classification", width=30, variable=choix8,anchor="w", bg='chocolate').place(y=220, x=900)
        choice9 = Checkbutton(fenetre, text="OX : Organism taxonomy cross-reference", width=30, variable=choix9,anchor="w", bg='chocolate').place(y=240, x=900)
        choice10 = Checkbutton(fenetre, text="OH : Organism Host", width=30, variable=choix10, anchor="w", bg='chocolate').place(y=260,x=900)
        choice11 = Checkbutton(fenetre, text="The reference : RN, RP, RC, RX, RG, RA, RT, RL lines", width=30,variable=choix11, anchor="w", bg='chocolate').place(y=280, x=900)
        choice12 = Checkbutton(fenetre, text="CC : free text comments", width=30, variable=choix12, anchor="w", bg='chocolate').place(y=300, x=900)
        choice13 = Checkbutton(fenetre, text="DR : Database cross-Reference", width=30, variable=choix13,anchor="w", bg='chocolate').place(y=320, x=900)
        choice14 = Checkbutton(fenetre, text="PE : Protein Existence", width=30, variable=choix14, anchor="w", bg='chocolate').place(y=340,x=900)
        choice15 = Checkbutton(fenetre, text="KW : KeyWord", width=30, variable=choix15, anchor="w", bg='chocolate').place(y=360,x=900)
        choice16 = Checkbutton(fenetre, text="FT : Feature Table", width=30, variable=choix16, anchor="w", bg='chocolate').place(y=380,x=900)
        choice17 = Checkbutton(fenetre, text="SQ : Sequence header", width=30, variable=choix17, anchor="w", bg='chocolate').place(y=400, x=900)



    global offline_status

            

    if check8.get() == 1: 
        Label(text="Veuillez choisir le critère du tri par ordre alphabétique :", bg='chocolate').place(y=150, x=20)
        choice18 = Checkbutton(fenetre, text="ID : Identification", width=30, variable=choix18, anchor="w", bg='chocolate').place(y=170, x=20)
        choice19 = Checkbutton(fenetre, text="GN : Gene Name", width=30, variable=choix19, anchor="w", bg='chocolate').place(y=190, x=20)
        choice20 = Checkbutton(fenetre, text="OS : Organism Species", width=30, variable=choix20, anchor="w", bg='chocolate').place(y=210, x=20)
        choice25 = Checkbutton(fenetre, text="tri croissant en fonction de la taille", width=30, variable=choix25, anchor="w", bg='chocolate').place(y=230, x=20)
 

    if check9.get() == 1:

        labelfiltre = Label(text="Veuillez choisir une option de filtre par une valeur maximum ou minimum :".format(dico), background="chocolate")
        labelfiltre.place(y=280,x=20)

        choice21 = Checkbutton(fenetre, text="OX >", width=8, variable=choix21, anchor="w", background="chocolate")
        choice21.place(y=310, x=20)
        w1 = Entry(fenetre, textvariable=oxsup, width=20, background="peach puff")
        w1.place(y=310, x=100)

        choice22 = Checkbutton(fenetre, text="PE >", width=8, variable=choix22, anchor="w",background="chocolate")
        choice22.place(y=340, x=20)
        w2 = Entry(fenetre, textvariable=pesup, width=20, background="peach puff")
        w2.place(y=340, x=100)

        choice23 = Checkbutton(fenetre, text="OX <", width=8, variable=choix23, anchor="w",background="chocolate")
        choice23.place(y=370, x=20)
        w3 = Entry(fenetre, textvariable=oxinf, width=20, background="peach puff")
        w3.place(y=370, x=100)

        choice24 = Checkbutton(fenetre, text="PE <", width=8, variable=choix24, anchor="w",background="chocolate")
        choice24.place(y=400, x=20)
        w4 = Entry(fenetre, textvariable=peinf, width=20, background="peach puff")
        w4.place(y=400, x=100)



########################### Sortie sous forme de fichier tabulé ##################################




def afficher():
    '''  Cette fonction va créer le fichier tabulé en fonction des choix de l'utilisateur  '''
    firstRow = []
    secondRow = []
    initRow = 230
    initColumn = 60
    acces_class()

    if choix1.get() == 1:
        initColumn += 10
        firstRow.append("ID")
        secondRow.append(prot.ID)
    if choix2.get() == 1:
        initColumn += 10
        firstRow.append("AC")
        secondRow.append(prot.AC)
    if choix3.get() == 1:
        initColumn += 10
        firstRow.append("DT")
        secondRow.append(prot.DT)
    if choix4.get() == 1:
        initColumn += 10
        firstRow.append("DE")
        secondRow.append(prot.DE)
    if choix5.get() == 1:
        initColumn += 10
        firstRow.append("GN")
        secondRow.append(prot.GN)
    if choix6.get() == 1:
        initColumn += 10
        firstRow.append("OS")
        secondRow.append(prot.OS)
    if choix7.get() == 1:
        initColumn += 10
        firstRow.append("OG")
        secondRow.append(prot.OG)
    if choix8.get() == 1:
        initColumn += 10
        firstRow.append("OC")
        secondRow.append(prot.OC)
    if choix9.get() == 1:
        initColumn += 10
        firstRow.append("OX")
        secondRow.append(prot.OX)
    if choix10.get() == 1:
        initColumn += 10
        firstRow.append("OH")
        secondRow.append(prot.OH)
    if choix11.get() == 1:
        initColumn += 10
        firstRow.append("reference")
        secondRow.append(prot.reference)
    if choix12.get() == 1:
        initColumn += 10
        firstRow.append("CC")
        secondRow.append(prot.CC)
    if choix13.get() == 1:
        initColumn += 10
        firstRow.append("DR")
        secondRow.append(prot.DR)
    if choix14.get() == 1:
        initColumn += 10
        firstRow.append("PE")
        secondRow.append(prot.PE)
    if choix15.get() == 1:
        initColumn += 10
        firstRow.append("KW")
        secondRow.append(prot.KW)
    if choix16.get() == 1:
        initColumn += 10
        firstRow.append("FT")
        secondRow.append(prot.FT)
    if choix17.get() == 1:
        initColumn += 10
        firstRow.append("SQ")
        secondRow.append(prot.SQ)

    save_tab =  tkinter.filedialog.asksaveasfile(mode ='a+', initialdir = "/",title = "Enregistrer le fichier FASTA",filetypes = (("*.tabulate","*.tab"),("Excel",".csv")))
    table = [firstRow, secondRow]

    save_tab.write(tabulate(table))
    save_tab.close()
    Label(fenetre,text=">>> Un fichier tabulé a été enregistré dans votre répertoire courant et contient les informations demandées", bg="peach puff").place(y=680,x=30)



############################ Les boutons et checkbuttons #############################################@

button_go = Button(fenetre, text="GO", width=20, command=go, background="peach puff")
button_go.place(y=460, x=600)



# Création de Bouton
checkbutton1 = Checkbutton(fenetre, text="Récupérer le fichier Uniprot", width=30, variable=check1, anchor="w", background="peach puff").place(
    y=100, x=550)
checkbutton2 = Checkbutton(fenetre, text="Récupérer le fichier Fasta", width=30, variable=check2, anchor="w", background="peach puff").place(
    y=140, x=550)
checkbutton3 = Checkbutton(fenetre, text="Obtenir l'hydrophobicité des AA", width=30, variable=check3,
                           anchor="w", background="peach puff").place(y=180, x=550)
checkbutton4 = Checkbutton(fenetre, text="Obtenir l'occurence des AA", width=30, variable=check4, anchor="w", background="peach puff").place(
    y=220, x=550)
checkbutton5 = Checkbutton(fenetre, text="Obtenir taille de la protéine", width=30, variable=check5, anchor="w", background="peach puff").place(
    y=260, x=550)
checkbutton6 = Checkbutton(fenetre, text="Obtenir le poids moléculaire", width=30, variable=check6, anchor="w", background="peach puff").place(
    y=300, x=550)
checkbutton7 = Checkbutton(fenetre, text="Plus d'infos sur la fiche Uniprot", width=30, variable=check7,
                           anchor="w", background="peach puff").place(y=340, x=550)
checkbutton8 = Checkbutton(fenetre, text="Tri", width=30, variable=check8, anchor="w", background="peach puff").place(
    y=380, x=550)

checkbutton9 = Checkbutton(fenetre, text="filtrer", width=30, variable=check9, anchor="w", background="peach puff").place(
    y=420, x=550)




def reset():
    ''' cette fonction permet à l'utilisaeur de fermer la fenetre et de réouvrir une nouvelle en appuyant sur le bouton clear'''
    fenetre.destroy()
    #ce try-except va d'adapter à la version de python installée sur l'ordinateur
    try:
        os.system('python main.py')
    except:
        os.system('python3 main.py') 
    
    

reset = Button(fenetre,text="clear",command= reset)
reset.place(y=57, x=500)

################# Menubar ##############################
def alert():
    A_propos=Tk()
    A_propos.title("BIENVENUE CHEZ L'ÉQUIPE DE L3-BIM")
    A_propos.geometry("800x100")
    global label7
    label7=Label(A_propos,text="Ce programme est le résultat d'un travail laborieux d'étudiants de 3ème année de Licence à l'université de Nice côte-d'azur", background="peach puff").grid(row=30, column=10)

def doc():
    showinfo("Documentation","Toutes les informations sur le fonctionnement du programme sont disponible dans un fichier README fourni avec le script, n'hésitez pas à le lire")

    
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_separator()
menu1.add_command(label="Ouvrir", command=newfile)
menu1.add_command(label="Quitter", command=Intercepte)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="A propos", command=alert)
menu2.add_command(label="Documentation", command=doc)
menubar.add_cascade(label="Aide", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_separator()
menu3.add_command(label="Alignement global/local", command=align_seq)
menubar.add_cascade(label="Aligner", menu=menu3)
fenetre.config(menu=menubar)






fenetre.mainloop()


