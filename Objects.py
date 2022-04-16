import numpy as np
import copy

class Card:
    """
    Classe qui décrit l'objet carte

    Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

    """
    def __init__(self,type, color = "None", destination = ("None","None")):
        """
            Créer une carte avec le type et la couleur voulu ou la destination voulu.

            Paramètres :
            ----------------
            type : string
                "destination" = Cartes destinations, "wagon" = Cartes wagon.

            Color : string (Seulement pour les cartes de type wagon)
                "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout".

            destination : double string (Seulement pour les cartes de type destination)
                ("Ville1","Ville2").
            ----------------
        """

        self.type = type
        self.color = color
        self.destination = destination

class Draw_pile:
    """
       Classe qui décrit l'objet paquet de carte
       (Utile pour définir les différentes pioches)

       Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

    """
    def __init__(self,cards):
        """
            Créer un paquet de cartes avec les cartes choisis.

            Paramètres :
            ----------------
            cards : np.array
                array numpy de toutes les cartes qui composent le paquet de carte.
            ----------------
        """

        self.cards = copy.deepcopy(cards)

    def mix(self):
        """
           Mélange le paquet de carte.
       """

        np.random.shuffle(self.cards)

    def draw(self,amount,target):
        """
           Pioche le nombre de carte donné dans le paquet de cartes et les ajoutes au paquet cible.

           Paramètres :
           ----------------
           amount : int
               nombre de cartes à piocher.

           target : Draw_pile Object
               paquet qui va recevoir les cartes (Main de joueur, défausse...)
           ----------------
       """

        for i in range(amount):
            target.cards = np.append(target.cards,self.cards[-1])
            self.cards = np.delete(self.cards,-1)


