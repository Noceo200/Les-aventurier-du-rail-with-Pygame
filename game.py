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

road_1 = Road(("ville1","ville2"),"tout")
wagon_1_1 = Wagon((0.0230, 0.315),"gris",sens = -7,road=road_1,scale = 0.02)
wagon_1_2 = Wagon((0.06, 0.327),"gris",sens = -5,road=road_1,scale = 0.02)
wagon_1_3 = Wagon((0.7269, 0.258),"gris",sens = 0,road=road_1,scale = 0.02)
wagon_1_4 = Wagon((0.6890, 0.2613),"gris",sens = 0,road=road_1,scale = 0.02)
wagon_1_5 = Wagon((0.6495, 0.262),"gris",sens = 9,road=road_1,scale = 0.02)
wagon_1_6 = Wagon((0.6145, 0.277),"gris",sens = 18,road=road_1,scale = 0.02)

road_2 = Road(("ville2","ville3"),"rouge")
wagon_2_1 = Wagon((0.108, 0.328),"gris",sens = 6,road=road_2,scale = 0.019)
wagon_2_2 = Wagon((0.143, 0.327),"gris",sens = 5,road=road_2,scale = 0.019)
wagon_2_3 = Wagon((0.1767, 0.321),"gris",sens = 9,road=road_2,scale = 0.018)

road_3 = Road(("ville3","ville4"),"tout")
wagon_3_1 = Wagon((0.102, 0.36),"gris",sens = 112,road=road_3,scale = 0.02)
wagon_3_2 = Wagon((0.1152, 0.418),"gris",sens = 123,road=road_3,scale = 0.02)
wagon_3_3 = Wagon((0.1385, 0.473),"gris",sens = 131,road=road_3,scale = 0.02)
wagon_3_4 = Wagon((0.1648, 0.522),"gris",sens = 145,road=road_3,scale = 0.02)
wagon_3_5 = Wagon((0.197, 0.56),"gris",sens = 149,road=road_3,scale = 0.02)

road_4 = Road(("ville1","ville2"),"tout")
wagon_4_1 = Wagon((0.2095, 0.335),"gris",sens = 100,road=road_4,scale = 0.02)
wagon_4_2 = Wagon((0.215, 0.398),"gris",sens = 100,road=road_4,scale = 0.02)
wagon_4_3 = Wagon((0.221, 0.459),"gris",sens = 100,road=road_4,scale = 0.02)
wagon_4_4 = Wagon((0.2274, 0.521),"gris",sens = 100,road=road_4,scale = 0.02)

road_5 = Road(("ville1","ville2"),"tout")
wagon_5_1 = Wagon((0.2177, 0.305),"gris",sens = 9,road=road_5,scale = 0.02)
wagon_5_2 = Wagon((0.2513, 0.294),"gris",sens = 10,road=road_5,scale = 0.019)
wagon_5_3 = Wagon((0.2834, 0.285),"gris",sens = 10,road=road_5,scale = 0.019)
wagon_5_4 = Wagon((0.3154, 0.271),"gris",sens = 10,road=road_5,scale = 0.019)

road_6 = Road(("ville1","ville2"),"tout")
wagon_6_1 = Wagon((0.24, 0.596),"gris",sens = -4,road=road_6,scale = 0.02)
wagon_6_2 = Wagon((0.278, 0.593),"gris",sens = 8,road=road_6,scale = 0.02)
wagon_6_3 = Wagon((0.3184, 0.5773),"gris",sens = 9,road=road_6,scale = 0.02)
wagon_6_4 = Wagon((0.3579, 0.5627),"gris",sens = 11,road=road_6,scale = 0.02)

road_7 = Road(("ville1","ville2"),"tout")
wagon_7_1 = Wagon((0.241, 0.54),"gris",sens = 39,road=road_7,scale = 0.02)
wagon_7_2 = Wagon((0.271, 0.505),"gris",sens = 31,road=road_7,scale = 0.02)
wagon_7_3 = Wagon((0.3013, 0.471),"gris",sens = 30,road=road_7,scale = 0.02)
wagon_7_4 = Wagon((0.336, 0.443),"gris",sens = 32,road=road_7,scale = 0.02)

road_8 = Road(("ville1","ville2"),"tout")
wagon_8_1 = Wagon((0.328, 0.281),"gris",sens = 46,road=road_8,scale = 0.02)
wagon_8_2 = Wagon((0.3261, 0.34),"gris",sens = 95,road=road_8,scale = 0.02)
wagon_8_3 = Wagon((0.3348, 0.402),"gris",sens = 145,road=road_8,scale = 0.019)

road_9 = Road(("ville1","ville2"),"tout")
wagon_9_1 = Wagon((0.3682, 0.4423),"gris",sens = 101,road=road_9,scale = 0.02)
wagon_9_2 = Wagon((0.3766, 0.5035),"gris",sens = 110,road=road_9,scale = 0.019)

road_10 = Road(("ville1","ville2"),"tout")
wagon_10_1 = Wagon((0.358, 0.2445),"gris",sens = 14,road=road_10,scale = 0.02)
wagon_10_2 = Wagon((0.392, 0.225),"gris",sens = 14,road=road_10,scale = 0.02)

road_11 = Road(("ville1","ville2"),"tout")
wagon_11_1 = Wagon((0.4243, 0.242),"gris",sens = 100,road=road_11,scale = 0.02)
wagon_11_2 = Wagon((0.42, 0.3024),"gris",sens = 73,road=road_11,scale = 0.02)
wagon_11_3 = Wagon((0.403, 0.358),"gris",sens = 51,road=road_11,scale = 0.019)
wagon_11_4 = Wagon((0.3751, 0.4035),"gris",sens = 23,road=road_11,scale = 0.019)

road_12 = Road(("ville1","ville2"),"tout")
wagon_12_1 = Wagon((0.405, 0.5507),"gris",sens = -4,road=road_12,scale = 0.02)
wagon_12_2 = Wagon((0.441, 0.5573),"gris",sens = -4,road=road_12,scale = 0.02)
wagon_12_3 = Wagon((0.4772, 0.5627),"gris",sens = -3,road=road_12,scale = 0.02)
wagon_12_4 = Wagon((0.5118, 0.5693),"gris",sens = -3,road=road_12,scale = 0.02)
wagon_12_5 = Wagon((0.549, 0.5733),"gris",sens = -5,road=road_12,scale = 0.02)
wagon_12_6 = Wagon((0.586, 0.58),"gris",sens = -4,road=road_12,scale = 0.02)
wagon_12_7 = Wagon((0.6249, 0.582),"gris",sens = -4,road=road_12,scale = 0.02)
wagon_12_8 = Wagon((0.66, 0.582),"gris",sens = 5,road=road_12,scale = 0.02)

road_13 = Road(("ville1","ville2"),"tout")
wagon_13_1 = Wagon((0.3982, 0.502),"gris",sens = 44,road=road_13,scale = 0.02)
wagon_13_2 = Wagon((0.4222, 0.469),"gris",sens = 25,road=road_13,scale = 0.02)
wagon_13_3 = Wagon((0.4552, 0.461),"gris",sens = 5,road=road_13,scale = 0.02)
wagon_13_4 = Wagon((0.4895, 0.466),"gris",sens = -14,road=road_13,scale = 0.02)
wagon_13_5 = Wagon((0.5235, 0.484),"gris",sens = -6,road=road_13,scale = 0.02)
wagon_13_6 = Wagon((0.557, 0.459),"gris",sens = 30,road=road_13,scale = 0.02)

road_14 = Road(("ville1","ville2"),"tout")
wagon_14_1 = Wagon((0.38, 0.4387),"gris",sens = -7,road=road_14,scale = 0.02)
wagon_14_2 = Wagon((0.416, 0.4427),"gris",sens = 0,road=road_14,scale = 0.02)
wagon_14_3 = Wagon((0.4519, 0.415),"gris",sens = 23,road=road_14,scale = 0.02)
wagon_14_4 = Wagon((0.484, 0.369),"gris",sens = 44,road=road_14,scale = 0.02)

road_15 = Road(("ville1","ville2"),"tout")
wagon_15_1 = Wagon((0.4333, 0.2300),"gris",sens = -39,road=road_15,scale = 0.02)
wagon_15_2 = Wagon((0.458, 0.2725),"gris",sens = -39,road=road_15,scale = 0.02)
wagon_15_3 = Wagon((0.485, 0.314),"gris",sens = -39,road=road_15,scale = 0.02)

road_16 = Road(("ville1","ville2"),"tout")
wagon_16_1 = Wagon((0.4392, 0.204),"gris",sens = 10,road=road_16,scale = 0.02)
wagon_16_2 = Wagon((0.4752, 0.204),"gris",sens = 0,road=road_16,scale = 0.02)
wagon_16_3 = Wagon((0.5123, 0.2053),"gris",sens = -12,road=road_16,scale = 0.02)
wagon_16_4 = Wagon((0.549, 0.22),"gris",sens = -35,road=road_16,scale = 0.02)
wagon_16_5 = Wagon((0.579, 0.2627),"gris",sens = -37,road=road_16,scale = 0.02)

road_17 = Road(("ville1","ville2"),"tout")
wagon_17_1 = Wagon((0.5198, 0.372),"gris",sens = -49,road=road_17,scale = 0.02)
wagon_17_2 = Wagon((0.5488, 0.4173),"gris",sens = -27,road=road_17,scale = 0.02)

road_18 = Road(("ville1","ville2"),"tout")
wagon_18_1 = Wagon((0.5943, 0.4653),"gris",sens = -35,road=road_18,scale = 0.02)
wagon_18_2 = Wagon((0.6271, 0.505),"gris",sens = -28,road=road_18,scale = 0.02)
wagon_18_3 = Wagon((0.6611, 0.536),"gris",sens = -32,road=road_18,scale = 0.02)

road_19 = Road(("ville1","ville2"),"tout")
wagon_19_1 = Wagon((0.581, 0.3884),"gris",sens = -96,road=road_19,scale = 0.02)
wagon_19_2 = Wagon((0.5876, 0.333),"gris",sens = -114,road=road_19,scale = 0.02)

road_20 = Road(("ville1","ville2"),"tout")
wagon_20_1 = Wagon((0.6189, 0.3165),"gris",sens = 0,road=road_20,scale = 0.02)
wagon_20_2 = Wagon((0.6547, 0.318),"gris",sens = -22,road=road_20,scale = 0.02)
wagon_20_3 = Wagon((0.689, 0.349),"gris",sens = -34,road=road_20,scale = 0.02)
wagon_20_4 = Wagon((0.7178, 0.399),"gris",sens = 109,road=road_20,scale = 0.02)
wagon_20_5 = Wagon((0.724, 0.463),"gris",sens = -100,road=road_20,scale = 0.02)
wagon_20_6 = Wagon((0.7031, 0.5256),"gris",sens = 53,road=road_20,scale = 0.02)

roads = [road_1,road_2,road_3,road_4,road_5,road_6,road_7,road_8,road_9,road_10,road_11,road_12,road_13,road_14,road_15,road_16,road_17,road_18,road_19,road_20]

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
                                wagon_1_1, wagon_1_2, wagon_1_3, wagon_1_4, wagon_1_5, wagon_1_6, wagon_2_1, wagon_2_2,wagon_2_3,
                                wagon_3_1, wagon_3_2, wagon_3_3, wagon_3_4, wagon_3_5, wagon_4_1, wagon_4_2, wagon_4_3,wagon_4_4,
                                wagon_5_1, wagon_5_2, wagon_5_3, wagon_5_4, wagon_6_1, wagon_6_2, wagon_6_3, wagon_6_4, wagon_7_1, wagon_7_2,
                                wagon_7_3, wagon_7_4, wagon_8_1, wagon_8_2, wagon_8_3, wagon_9_1, wagon_9_2, wagon_10_1,wagon_10_2, wagon_11_1,
                                wagon_11_2, wagon_11_3, wagon_11_4, wagon_12_1, wagon_12_2, wagon_12_3, wagon_12_4,wagon_12_5, wagon_12_6, wagon_12_7,
                                wagon_12_8, wagon_13_1, wagon_13_2, wagon_13_3, wagon_13_4, wagon_13_5, wagon_13_6,wagon_14_1, wagon_14_2, wagon_14_3, wagon_14_4,
                                wagon_15_1, wagon_15_2, wagon_15_3, wagon_16_1, wagon_16_2, wagon_16_3, wagon_16_4,wagon_16_5, wagon_17_1, wagon_17_2,
                                wagon_18_2, wagon_18_3, wagon_19_1, wagon_19_2, wagon_20_1, wagon_20_2, wagon_20_3,wagon_20_4, wagon_20_5, wagon_20_6,
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