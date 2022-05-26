import sys
import time
import numpy as np
from objects import *

#quand pioche principale = vide (donc quand il reste 6 cartes) il faut mélanger les cartes dans la défausse et les ajouter à la suite de ces 6 cartes
#Empecher le joueur de piocher plus de 8 cartes destinations pour eviter problème affichage
#ajout 2 type IA

import pygame
from screeninfo import get_monitors

from playsound import playsound

#initialisation des sons

back_ground_music = "Resources/Songs/background_theme.mp3"
playsound(back_ground_music,block=False) #lancement de la music de fond, voir si plus simple avec autre librairy pour loop et intensité son

sound_end = 'Resources/Songs/TicketCompletedVictory.mp3'
sound_IA_turn = 'Resources/Songs/Intro_J_Connected2.mp3'

#Dimensionnement zone d'affichage en fonction de l'ecran
screen = get_monitors()
screen_height = screen[0].height -150
screen_width = int(screen_height * 1.789)

#initialisation pygame et de la surface d'affichage
pygame.init()
display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jeux du Train')

#Création du joueur

player = Player("No_name")

#création des routes et leur wagons

road_1 = Road(("ville0","ville1"),"noir",player)
wagon_1_1 = Wagon((0.0230, 0.315) ,sens = -7,road=road_1,scale = 0.016)
wagon_1_2 = Wagon((0.06, 0.327) ,sens = -5,road=road_1,scale = 0.016)
wagon_1_3 = Wagon((0.7269, 0.258) ,sens = 0,road=road_1,scale = 0.016)
wagon_1_4 = Wagon((0.6890, 0.2613) ,sens = 0,road=road_1,scale = 0.016)
wagon_1_5 = Wagon((0.6495, 0.262) ,sens = 9,road=road_1,scale = 0.016)
wagon_1_6 = Wagon((0.6145, 0.277) ,sens = 18,road=road_1,scale = 0.016)

road_2 = Road(("ville2","ville3"),"vert",player)
wagon_2_1 = Wagon((0.108, 0.328),sens = 6,road=road_2,scale = 0.016)
wagon_2_2 = Wagon((0.143, 0.327),sens = 5,road=road_2,scale = 0.016)
wagon_2_3 = Wagon((0.1767, 0.321),sens = 9,road=road_2,scale = 0.016)

road_3 = Road(("ville3","ville4"),"rouge",player)
wagon_3_1 = Wagon((0.102, 0.36) ,sens = 112,road=road_3,scale = 0.016)
wagon_3_2 = Wagon((0.1152, 0.418) ,sens = 123,road=road_3,scale = 0.016)
wagon_3_3 = Wagon((0.1385, 0.473) ,sens = 131,road=road_3,scale = 0.016)
wagon_3_4 = Wagon((0.1648, 0.522) ,sens = 145,road=road_3,scale = 0.016)
wagon_3_5 = Wagon((0.197, 0.56) ,sens = 149,road=road_3,scale = 0.016)

road_4 = Road(("ville0","ville1"),"tout",player)
wagon_4_1 = Wagon((0.2095, 0.335) ,sens = 100,road=road_4,scale = 0.016)
wagon_4_2 = Wagon((0.215, 0.398) ,sens = 100,road=road_4,scale = 0.016)
wagon_4_3 = Wagon((0.221, 0.459) ,sens = 100,road=road_4,scale = 0.016)
wagon_4_4 = Wagon((0.2274, 0.521) ,sens = 100,road=road_4,scale = 0.016)

road_5 = Road(("ville0","ville1"),"jaune",player)
wagon_5_1 = Wagon((0.2177, 0.305) ,sens = 9,road=road_5,scale = 0.016)
wagon_5_2 = Wagon((0.2513, 0.294) ,sens = 10,road=road_5,scale = 0.016)
wagon_5_3 = Wagon((0.2834, 0.285) ,sens = 10,road=road_5,scale = 0.016)
wagon_5_4 = Wagon((0.3154, 0.271) ,sens = 10,road=road_5,scale = 0.016)

road_6 = Road(("ville0","ville1"),"rose",player)
wagon_6_1 = Wagon((0.24, 0.596) ,sens = -4,road=road_6,scale = 0.016)
wagon_6_2 = Wagon((0.278, 0.593) ,sens = 8,road=road_6,scale = 0.016)
wagon_6_3 = Wagon((0.3184, 0.5773) ,sens = 9,road=road_6,scale = 0.016)
wagon_6_4 = Wagon((0.3579, 0.5627) ,sens = 11,road=road_6,scale = 0.016)

road_7 = Road(("ville0","ville1"),"tout",player)
wagon_7_1 = Wagon((0.241, 0.54) ,sens = 39,road=road_7,scale = 0.016)
wagon_7_2 = Wagon((0.271, 0.505) ,sens = 31,road=road_7,scale = 0.016)
wagon_7_3 = Wagon((0.3013, 0.471) ,sens = 30,road=road_7,scale = 0.016)
wagon_7_4 = Wagon((0.336, 0.443) ,sens = 32,road=road_7,scale = 0.016)

road_8 = Road(("ville0","ville1"),"orange",player)
wagon_8_1 = Wagon((0.328, 0.281) ,sens = 46,road=road_8,scale = 0.016)
wagon_8_2 = Wagon((0.3261, 0.34) ,sens = 95,road=road_8,scale = 0.016)
wagon_8_3 = Wagon((0.3348, 0.402) ,sens = 145,road=road_8,scale = 0.016)

road_9 = Road(("ville0","ville1"),"jaune",player)
wagon_9_1 = Wagon((0.3682, 0.4423) ,sens = 101,road=road_9,scale = 0.016)
wagon_9_2 = Wagon((0.3766, 0.5035) ,sens = 110,road=road_9,scale = 0.016)

road_10 = Road(("ville0","ville1"),"tout",player)
wagon_10_1 = Wagon((0.358, 0.2445) ,sens = 14,road=road_10,scale = 0.016)
wagon_10_2 = Wagon((0.392, 0.225) ,sens = 14,road=road_10,scale = 0.016)

road_11 = Road(("ville0","ville1"),"rose",player)
wagon_11_1 = Wagon((0.4243, 0.242) ,sens = 100,road=road_11,scale = 0.016)
wagon_11_2 = Wagon((0.42, 0.3024) ,sens = 73,road=road_11,scale = 0.016)
wagon_11_3 = Wagon((0.403, 0.358) ,sens = 51,road=road_11,scale = 0.016)
wagon_11_4 = Wagon((0.3751, 0.4035) ,sens = 23,road=road_11,scale = 0.016)

road_12 = Road(("ville0","ville1"),"noir",player)
wagon_12_1 = Wagon((0.405, 0.5507) ,sens = -4,road=road_12,scale = 0.016)
wagon_12_2 = Wagon((0.441, 0.5573) ,sens = -4,road=road_12,scale = 0.016)
wagon_12_3 = Wagon((0.4772, 0.5627) ,sens = -3,road=road_12,scale = 0.016)
wagon_12_4 = Wagon((0.5118, 0.5693) ,sens = -3,road=road_12,scale = 0.016)
wagon_12_5 = Wagon((0.549, 0.5733) ,sens = -5,road=road_12,scale = 0.016)
wagon_12_6 = Wagon((0.586, 0.58) ,sens = -4,road=road_12,scale = 0.016)
wagon_12_7 = Wagon((0.6249, 0.582) ,sens = -4,road=road_12,scale = 0.016)
wagon_12_8 = Wagon((0.66, 0.582) ,sens = 5,road=road_12,scale = 0.016)

road_13 = Road(("ville0","ville1"),"blanc",player)
wagon_13_1 = Wagon((0.3982, 0.502) ,sens = 44,road=road_13,scale = 0.016)
wagon_13_2 = Wagon((0.4222, 0.469) ,sens = 25,road=road_13,scale = 0.016)
wagon_13_3 = Wagon((0.4552, 0.461) ,sens = 5,road=road_13,scale = 0.016)
wagon_13_4 = Wagon((0.4895, 0.466) ,sens = -14,road=road_13,scale = 0.016)
wagon_13_5 = Wagon((0.5235, 0.484) ,sens = -6,road=road_13,scale = 0.016)
wagon_13_6 = Wagon((0.557, 0.459) ,sens = 30,road=road_13,scale = 0.016)

road_14 = Road(("ville0","ville1"),"tout",player)
wagon_14_1 = Wagon((0.38, 0.4387) ,sens = -7,road=road_14,scale = 0.016)
wagon_14_2 = Wagon((0.416, 0.4427) ,sens = 0,road=road_14,scale = 0.016)
wagon_14_3 = Wagon((0.4519, 0.415) ,sens = 23,road=road_14,scale = 0.016)
wagon_14_4 = Wagon((0.484, 0.369) ,sens = 44,road=road_14,scale = 0.016)

road_15 = Road(("ville0","ville1"),"tout",player)
wagon_15_1 = Wagon((0.4333, 0.2300) ,sens = -39,road=road_15,scale = 0.016)
wagon_15_2 = Wagon((0.458, 0.2725) ,sens = -39,road=road_15,scale = 0.016)
wagon_15_3 = Wagon((0.485, 0.314) ,sens = -39,road=road_15,scale = 0.016)

road_16 = Road(("ville0","ville1"),"bleu",player)
wagon_16_1 = Wagon((0.4392, 0.204) ,sens = 10,road=road_16,scale = 0.016)
wagon_16_2 = Wagon((0.4752, 0.204) ,sens = 0,road=road_16,scale = 0.016)
wagon_16_3 = Wagon((0.5123, 0.2053) ,sens = -12,road=road_16,scale = 0.016)
wagon_16_4 = Wagon((0.549, 0.22) ,sens = -35,road=road_16,scale = 0.016)
wagon_16_5 = Wagon((0.579, 0.2627) ,sens = -37,road=road_16,scale = 0.016)

road_17 = Road(("ville0","ville1"),"vert",player)
wagon_17_1 = Wagon((0.5198, 0.372) ,sens = -49,road=road_17,scale = 0.016)
wagon_17_2 = Wagon((0.5488, 0.4173) ,sens = -27,road=road_17,scale = 0.016)

road_18 = Road(("ville0","ville1"),"tout",player)
wagon_18_1 = Wagon((0.5943, 0.4653) ,sens = -35,road=road_18,scale = 0.016)
wagon_18_2 = Wagon((0.6271, 0.505) ,sens = -28,road=road_18,scale = 0.016)
wagon_18_3 = Wagon((0.6611, 0.536) ,sens = -32,road=road_18,scale = 0.016)

road_19 = Road(("ville0","ville1"),"tout",player)
wagon_19_1 = Wagon((0.581, 0.3884) ,sens = -96,road=road_19,scale = 0.016)
wagon_19_2 = Wagon((0.5876, 0.333) ,sens = -114,road=road_19,scale = 0.016)

road_20 = Road(("ville0","ville1"),"orange",player)
wagon_20_1 = Wagon((0.6189, 0.3165) ,sens = 0,road=road_20,scale = 0.016)
wagon_20_2 = Wagon((0.6547, 0.318) ,sens = -22,road=road_20,scale = 0.016)
wagon_20_3 = Wagon((0.689, 0.349) ,sens = -34,road=road_20,scale = 0.016)
wagon_20_4 = Wagon((0.7178, 0.399) ,sens = 109,road=road_20,scale = 0.016)
wagon_20_5 = Wagon((0.724, 0.463) ,sens = -100,road=road_20,scale = 0.016)
wagon_20_6 = Wagon((0.7031, 0.5256) ,sens = 53,road=road_20,scale = 0.016)

roads = [road_1,road_2,road_3,road_4,road_5,road_6,road_7,road_8,road_9,road_10,road_11,road_12,road_13,road_14,road_15,road_16,road_17,road_18,road_19,road_20]

#création des cartes
destination_cards = [Card("destination",destination=("ville0","ville1")),
          Card("destination",destination=("ville0","ville1")),
          Card("destination",destination=("ville0","ville1")),
          Card("destination",destination=("ville0","ville1")),
          Card("destination",destination=("ville0","ville1")),
          Card("destination",destination=("ville0","ville1")),
          Card("destination", destination=("ville0","ville1")),
          Card("destination", destination=("ville0","ville1")),
          Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1")),
                     Card("destination", destination=("ville0","ville1"))
                     ]

wagon_cards = []

color_list = ["rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout"]

for color in color_list:
    for i in range(12): #12 cartes de chaques couleurs
        wagon_cards.append(Card("wagon", color=color))


#Création des pioches

destination_pile = Draw_pile(destination_cards,player,"destination_pile",(0.865, 0.486),0.162,'Resources\Destination_pioche.png')

wagon_pile = Draw_pile(wagon_cards,player,"wagon_pile",(0.783, 0.405),0.24)

used_cards = []

#mise à jour du joueur

player.wagon_cards = []
player.destination_cards = [] #utiliser pop up pour proposer de choisir cartes
player.used_cards = used_cards

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
wagon_txt_IA = Button((0.40, 0.045),scale = 0.07,center=True,texte = "45")

#bouton qui affiche texte instructions à l'utilisateur

instruction_button = Button((0.5, 0.95),center = True,scale = 0.17, image = 'Resources\instructions.png',texte = 'Bienvenue !')

#bouton qui affiche les carte destination du joueur

show_destination_button = Button((0.6687, 0.7452),scale = 0.16,image = "Resources\destination_button.png",convert=True,player = player)

#ordre à respecter pour la liste : "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout"...
buttons = [wagon_rose_button,wagon_blanc_button,wagon_bleu_button,wagon_jaune_button,wagon_orange_button,
           wagon_noir_button,wagon_rouge_button,wagon_vert_button,wagon_tout_button,credit_txt,wagon_txt,
           wagon_txt_IA,show_destination_button,instruction_button,info1_button,info2_button,info3_button,
           info4_button,info5_button,info6_button]

#Création du plateau

board = Board(destination_pile,wagon_pile,roads,buttons,display_surface,'Resources\Map.png')
player.board = board

#liste des objets intéractifs (qui nécessitent qu'on vérifie régulièrement si l'utilisateur intéragit avec)

interactive_objects = [destination_pile,
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
                                wagon_18_1,wagon_18_2, wagon_18_3, wagon_19_1, wagon_19_2, wagon_20_1, wagon_20_2, wagon_20_3,wagon_20_4, wagon_20_5, wagon_20_6,
                                wagon_pile.cards[0],wagon_pile.cards[1],wagon_pile.cards[2],wagon_pile.cards[3],wagon_pile.cards[4]] #les derniers éléments doivent etre les cartes de dessus de pioche


def IA_turn():
    #on met un cache transparent
    playsound(sound_IA_turn, block=False)
    pop_up("L'IA à joue ça...", Button((0, 0)))


def player_turn():
    end_turn = False
    player.draw_credit = 2
    pygame.event.clear()

    while end_turn == False :

        Update_Objects(player, board) #mise à jour des variables des objets sur le plateau
        board.represent() #actualisation graphique du plateau

        for event in pygame.event.get(): #vérification des actions du joueur
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                check_all_event(event,interactive_objects)
            if event.type == pygame.MOUSEBUTTONUP :
                check_all_event(event,interactive_objects)
                show_visible_wagon(player, wagon_pile, interactive_objects) #mise à jour des cartes visibles
                print((round(event.pos[0]/screen_width,4),round(event.pos[1]/screen_height,4)))
            if event.type == pygame.KEYUP : #Infos utiles pour débogage
                print("Destinis pioche : ",len(destination_pile.cards))
                print("wagons pioche : ", len(wagon_pile.cards))
                print("destini cards player : ", len(player.destination_cards))
                print("wagon cards player : ", len(player.wagon_cards))
                print("TOTAL : ",len(destination_pile.cards)+len(wagon_pile.cards)+len(player.destination_cards)+len(player.wagon_cards))

        Update_Objects(player, board)  # mise à jour des variables des objets sur le plateau
        board.represent()  # actualisation graphique du plateau

        pygame.display.update()

        if player.draw_credit <= 0:
            end_turn = True

def game():

    #INITIALISATION
    end_game = False
    destination_pile.mix() #mélange des pioches
    wagon_pile.mix()
    show_visible_wagon(player, wagon_pile, interactive_objects)  # première mise à jour des cartes wagons visibles
    Update_Objects(player, board)  # mise à jour des variables des objets sur le plateau
    board.represent()  # actualisation graphique du plateau
    pop_up("A votre tour de commencer, utilisez les icones bleues pour vous aider !", Button((0, 0)))
    Update_Objects(player, board)  # mise à jour des variables des objets sur le plateau
    board.represent()  # actualisation graphique du plateau
    pygame.display.update()
    #choix des cartes destinations
    player.draw_credit = 2
    destination_pile.mouse_click()
    message("A votre tour : Piochez 2 cartes wagons, Piochez d'autres cartes destinations, ou prenez une route.",instruction_button)

    while end_game != True :

        message("A votre tour : Piochez 2 cartes wagons, Piochez d'autres cartes destinations, ou prenez une route.",instruction_button)
        pygame.display.update()
        player_turn()
        message("C'est au tour de votre adversaire.",instruction_button)
        pygame.display.update()
        time.sleep(0.2)
        IA_turn()
        pygame.display.update()

        #vérification fin de pioches
        if len(wagon_pile.cards) <= 11:
            np.random.shuffle(used_cards)
            wagon_pile.cards = np.append(wagon_pile.cards,used_cards)
            if len(used_cards) == 0 : #pour eviter bug au cas ou personne ne se débarasse de ses cartes
                np.random.shuffle(wagon_cards)
                wagon_pile.cards = np.append(wagon_pile.cards, wagon_cards)

        #vérification fin de jeu
        end_game = True
        #si il reste une route que le joueur et l'IA peuvent remplir, alors le jeu continue,sinon on l'arrête
        for road in roads :
            if road.taken == False and len(road.sites) <= player.wagons :
                end_game = False
                break


    playsound(sound_end,block=False)

game()