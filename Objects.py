import numpy as np

class Card:
    """
    Classe qui décrit l'objet carte
    """
    def __init__(self,type, color = "None"):
        """
            Créer une carte avec le type et la couleur voulu.

            Paramètres :
            ----------------
            type : string
                "destination" = Cartes destinations, "wagon" = Cartes wagon.

            Color : string
                "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout".
            ----------------
        """

        self.type = type
        self.color = color

class Draw_pile:
    """
       Classe qui décrit l'objet paquet de carte
       (Utile pour définir les différentes pioches)
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

        self.cards = cards

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
            np.append(target.cards,self.cards[len(self.cards)-1])
            np.delete(self.cards,len(self.cards)-1)
