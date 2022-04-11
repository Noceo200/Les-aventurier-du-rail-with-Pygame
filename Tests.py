from Objects import *

"""
Test des objets
"""

class TestCard: #Carte

    def __init__(self,type, color = "None"): #Type de carte : "destination" = Cartes destinations, "wagon" = Cartes wagon // Couleur : "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout"
        self.type = type
        self.color = color

class TestDraw_pile: #pioche de carte

    def __init__(self,cards): #Cards = array numpy de toutes les cartes qui composent la pioche
        self.cards = cards

    def mix(self): #on mélange le paquet de cartes
        np.random.shuffle(self.cards)

    def draw(self,amount): #on pioche "amount" cartes
        for i in range(amount):
            np.delete(self.cards,len(self.cards)-1)