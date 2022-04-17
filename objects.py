import numpy as np
import copy
from functions import *

class Click_area():
    #seulement pour partie graphique
    #Class mère des zonnes cliquable avec détection si la souris passe dessus et si clique effectué (zone cliquable = bouttons + cartes)
    pass

class Card(Click_area):
    """
    Classe qui décrit l'objet carte, qui peut etre soit une carte destination, soit une carte wagon, cette classe hérite de la classe Click_area qui permet de rendre un objet intéractif graphiquement.

    Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

    Paramètres :
            type(string)
                Soit "destination" = Cartes destinations soit "wagon" = Cartes wagon.

            color(string) (Seulement pour les cartes de type wagon)
                Choix entre les couleurs possibles pour les wagons, "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout".

            destination(string,string) (Seulement pour les cartes de type destination)
                ("Ville1","Ville2").
    """
    def __init__(self,type, color = "None", destination = ("None","None")):
        """
            Créer une carte avec le type et la couleur voulu ou la destination voulu.
        """

        self.type = type
        self.color = color
        self.destination = destination

    def represent(self,position):
        #seulement pour partie graphique
        #doit représenter la carte la ou position donné (c'est ici que il faut mettre des représentation différente en fonction couleur et type carte)
        pass

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
             Nom du joueur.

           pion(Object.Wagon)
             Motif qui représente les wagons du joueur sur le plateau.

           wagon_cards(Object.Draw_pile)
             Paquet de cartes wagon du joueur.

           destination_cards(Object.Draw_pile)
             Paquet de cartes destination du joueur.
    """
    def __init__(self, name, pion, wagon_cards, destination_cards):
        """
            Créer un joueur avec le nom donné et ses cartes.
        """

        self.name = name
        self.pion = pion #motif qui va representer les wagon du joueur posés sur le plateau
        self.wagon_cards = wagon_cards #cartes wagon du joueur
        self.destination_cards = destination_cards #cartes destination du joueur
        self.wagons = 45 #chaque joueur commence avec 45 wagons
        self.draw_credit = 2 #nombre de carte que le joueur peut piocher (piocher une locomotive termine le tour donc coute 2 credits par exemple)
        self.status = "" #status du joueur qui permet de savoir si il est en train de faire une action ou pas*
        self.linked_cities = np.array([]) #villes reliées par le joueur (mise a jour à chaque fois qu'il prend une route en ajoutant couple ("ville1","ville2"))

        self.cards_bar = Draw_pile(np.array([Card("wagon",color="rose"),
                                            Card("wagon",color="blanc"),
                                            Card("wagon",color="bleu"),
                                            Card("wagon",color="jaune"),
                                            Card("wagon",color="orange"),
                                            Card("wagon",color="noir"),
                                            Card("wagon",color="rouge"),
                                            Card("wagon",color="vert"),
                                            Card("wagon",color="tout")])) #bar de cartes utiles pour la partie graphique ensuite

        self.update() #on met à jour le player graphiquement

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
            pioche.draw(1,self.wagon_cards,-indice)
        else :
            if pioche.cards[-indice].color == "tout" and self.draw_credit > 1 : #si c'est une locomotive et que le joueur à le droit de la piocher
                self.draw_credit -= 2  # on retire deux crédits
                pioche.draw(1, self.wagon_cards, -indice)
            elif pioche.cards[-indice].color == "tout" : #sinon si il peut pas piocher la locomotive
                message("Vous ne pouvez pas piocher de locomotive après avoir piocher une première carte",5)
                pass
            else : #sinon si c'est une autre carte
                self.draw_credit -= 1  # on retire un crédit
                self.status = "drawing_wagon"  # mise à jour du status du joueur
                pioche.draw(1, self.wagon_cards, -indice)

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

        #le programme principale gère le changement graphique qui affiche les cartes destinations

        self.draw_credit -= 1  # on retire un crédit
        self.status = "drawing_destination1"  # mise à jour du status du joueur
        pioche.draw(1, self.destination_cards, -indice)

        if self.draw_credit == 0:  # si le joueur a pioché sa deuxième carte destination, on change son status pour l'autoriser à arreter de piocher
            self.status = "drawing_destination2"

        if self.draw_credit == -1: #le joueur peut piocher jusqu'a 3 cartes destination, son tour se termine quand il a -1 credits ou quand il veut piocher que 2 cartes
            self.status = "None"

    def take_route(self,road,pioche,verif = False):
        """
            Permet au joueur de prendre possession d'une route lorsque c'est sont tour.

            Paramètres :
            road(Objetc.Road)
                Route que le joueur souhaite prendre.

            pioche(Object.Draw_pile)
                Pioche où défaussez les cartes.

            verif(Bool)
                Paramètre pour définir si il a le droit de prendre la route ou pas.
        """
        joker_use = 0 #variable pour gérer l'utilisation ou non de joker
        color_chose = road.color #variable pour gérer le choix de la couleur à utiliser lorsque la route le permet, elle vaut celle de la route par defaut

        #VERIFICATION
        if road.taken == False and  verif == False :
            wagons_player = player_wagon_cards(self) #dictionnaire qui compte les cartes du joueur en fonction des couleurs
            if road.color == "tout" : #si c'est une route où on peut mettre des wagons de la couleur souhaitée, il suffit d'avoir assez de wagon d'une même couleur ou d'avoir des jokers
                if max(wagons_player.items()) >= len(road.sites): #si on a assez de wagons d'une meme couleur, on demande laquelle utiliser
                    color_possible = np.array([]) #on regard entre quelles couleur l'utilisateur à le choix
                    i = 0
                    for key in wagons_player:
                        if wagons_player[key] >= len(road.sites):
                            color_possible = np.append(color_possible,0) #on ajoute la position de la couleur qu'on peut utiliser
                        i += 1
                    color_chose = pop_up("Choisissez quels wagons de la même couleur poser, il en faut "+str(len(road.sites)),
                                         [self.cards_bar.cards[i] for i in color_possible]).color # propose à l'utilisateur de choisir entre les wahons possibles et renvoie la couleur de la carte choisi par l'utilisateur
                    verif = True
                elif max(wagons_player.items())+wagons_player["tout"] >= len(road.sites): #si on a pas assez de wagons d'une meme couleur mais qu'on a assez de jokers, on demande quelle couleur utiliser avec les jokers
                    color_possible = []  # on regard entre quelles couleur l'utilisateur à le choix
                    i = 0
                    for key in wagons_player:
                        if wagons_player[key] >= len(road.sites)-wagons_player["tout"]:
                            color_possible = np.append(color_possible,0)  # on ajoute la position de la couleur qu'on peut utiliser
                        i += 1
                    color_chose = pop_up("Vous avez "+str(wagons_player["tout"])+" jokers, "
                                         +"choisissez quels wagons de la même couleur poser, il en faut " + str(len(road.sites)-wagons_player["tout"]),
                                         [self.cards_bar.cards[i] for i in color_possible]).color  # propose à l'utilisateur de choisir entre les wagons possibles et renvoie la couleur de la carte choisi par l'utilisateur
                    joker_use = len(road.sites) - wagons_player[color_chose] #nombre de joker a utiliser
                    verif = True
                else :
                    message("Vous n'avez pas assez de wagons d'une même couleur, choisissez une autre route ou une autre action",4)
            else : #sinon si c'est une route avec une couleur définie
                if wagons_player[road.color] >= len(road.sites):
                    verif = True
                elif wagons_player[road.color]+ wagons_player["tout"] >= len(road.sites):
                    joker_use = len(road.sites) - wagons_player[color_chose]
                    verif = True
                else :
                    message("Vous n'avez pas assez de wagons "+str(road.color)+", il en faut "+str(len(road.sites)),4)
        elif verif == False :
            message("Cette routes est déjà prise",2)

        if verif == True:
            # PRISE DE LA ROUTE
            self.draw_credit -= 2
            self.status = "None"
            self.wagons -= len(road.sites)

            #on défausse les cartes utilisées de son paquet
            delete_cards(self,color_chose,len(road.sites)-joker_use,pioche)
            delete_cards(self,"tout",joker_use,pioche)

            road.taken = True
            check_real_roads(self, road)  # ajout et mise à jour des différentes villes reliées par le joueur
            """
            Seulement pour partie graphique :
            Ajout des wagons du joueur sur la route prise,

            for site in road.sites :
                 self.pion.represent(site.position[0],site.position[1]) #les wagons du joueur se placent sur tout les emplacements libres de la route
            """

    def update(self):
        """
            Met à jour les différents éléments du joueur.
        """
        #seulement pour partie graphique
        pass

    def represent(self,position):
        """
            Permet de representer graphiquement le joueur avec ces cartes
        """
        #self.cards_pack.represent(position) utiliser representation deja codé des autres objets pour les afficher
        #utiliser le dictionnaire renvoyé par player_wagon_cards() pour afficher les paquets de cartes de différentes couleurs devant le joueurs
        #définir ici ou afficher paramètre comme nom, nb wagon, credit pioche...
        #Voir pour affichage des destinations choisis par l'utilisateur avec zone cliquable qui utilise pop_up("Voila vos cartes destinations",np.array([mettre carte destination])) (pas oublié de changer status joueur en "pop_up")
        pass

class Board():
    """
        Plateau de jeu.

        Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

        Paramètres :
        destination_pile(Object.Draw_pile)
            Pioche pour les cartes destination.

        wagon_pile(Object.Draw_pile)
            Pioche pour les cartes wagon.

        cities(numpy.Array(Object.City))
            Villes présentent dans le jeu.

        roads(numpy.Array(Object.Road))
            Routes présente dans le jeu.
    """

    def __init__(self,destination_pile,wagon_pile,cities,roads):
        """
            Créer un plateau avec les pioches.
        """
        self.destination_pile = destination_pile
        self.wagon_pile = wagon_pile
        self.cities = copy.deepcopy(cities)
        self.roads = copy.deepcopy(roads)


    def represent(self):
        """
            Permet de representer graphiquement le plateau avec ses pioches, ses routes et ses villes.
        """
        # Exemple code :
        """
            for road in roads :
                road.represent() #utilisation de la méthode represent de chaque route pour qu'elles se placent toutes seul la ou il faut (avec zone cliquable)
        """

class Road():
    """
        Classe qui décrit une route.

        Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

        Paramètres :
               cities(string,string)
                 Corespond aux villes reliées par cette route.

               sites(numpy.Array(Button))
                 Ensembles des emplacements à remplir de wagon pour relier les deux villes.

               color(string)
                 Couleur de la route. ("rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout")
    """

    def __init__(self,cities,sites,color):
        """
            Créer une route qui relie les deux villes donnés en paramètre
        """
        self.cities = cities
        self.sites = copy.deepcopy(sites)
        self.taken = False #booléen pour savoir si la route est prise ou pas (change ca méthode de représentation en conséquence)
        self.color = color

class City():
    #seulement pour partie graphique
    pass

class Wagon():
    #seulement pour partie graphique
    pass

class Button(Click_area):
    #seulement pour partie graphique
    #Ajouter variable group pour savoir à quel groupe appartient le bouton (utile pour selection graphique d'un emplacement wagon par joueur)
    pass

class Group():
    #seulement pour partie graphique
    #permet que si joueur clique sur un des emplacement libre sur le plateau, on puisse accéder au groupe d'emplacements qui représente la route en question
    pass
