import unittest
import numpy as np
from objects import *

"""
Test des objets
"""

class TestCard(unittest.TestCase):

    def test_init(self): #vérification de l'initialisation de notre objet
        #création des objets utiles
        card1 = Card("destination")
        card2 = Card("destination",destination = ("Ville1","Ville2"))
        card3 = Card("wagon",color = "bleu")

        # ////TESTS////
        self.assertEqual(card1.type,"destination")
        self.assertEqual(card1.color, "None")
        self.assertEqual(card1.destination, ("None","None"))
        self.assertEqual(card2.type, "destination")
        self.assertEqual(card2.color, "None")
        self.assertEqual(card2.destination, ("Ville1","Ville2"))
        self.assertEqual(card3.type, "wagon")
        self.assertEqual(card3.color, "bleu")
        self.assertEqual(card3.destination, ("None", "None"))

class TestDraw_pile(unittest.TestCase):

    def setUp(self): #création des objets utiles
        self.list_cards = np.array([Card("destination",destination = ("Ville1","Ville2")),
                               Card("destination", destination=("Ville3", "Ville4")),
                               Card("wagon",color = "bleu"),
                               Card("wagon",color = "bleu"),
                               Card("wagon",color = "rouge"),
                               Card("wagon",color = "rose"),
                               Card("wagon",color = "orange")])

        self.pile = Draw_pile(self.list_cards)

    def test_init(self): #vérification de l'initialisation de notre objet
        # ////INITIALISATION////
        verif = True
        # ////TESTS////
        if len(self.pile.cards) != len(self.list_cards):
            verif = False
        else : #verification qu'on a les cartes voulus
            for i in range(len(self.list_cards)):
                if (self.pile.cards[i].destination != self.list_cards[i].destination) or (self.pile.cards[i].color != self.list_cards[i].color):
                    verif = False
        self.assertTrue(verif)

    def test_mix(self):
        # ////INITIALISATION////
        self.pile.mix()
        # ////TESTS////
        verif = False
        for i in range(len(self.list_cards)):
            if (self.pile.cards[i].destination != self.list_cards[i].destination) or (self.pile.cards[i].color != self.list_cards[i].color):
                verif = True

        self.assertTrue(verif) #on vérifie que le paquet de carte n'est plus le meme qu'avant

    def test_draw(self):
        # ////INITIALISATION////
        pile2 = Draw_pile(np.array([]))
        to_draw = self.pile.cards[len(self.pile.cards)-5:len(self.pile.cards)] #ce qui est censé etre pioché
        initial_len = len(self.pile.cards) #nombre de cartes avant pioche dans le paquet ou on va piocher
        self.pile.draw(5,pile2)
        verif = True
        # ////TESTS////
        if len(pile2.cards) != len(to_draw):
            verif = False
        else : #verification qu'on a les cartes voulus dans la pile cible
            for i in range(len(to_draw)):
                if (pile2.cards[i].destination != to_draw[len(to_draw)-i-1].destination) or (pile2.cards[i].color != to_draw[len(to_draw)-i-1].color):
                    verif = False
        self.assertTrue(verif) #on vérifie que la pile 2 à bien recu les cartes a piocher
        self.assertEqual(len(self.pile.cards), initial_len-len(to_draw)) #on vérifie qu'on a bien effacer les cartes de la pile initial


if __name__ == '__main__' :
    unittest.main()