import numpy as np
import copy

from functions import *
from objects import *

#quand pioche principale = vide (donc quand il reste 6 cartes) il faut mélanger les cartes dans la défausse et les ajouter à la suite de ces 6 cartes

#quand le joueur choisi l'action piocher carte destination, utiliser pop_up()
#utiliser player.update régulièrement quand c son tour pour mettre à jour nombre de cartes, wagons....


import pygame
from screeninfo import get_monitors

#Dimensionnement zone d'affichage en fonction de l'ecran
screen = get_monitors()
screen_height = screen[0].height -100
screen_width = int(screen_height * 1.789)

#initialisation pygame et de la surface d'affichage
pygame.init()
display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jeux du Train')

#création des villes
ville1 = City("Ville1",(0.1,0.1),0.2)
ville2 = City("Ville2",(0.4,0.3),0.2)
cities = [ville1,ville2]

#création des routes
road1 = Road(cities,np.array([]),"tout")
roads = [road1]

#création des cartes
destination_cards = [Card("destination",destination=("Ville1","Ville2")),
          Card("destination",destination=("Ville1","Ville2")),
          Card("destination",destination=("Ville1","Ville2")),
          Card("destination",destination=("Ville1","Ville2")),
          Card("destination",destination=("Ville1","Ville2")),
          Card("destination",destination=("Ville1","Ville2"))]

wagon_cards = [Card("wagon",color = "rouge"),
                      Card("wagon",color = "jaune"),
                      Card("wagon",color = "blanc"),
                      Card("wagon",color = "tout"),
                      Card("wagon",color = "rouge"),
                      Card("wagon",color = "noir")]

#Création des pioches

destination_pile = Draw_pile(wagon_cards,(0.80,0.43),0.26,'Resources\Destination_pioche.png')

wagon_pile = Draw_pile(wagon_cards,(0.9,0.43),0.26)

#Création des autres boutons intéractifs


wagon_bleu_button = Button((0.23, 0.79),scale = 0.07,center=True,texte = "0")
wagon_rose_button = Button((0.27, 0.79),scale = 0.07,center=True,texte = "0")
wagon_rouge_button = Button((0.31, 0.79),scale = 0.07,center=True,texte = "0")
wagon_noir_button = Button((0.35, 0.79),scale = 0.07,center=True,texte = "0")
wagon_jaune_button = Button((0.39, 0.79),scale = 0.07,center=True,texte = "0")
wagon_orange_button = Button((0.43, 0.79),scale = 0.07,center=True,texte = "0")
wagon_vert_button = Button((0.47, 0.79),scale = 0.07,center=True,texte = "0")
wagon_blanc_button = Button((0.51, 0.79),scale = 0.07,center=True,texte = "0")
wagon_tout_button = Button((0.55, 0.79),scale = 0.07,center=True,texte = "0")


#ordre à respecter pour la liste : "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout"
buttons = [wagon_rose_button,wagon_blanc_button,wagon_bleu_button,wagon_jaune_button,wagon_orange_button,
           wagon_noir_button,wagon_rouge_button,wagon_vert_button,wagon_tout_button]

#Création et affichage du plateau

board = Board(destination_pile,wagon_pile,cities,roads,buttons,display_surface,'Resources\Map.png')

#liste des objets intéractifs (qui nécessitent qu'on vérifie régulièrement si l'utilisateur intéragit avec)

interactive_objects = np.array([destination_pile,
                                wagon_pile,
                                wagon_pile.cards[0],
                                wagon_pile.cards[1],
                                wagon_pile.cards[2],
                                wagon_pile.cards[3],
                                wagon_pile.cards[4]])

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
            print((round(event.pos[0]/screen_width,2),round(event.pos[1]/screen_height,2)))

    pygame.display.update()