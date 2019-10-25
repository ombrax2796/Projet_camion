#---------------------------------------------------------------------LES LIBRAIRIES
from tkinter import *
import re
import requests
from bs4 import BeautifulSoup
from time import *

#---------------------------------------------------------------------LES VARIABLES
tpstrajets =0
tpspause =0
vitesse = 0
nombrepause = 0
distance=0
distancebase=0

#---------------------------------------------------------------------BEAUTIFULSOUP
def trouvedist():
    global distance,distancebase
    nomville1=ville1.get()
    nomville2=ville2.get()
    liens=f"https://www.bonnesroutes.com/distance/?from={nomville1}&to={nomville2}"
    site=requests.get(liens)#On vas demander d'extraire les données du de la page
    page= site.content
    soup= BeautifulSoup(page, "html.parser")#-----------------------------analyse les données de la page

    #---------------------------------------------------------------------MANIPULATION DES DONNEES
    lignes= soup.find_all(class_="value")#--------------------------------recherche "class=value" (ou est stocké la distance, mais je vais avoir plusieurs 'class=value')
    laligne=lignes[2]#----------------------------------------------------je prend la 3eme "valeur" du tableau car elle correspond au bon 'class=value' soit la distance
    distancediv=[i for i in laligne]#-------------------------------------je ne tire que la distance (de "<div class="value">773</div>" je tire "['773']")
    distancetotal=distancediv[0]#-----------------------------------------je sort la distance du tableau pour le manipuler facilement
    print(laligne)
    print(distancediv)
    print(distancetotal)
    distance = float(distancetotal)#--------------------------------------convertie la valeur distancetotal (actuellement en string) en float
    distancebase = distance

#---------------------------------------------------------------------LES FONCTIONS
def acceleration():
    global vitesse, tpstrajets, distance
    while vitesse < 90:
        vitesse += 10
        tpstrajets += 1
    distance -=7.5#--------------------------------------------------distance parcouru lors de l'acceleration
        
def frein():
    global vitesse, tpstrajets, distance
    while vitesse > 0:
        vitesse -= 10
        tpstrajets += 1
    distance -=7.5 #-------------------------------------------------distance parcouru lors du freinage 

def pause():
    global tpspause
    frein()
    tpspause += 15
    acceleration()

def parcours():
    global vitesse, tpstrajets, distance,tpspause,nombrepause
    trouvedist()
    acceleration()
    while distance > 0:
        tpstrajets +=1
        distance -=1.5#-------------------------------------------------en1minute a 90km/h on parcours 1.5km/minute
        if tpstrajets%120==0:
            pause()
            nombrepause += 1
        if distance<=7.5:
            frein()
    tpstrajets += tpspause
    tpstrajets=strftime('%H''h''%M', gmtime(tpstrajets*60))



#-------------------------------------------------------------------DECORATION

def resultat():
    parcours()
    Mafenetre = Toplevel()
    can=Canvas(Mafenetre,width=900,height=300) 
    can.pack()

    #-------------------------------------------------------------------Tableau

    can.create_rectangle(0,150,150,300)
    can.create_rectangle(150,150,300,300)
    can.create_rectangle(300,150,450,300)
    can.create_rectangle(450,150,600,300)
    can.create_rectangle(600,150,750,300)
    can.create_rectangle(750,150,900,300)
    temps = can.create_text((75, 225), text=("temps trajets :",tpstrajets))
    tempspause = can.create_text((225, 225), text=("temps de pause:", tpspause))
    nbpause = can.create_text((375, 225), text=("nombre de pause:",nombrepause))
    dist = can.create_text((525, 225), text=("distance:",distancebase))
    villedep = can.create_text((675, 225), text=("ville départ:",ville1.get()))
    villearr = can.create_text((825, 225), text=("ville arrivé:",ville2.get()))
    Mafenetre.update()
    Mafenetre.mainloop()

#-------------------------------------------------------------------Création de la fenêtre principale(question des villes)

fenetreparametre=Tk()
fenetreparametre.title('calcule temps trajet')
canv=Canvas(fenetreparametre,width=40,height=40)
textv1=Label(fenetreparametre, text="première ville")
textv2=Label(fenetreparametre, text="deuxieme ville")
ville1 = Entry(fenetreparametre)
ville2 = Entry(fenetreparametre)
btn_calcul=Button(fenetreparametre,text='Executer',command=resultat,width=20)
canv.grid(row=1,column=4)
textv1.grid(row=0, column=1)
textv2.grid(row=0, column=3)
ville1.grid(row=0, column=2)
ville2.grid(row=0, column=4)
btn_calcul.grid(row=1,column=2)
fenetreparametre.update()
fenetreparametre.mainloop()








