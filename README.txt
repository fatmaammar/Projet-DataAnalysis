# Informations générales

Ce programme a été conçu par trois étudiants en 3ème année de Licence en Biologie, Informatique et mathématiques : AMMAR Fatma , LAGHISSI Hiba et MARIAULT Lee , dans le cadre d'un projet en programmation au semestre 6.


# Dates

Nous avons commencé l'élaboration de cet outil mi-février 2020 et on l'a terminé le 02/05/2020. 

# Installation

Le bon fonctionnement du script nécessite l'utilisation de PYTHON et le téléchargement des modules suivants avec `pip` ou `pip3`:

- argparse : ```pip install argparse ```
- Biopython : ```pip install Biopython```
- Collections : ```pip install collections-extended```
- csv : ```pip install python-csv```
- itertools : ```fourni avec python```
- matplotlib : ```python -m pip install -U matplotlib```
- numpy :  ```pip install numpy```
- os : ```fourni avec python```
- requests : ```piping install requests``
- sys : ```fourni avec python```
- tabulate : ```pip install requests```
- tkinter (pour python3) ou Tkinter(pour python2) : ```sudo apt-get install python3-tk```
- urlib.request : ```fourni avec python```

## Langage utilisé

PYTHON

## Déploiement

Sur le shell du terminal, le programme s'exécute avec la commande : python3 main.py (ou python main.py)
Vérifiez que le main.py et function.py (le script d'où main importe ses fonctions) se trouvent dans le même répertoire courant ainsi que l’image UCA.png et le fichier BLOSUM62.txt à partir duquel l’alignement sera fait.

Si vous ne disposez pas de tous les modules, le programme tournera quand même bien que certaines fonctionnalités ne marchent pas 


# De quoi s'agit-il

C'est une interface graphique réalisée avec tkinter. Elle propose de traiter des protéines à partir de leurs numéros d’accession pour en soutirer plusieurs informations qui peuvent intéresser l'utilisateur comme la taille, la composition, le poids moléculaire, l'hydrophobicité, le tri/filtre, la récupération de fiche Uniprot et Fasta et même l'alignement 2 à 2 global/local.

# Utilisation


-Une fois le programme lancé, vous pourrez utiliser l'interface de 2 façons différentes :
	-> Soit vous saisissez un code d'accession dans le champ de saisie, dans ce cas toutes les informations concernant la protéine seront importées d'internet (vérifiez donc votre connexion avant de commencer).

	-> Soit vous importez un fichier sous format `.fas` et dans ce cas, toutes les informations seront récupérées en local à partir de la séquence disponible dans votre fichier. Seul l'option de récupération de la fiche Uniprot demandera toujours une connexion internet.

	Dans tous les cas, il faut cliquer sur le bouton `GO` pour obtenir les résultats

-  Un bouton `clear` est disponible pour rafraîchir la page et recommencer les recherches dès le début.

- Les fonctions du TRI\Filtre ne fonctionnent qu’avec les fichiers multifasta importés.

- Pour les informations sur la fiche Uniprot, d’autres choix s’affichent quand vous choisissez d’obtenir `plus d’infos sur la fiche Uniprot`. Il faudrait faire vos choix concernant les données qui vous intéressent et cliquer sur `Afficher` pour enregistrer le fichier tabulé.

-Pour l’alignement 2 à 2 : tout d’abord, assurez-vous qu’il a bel et bien le fichier BLOSUM62.txt dans votre répertoire courant. Insérez les deux séquences à aligner.
	—> Étant donné que c’est la programmation dynamique, l’alignement peut prendre un certain temps, surtout si la séquence est longue et encore plus si c’est un alignement local. Ne quittez pas le programme même si ça prend du temps.
	—> Pour l’alignement local, l’implémentation préfère les matches/mismatches aux créations de gap et quand ce dernier est créé la délation est privilégiée par rapport aux insertions 

- Parfois les fenêtres générées par les boutons s’affichent derrière la fenêtre principale. Si rien ne s’affiche vérifiez les fenêtres en arrière-plan
   

# Sortie

L'importation de fichiers est possible mais uniquement sous format ".fas", et plusieurs fichiers peuvent être générés selon vos besoins:
- fiches Uniprot : sous format ".txt"
- fichier fasta : sous format ".fas"
- hydrophobicité_moyenne : sous format ".txt"
- Occurence des acides aminées : sous format ".txt"
- Sélection d'informations à partir d'Uniprot : sous format tabulé .csv\.tab
- Tri/Filtre : Sous format ".txt"

Des graphiques pour mieux représenter les résultats peuvent aussi être créés et enregistrés :
- Graphique d'occurence
- Graphique d'hydrophobicité



## Enregistrement des résultats

Des possibilités d'enregistrement des résultats sont proposés. Il suffit de cliquer sur les boutons correspondants

# Fonctions:
Récupérer le fichier Uniprot —> Recherche la fiche UNIPROT sur internet (nécessite une connexion)

Récupérer le fichier faste —> Recherche la fiche FASTA 

Obtenir l’hydrophobicité —> Il faut télécharger le fichier d’hydrophobicité pour pouvoir afficher le graphique

Obtenir la taille de la protéine —> renvoie la taille de la protéine. On n’a pas mis de proposition d’enregistrement car elle est déjà dans le fichier tabulé

Obtenir le poids moléculaire —> Renvoie la taille moléculaire en se basant sur un dictionnaire intégré dans le code on ne propose pas de possibilité d’enregistrer le résultat pour les mêmes raisons cités ci-dessus.

Plus d’infos sur la fiche Uniprot —> Vous permet d’enregistrer sur un fichier tabulé, les lignes qui vous intéressent dans la fiche Uniprot

Tri —> Vous permet de trier vos séquences en fonction de :
		- ID : Identification, par ordre alphabétique
		- GN : Gene Name, par ordre alphabétique
		- OS : Organism Species, par ordre alphabétique
		- tri croissant en fonction de la taille

Filtre —> Vous permet de filtrer vos séquences en fonction de :
		- OX : Organism taxonomy cross-reference (supérieur à/ inférieur à un chiffre de votre choix)
		- PE : Protein Existence (supérieur à/ inférieur à un chiffre de votre choix)


# Idées 
Notre équipe n'a pas encore tout donné. Effectivement, nous avons plus d'idées qui peuvent être mises en place pour d'éventuelles mises à jour. Par exemple:

 - Donner la possibilité à l'utilisateur d'envoyer les résultats par mail à lui-même ou une autre personne
 - Ajouter plus d'options d'alignements : BLAST et multiples

# Référence:

Alignement local : https://github.com/slyyy312/local_alignment
Alignement global : https://github.com/raha1/BLOSUM62


#Licence:

Copyright © 2020 LAGHRISSI Hiba, AMMAR Fatma.
This project is MIT licensed
