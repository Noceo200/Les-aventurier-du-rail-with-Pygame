import numpy as np
import copy
from functions import *

class Card:
    """
    Classe qui décrit l'objet carte, qui peut etre soit une carte destination, soit une carte wagon.

    Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

    Paramètres :
            type(string)
                Soit "destination" = Cartes destinations soit "wagon" = Cartes wagon.

            color(string) (Seulement pour les cartes de type wagon)
                Choix entre les couleurs possibles pour les wagons, "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout".

            destination(double string) (Seulement pour les cartes de type destination)
                ("Ville1","Ville2").
    """
    def __init__(self,type, color = "None", destination = ("None","None")):
        """
            Créer une carte avec le type et la couleur voulu ou la destination voulu.
        """

        self.type = type
        self.color = color
        self.destination = destination

class Draw_pile:
    """
       Classe qui décrit l'objet paquet de carte
       (Utile pour définir les différentes pioches et mains des joueurs)

       Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

       Paramètres :
            cards(numpy.array)
                array numpy de toutes les cartes qui composent le paquet de carte.
    """
    def __init__(self,cards):
        """
            Créer un paquet de cartes avec les cartes choisis.
        """

        self.cards = copy.deepcopy(cards)

    def mix(self):
        """
           Mélange le paquet de carte.
        """

        np.random.shuffle(self.cards)

    def draw(self,amount,target,position = -1):
        """
           Pioche le nombre de carte donné dans ce paquet de cartes et les ajoutes au paquet cible.

           Paramètres :
               amount(int)
                 Nombre de cartes à piocher.

               target(Object.Draw_pile)
                 Paquet qui va recevoir les cartes (Main de joueur, défausse...)

               position(int)
                 Position à partie de laquelle piocher, permet de piocher une carte spécifique dans la pioche. Par défaut, on commence avec la carte au dessus du paquet.
       """

        for i in range(amount):
            target.cards = np.append(target.cards,self.cards[position])
            self.cards = np.delete(self.cards,position)

class Player:
    """
    Classe qui décrit un joueur.

    Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

    Paramètres :
           name(string)
             nom du joueur.
    """
    def __init__(self, name):
        """
            Créer un joueur avec le nom donné.
        """

        self.name = name
        self.cards = np.array([]) #cartes du joueur, aucune au début
        self.wagons = 45 #chaque joueur commence avec 45 wagons
        self.draw_credit = 2 #nombre de carte que le joueur peut piocher (piocher une locomotive termine le tour donc coute 2 credits par exemple)
        self.status = "" #status du joueur qui permet de savoir si il est en train de faire une action ou pas


    def draw_wagon(self,indice,pioche):
        """
            Permet au joueur de piocher une carte wagon lorsque c'est sont tour.

            Paramètres :
            indice(int)
                indice qui permet de choisir quelle carte il veut piocher :
                - indice entre 1 et 6 => Le joueur veut piocher une des 6 cartes wagon face visible
                - indice = 7 => Le joueur veut piocher dans la pioche (cartes face cachées)

            pioche(Object.Draw_pile)
                paquet de cartes qui correspond à la pioche pour les cartes wagon
        """

        if indice == 7 : #si le joueur pioche dans la pioche, il perd juste un crédit, et il ne peut plus piocher de locomotive face visible
            self.draw_credit -= 1 #on retire un crédit
            self.status = "drawing_wagon" #mise à jour du status du joueur
            pioche.draw(1,self.cards,-indice)
        else :
            if pioche.cards[-indice].color == "tout" and self.draw_credit > 1 : #si c'est une locomotive et que le joueur à le droit de la piocher
                self.draw_credit -= 2  # on retire deux crédits
                pioche.draw(1, self.cards, -indice)
            elif pioche.cards[-indice].color == "tout" : #sinon si il peut pas piocher la locomotive
                print("Vous ne pouvez pas piocher de locomotive après avoir piocher une première carte")
                #Créer un objet avec une méthode qui permet d'afficher un message à l'utilisateur
                pass
            else : #sinon si c'est une autre carte
                self.draw_credit -= 1  # on retire un crédit
                self.status = "drawing_wagon"  # mise à jour du status du joueur
                pioche.draw(1, self.cards, -indice)

        if self.draw_credit == 0: #si le joueur n'a plus de crédit c'est la fin de son tour
            self.status = "None"


    def draw_destination(self,indice,pioche):
        """
            Permet au joueur de piocher une carte destination lorsque c'est sont tour.

            Paramètres :
            indice(int)
                indice qui permet de choisir quelle carte il veut piocher :
                - indice entre 1 et 3

            pioche(Object.Draw_pile)
                paquet de cartes qui correspond à la pioche pour les cartes destination
        """

        self.draw_credit -= 1  # on retire un crédit
        self.status = "drawing_destination1"  # mise à jour du status du joueur
        pioche.draw(1, self.cards, -indice)

        if self.draw_credit == 0:  # si le joueur a pioché sa deuxième carte destination, on change son status pour l'autoriser à arreter de piocher
            self.status = "drawing_destination2"

        if self.draw_credit == -1: #le joueur peut piocher jusqu'a 3 cartes destination, son tour se termine quand il a -1 credits ou quand il veut piocher que 2 cartes
            self.status = "None"


    def take_route(self,route):
        """
            Permet au joueur de prendre possession d'une route lorsque c'est sont tour.

            Paramètres :
            route(Objetc.Road)
                Route que le joueur souhaite prendre
        """

        #utiliser player_wagon_cards(self) pour vérifier si prise de route possible ou non