import unittest
from objects import *
import pygame
import random

"""
 Module de Test. Ce module test les méthodes élémentaires qui sont le plus utilisées dans notre programme.
"""

pygame.init()
display_surface = pygame.display.set_mode((10, 10))

class TestCard(unittest.TestCase):
    """
        Test de l'objet Card, qui représente une carte. Vérification de leur bonne initialisation.
    """
    def setUp(self):
        """
            Création de toutes les cartes possibles pour les tests

             Auteur : NOEL Océan
        """
        #création de toutes les cartes destinations
        self.destination_cards = []
        cards = destination_cards_f() #renvoie les cartes destination possibles depuis le fichier texte fait pour
        for card in cards:
            self.destination_cards.append(Card("destination", destination=(card[0], card[1]), points=int(card[2])))

        #création de toutes les cartes wagon possibles
        self.wagon_cards = []
        color_list = ["rose", "blanc", "bleu", "jaune", "orange", "noir", "rouge", "vert", "tout"]
        for color in color_list:
            for i in range(1):  # 1 carte de chaques couleurs
                self.wagon_cards.append(Card("wagon", color=color))

    def test_init(self):
        """
            Vérification que la variable path des cartes créés est bien assignée automatiquement
            en fonction de la couleur ou de la destination de cette dernière.

             Auteur : NOEL Océan
        """
        #TEST du bon paramétrage des cartes wagons
        for card in self.wagon_cards:
            self.assertEqual(card.path, "Resources/Card_"+card.color+".png")

        #TEST du bon paramétrage des cartes destinations
        for card in self.destination_cards:
            self.assertEqual(card.path, "Resources/Card_"+card.destination[0]+"_"+card.destination[1]+".png")

#création de listes pour les tests de pioches

list_cards = np.array([Card("wagon",color = "bleu"),
                       Card("wagon",color = "bleu"),
                       Card("wagon",color = "rouge"),
                       Card("wagon",color = "rose"),
                       Card("wagon",color = "orange")]) #liste de cartes wagons

list_cards2 = np.array([Card("destination",destination = ("newyork","lecap")),
                       Card("destination",destination = ("pekin","newyork")),
                       Card("destination",destination = ("paris","moscou")),
                       Card("destination",destination = ("mumbay","kualalumpur"))]) #liste de cartes destinations

list_cards_sav = np.array([Card("wagon",color = "bleu"),
                           Card("wagon",color = "bleu"),
                           Card("wagon",color = "rouge"),
                           Card("wagon",color = "rose"),
                           Card("wagon",color = "orange")]) #sauvegarde de la liste de cartes 1 pour comparaison après manipulations pour les tests

list_cards2_sav = np.array([Card("destination",destination = ("newyork","lecap")),
                           Card("destination",destination = ("pekin","newyork")),
                           Card("destination",destination = ("paris","moscou")),
                           Card("destination",destination = ("mumbay","kualalumpur"))])#sauvegarde de la liste de cartes 2 pour comparaison après manipulations pour les tests

class TestDraw_pile(unittest.TestCase):
    """
        Test de l'objet Draw_pile, paquet de cartes.
    """
    def setUp(self):
        """
            Création des pioches.

            Auteur : NOEL Océan
        """
        self.pile1 = Draw_pile(list_cards)
        self.pile2 = Draw_pile(list_cards2)

    def test_init(self):
        """
            Vérification que la pioche créée contient bien les cartes des listes initiales

             Auteur : NOEL Océan
        """
        # ////TESTS////
        # on vérifie que la taille des pioches est correcte
        self.assertEqual(len(self.pile1.cards), len(list_cards))
        self.assertEqual(len(self.pile2.cards), len(list_cards2))

        #on vérifie que chaque carte du paquet correspond bien à celle voulu
        self.assertEqual([card.color for card in self.pile1.cards], [card.color for card in list_cards_sav])
        self.assertEqual([card.destination for card in self.pile2.cards],[card.destination for card in list_cards2_sav])

    def test_mix(self):
        """
            Test la méthode pour mélanger les cartes

             Auteur : NOEL Océan
        """
        # ////INITIALISATION////
        self.pile1.mix() #on mélange les carte
        self.pile2.mix()
        # ////TESTS////
        #on vérifie que les paquets sont différents
        self.assertNotEqual([card.color for card in self.pile1.cards], [card.color for card in list_cards_sav])
        self.assertNotEqual([card.destination for card in self.pile2.cards], [card.destination for card in list_cards2_sav])

    def test_draw(self):
        """
            On test la méthode pour piocher, elle renvoie une liste des cartes qu'on a pioché et les enlève de la pioche cible.

             Auteur : NOEL Océan
        """
        for i in range(10): #on fait 10 tests différents avec des valeurs aléatoires
            amount1 = random.randint(0,len(self.pile1.cards)-1) #nombre de carte à piocher dans la pioche1
            amount2 = random.randint(0,len(self.pile2.cards)-1) #nombre de carte à piocher dans la pioche2
            pos1 = random.randint(0,len(self.pile1.cards)-1-amount1) #a partir de quelle position piocher dans la pioche 1
            pos2 = random.randint(0,len(self.pile2.cards)-1-amount2)#a partir de quelle position piocher dans la pioche 1

            # ////INITIALISATION////
            to_draw1 = self.pile1.cards[pos1:pos1+amount1] #résultat auquel on s'attend après avoir piocher amount1 cartes depuis la carte de position pos1 de la pioche 1
            to_draw2 = self.pile2.cards[pos2:pos2+amount2] #résultat auquel on s'attend après avoir piocher amount2 cartes depuis la carte de position pos2 de la pioche 2
            draw1 = self.pile1.draw(amount1,pos1) #on pioche amount1 cartes depuis la carte de position pos1
            draw2 = self.pile2.draw(amount2,pos2) #on pioche amount2 cartes depuis la carte de position pos2
            # ////TESTS////
            #vérification des tailles
            self.assertEqual(len(draw1), len(to_draw1))
            self.assertEqual(len(draw2), len(to_draw2))

            #verification qu'on a les cartes voulus en piochant
            self.assertEqual([card.color for card in draw1], [card.color for card in to_draw1])
            self.assertEqual([card.destination for card in draw2], [card.destination for card in to_draw2])

            #remise des cartes dans les pioches pour prochain test
            self.pile1.cards = np.append(self.pile1.cards,draw1)
            self.pile2.cards = np.append(self.pile2.cards,draw2)


if __name__ == '__main__' :
    unittest.main()

