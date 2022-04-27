import numpy as np
import copy

from functions import *
from objects import *

#quand pioche principale = vide (donc quand il reste 6 cartes) il faut mélanger les cartes dans la défausse et les ajouter à la suite de ces 6 cartes
#Empecher le joueur de piocher plus de 8 cartes destinations pour eviter problème affichage

import pygame
from screeninfo import get_monitors

#Dimensionnement zone d'affichage en fonction de l'ecran
screen = get_monitors()
screen_height = screen[0].height -150
screen_width = int(screen_height * 1.789)

#initialisation pygame et de la surface d'affichage
pygame.init()
display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jeux du Train')

#création des routes et leur wagons

"""
    - Créer route puis tout ses wagons à la suite
    - ajouter chaque wagons dans la liste "interactive_objects" tout en bas
    - ajouter chaque routes dans la liste roads juste en bas
    
    tu peut ajouter "center = True" comme paramètre pour les wagons si tu préfère qu'il se place au centre de ta position plutot qu'avec leur coin supérieur gauche
"""

road_1 = Road(("ville1","ville2"),"tout")
wagon_1_1 = Wagon((0.06,0.15),"gris",sens = 0,road=road_1,scale = 0.02)
wagon_1_2 = Wagon((0.1,0.15),"gris",sens = 0,road=road_1,scale = 0.02)

road_2 = Road(("ville2","ville3"),"rouge")
wagon_2_1 = Wagon((0.1,0.3),"gris",sens = 0,road=road_2,scale = 0.02)
wagon_2_2 = Wagon((0.14, 0.28),"gris",sens = 25,road=road_2,scale = 0.02)

roads = [road_1,road_2]

#création des cartes
destination_cards = [Card("destination",destination=("Ville1","Ville2"),convert = False),
          Card("destination",destination=("Ville1","Ville2"),convert = False),
          Card("destination",destination=("Ville1","Ville2"),convert = False),
          Card("destination",destination=("Ville1","Ville2"),convert = False),
          Card("destination",destination=("Ville1","Ville2"),convert = False),
          Card("destination",destination=("Ville1","Ville2"),convert = False),
          Card("destination", destination=("Ville1", "Ville2"),convert = False),
          Card("destination", destination=("Ville1", "Ville2"),convert = False),
          Card("destination", destination=("Ville1", "Ville2"),convert = False)]

wagon_cards = [Card("wagon",color = "rouge"),
                      Card("wagon",color = "jaune"),
                      Card("wagon",color = "blanc"),
                      Card("wagon",color = "tout"),
                      Card("wagon",color = "rouge"),
                      Card("wagon",color = "noir")]

#Création des pioches

destination_pile = Draw_pile(wagon_cards,(0.865, 0.486),0.162,'Resources\Destination_pioche.png')

wagon_pile = Draw_pile(wagon_cards,(0.783, 0.405),0.24)

#Création du joueur

player = Player("No_name","",wagon_pile,destination_cards[0:9]) #utiliser pop up pour proposer de choisir cartes

#Création des autres boutons intéractifs

#boutons qui affichent le nombre de carte wagons de chaque couleur que possède l'utilisateur
wagon_rose_button = Button((0.23, 0.79),scale = 0.07,center=True,texte = "0")
wagon_blanc_button = Button((0.27, 0.79),scale = 0.07,center=True,texte = "0")
wagon_bleu_button = Button((0.31, 0.79),scale = 0.07,center=True,texte = "0")
wagon_jaune_button = Button((0.35, 0.79),scale = 0.07,center=True,texte = "0")
wagon_orange_button = Button((0.39, 0.79),scale = 0.07,center=True,texte = "0")
wagon_noir_button = Button((0.43, 0.79),scale = 0.07,center=True,texte = "0")
wagon_rouge_button = Button((0.47, 0.79),scale = 0.07,center=True,texte = "0")
wagon_vert_button = Button((0.51, 0.79),scale = 0.07,center=True,texte = "0")
wagon_tout_button = Button((0.55, 0.79),scale = 0.07,center=True,texte = "0")

#bouton qui affichent des informations lors du passage de la souris dessus
info1_button = Button((0.03, 0.92),scale = 0.06,center=True,image = 'Resources\info_button.png',image2='Resources\info_pioche.png')
info2_button = Button((0.19, 0.75),scale = 0.06,center=True,image = 'Resources\info_button.png',image2='Resources\info_pioche.png')
info3_button = Button((0.78, 0.75),scale = 0.06,center=True,image = 'Resources\info_button.png',image2='Resources\info_pioche.png')
info4_button = Button((0.97, 0.92),scale = 0.06,center=True,image = 'Resources\info_button.png',image2='Resources\info_pioche.png')
info5_button = Button((0.97, 0.04),scale = 0.06,center=True,image = 'Resources\info_button.png',image2='Resources\info_pioche.png')
info6_button = Button((0.72, 0.04),scale = 0.06,center=True,image = 'Resources\info_button.png',image2='Resources\info_pioche.png')

#bouton qui affichent les nombres de crédits et de wagons restant de l'utilisateur et de l'IA
credit_txt = Button((0.91, 0.91),scale = 0.07,center=True,texte = "2")
wagon_txt = Button((0.09, 0.91),scale = 0.07,center=True,texte = "45")
credit_txt_IA = Button((0.63, 0.045),scale = 0.07,center=True,texte = "0")
wagon_txt_IA = Button((0.40, 0.045),scale = 0.07,center=True,texte = "45")

#bouton qui affiche texte instructions à l'utilisateur

instruction_button = Button((0.5, 0.95),center = True,scale = 0.17, image = 'Resources\instructions.png',texte = 'texte de malade')

#bouton qui affiche les carte destination du joueur

show_destination_button = Button((0.6687, 0.7452),scale = 0.16,image = "Resources\destination_button.png",convert=True,player = player)

#ordre à respecter pour la liste : "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout"...
buttons = [wagon_rose_button,wagon_blanc_button,wagon_bleu_button,wagon_jaune_button,wagon_orange_button,
           wagon_noir_button,wagon_rouge_button,wagon_vert_button,wagon_tout_button,credit_txt,wagon_txt,
           credit_txt_IA,wagon_txt_IA,show_destination_button,instruction_button,info1_button,info2_button,info3_button,
           info4_button,info5_button,info6_button]

#Création et affichage du plateau

board = Board(destination_pile,wagon_pile,roads,buttons,display_surface,'Resources\Map.png')

#liste des objets intéractifs (qui nécessitent qu'on vérifie régulièrement si l'utilisateur intéragit avec)

interactive_objects = np.array([destination_pile,
                                wagon_pile,
                                info1_button,
                                info2_button,
                                info3_button,
                                info4_button,
                                info5_button,
                                info6_button,
                                show_destination_button,
                                wagon_1_1,wagon_1_2,wagon_2_1,wagon_2_2,
                                wagon_pile.cards[0],wagon_pile.cards[1],wagon_pile.cards[2],wagon_pile.cards[3],wagon_pile.cards[4]]) #les derniers éléments doivent etre les cartes de dessus de pioche

show_visible_wagon(wagon_pile,interactive_objects)#première mise à jour des cartes wagons visibles

while True :

    Update_Objects("player", board) #mise à jour des variables des objets sur le plateau
    board.represent() #actualisation graphique du plateau

    for event in pygame.event.get(): #vérification des actions du joueur
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEMOTION:
            check_all_event(event,interactive_objects)
        if event.type == pygame.MOUSEBUTTONUP :
            check_all_event(event,interactive_objects)
            print((round(event.pos[0]/screen_width,4),round(event.pos[1]/screen_height,4)))

    pygame.display.update()