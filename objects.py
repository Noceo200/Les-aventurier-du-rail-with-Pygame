import copy
from functions import *
import pygame
from playsound import playsound
import random

#initialisation des sons

sound_take_road = 'Resources/Songs/Sifflet.mp3'
sound_draw_card = 'Resources/Songs/take_card2.mp3'
sound_mouse_pass = 'Resources/Songs/clic.mp3'
sound_card_shuffle = 'Resources/Songs/card_shuffling3.mp3'

class Graphic_area():
    """
        Classe mère des éléments grqphiques à afficher pour l'IHM.

        Auteur : NOEL Océan

        :param position: Position associée à l'objet graphique en pourcentage.
        :type position: tuple (int,int)
        :param scale: Taille associée à l'objet graphique en pourcentage.
        :type scale: float
        :param image: Chemin de l'image associée à l'objet graphique.
        :type image: string
        :param image2: Chemin de la deuxième image associée à l'objet graphique.
        :type image2: string
        :param convert: Défini si il faut convertir l'image en jpeg (True permet de faire des jeu de transparence).
        :type convert: bool
        :param center: Indique si l'objet doit être centré par rapport à sa position ou non (par défaut la position correspond au coin supérieur gauche).
        :type center: bool
        :param texte: Texte associée à l'objet graphique.
        :type texte: string
        :param sens: Sens associée à l'objet graphique en degrés.
        :type sens: float
    """
    def __init__(self,position,scale,image,image2 = "",convert = False,center = False,texte = "",sens = 0):

        self.position = position
        self.path = image
        self.image = pygame.image.load(self.path) #chargement de l'image
        self.image2 = image2
        self.scale = scale
        self.passed = False #variable pour gestion evennements
        self.texte = texte #texte à mettre sur l'image
        self.center = center
        self.sens = sens

        #Conversion en jpeg de l'image si nécessaire (pour autoriser transparence)
        if convert == True:
            self.image= self.image.convert()
        #Determination de la position en pixels
        self.x = int(self.position[0] * pygame.display.Info().current_w)
        self.y = int(self.position[1] * pygame.display.Info().current_h)
        #Mise à l'échelle de l'affichage
        self.reso = self.image.get_width()/self.image.get_height()
        perso_heigth = pygame.display.Info().current_h*self.scale
        self.image = pygame.transform.scale(self.image, (int(perso_heigth*self.reso), int(perso_heigth)))
        # Initialisation du sens de l'image
        self.image = pygame.transform.rotate(self.image, self.sens)
        # Centrage position
        if self.center == True :
            self.x, self.y = (int(self.x - self.image.get_width() / 2), int(self.y - self.image.get_height() / 2))

    def represent(self):
        """
            Représente graphiquement l'objet sur le plateau.

            Auteur : NOEL Océan
        """
        #Affichage
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.image, (self.x, self.y))
        if self.texte != "" and (self.path == "Resources/default_button.png" or self.path == "Resources/instructions.png"): #donc si on a initialiser le texte pour le mettre au dessus de l'image
            l = int(pygame.display.Info().current_h / 32.6)
            police = pygame.font.SysFont("Monospace", l, bold=True)
            texte = ""
            texte2 = ""
            if len(self.texte) > 56:  # si le texte est trop grand et doit aller sur une deuxième ligne
                texte = self.texte[0:56]
                texte2 = self.texte[56:]
                texte = police.render(texte, 1, (0, 0, 0))
                texte2 = police.render(texte2, 1, (0, 0, 0))
            else:
                texte = police.render(self.texte, 1, (0, 0, 0))
            #affichage sur une ligne ou deux
            if texte2 != "":  # si on doit afficher une deuxième ligne de texte
                ecart_interligne = int(pygame.display.Info().current_h / 80) #trouvé a taton
                display_surface.blit(texte, (int(self.x + (self.image.get_width()/2) - (texte.get_width()/2)), int(self.y + self.image.get_height()/2 - (texte.get_height()/2)-ecart_interligne)))
                display_surface.blit(texte2, (int(self.x + (self.image.get_width()/2) - (texte2.get_width()/2)), int(self.y + self.image.get_height()/2 - (texte2.get_height()/2)+ecart_interligne)))
            else:
                display_surface.blit(texte, (int(self.x + (self.image.get_width()/2) - (texte.get_width()/2)), int(self.y + self.image.get_height()/2 - (texte.get_height()/2)))) #on place le texte au centre de l'image

    def check_event(self,event):
        """
            Vérifie si l'utilisateur place sa souris sur la zone ou clique sur la zone graphique de l'objet et appel les méthodes adaptées en fonction de l'action.

            :param event: Action réalisée par l'utilisateur à analyser (clic, déplacement de souris).
            :type event: Object pygame.event

            Auteur : NOEL Océan
        """
        center = (self.x+self.image.get_width()/2,self.y+self.image.get_height()/2)#position centrale de l'object
        if event.type == pygame.MOUSEMOTION:
            if abs(event.pos[0]-center[0]) <= self.image.get_width()/2 and abs(event.pos[1] - center[1]) <= self.image.get_height()/2 :
                if self.passed == False:
                    self.mouse_pass(True)
                    self.passed = True
            else:
                if self.passed == True:
                    self.mouse_pass(False)
                    self.passed = False
        if event.type == pygame.MOUSEBUTTONUP:
            if abs(event.pos[0] - center[0]) <= self.image.get_width()/2 and abs(event.pos[1] - center[1]) <= self.image.get_height()/2 :
                self.mouse_click()

    def mouse_pass(self,statut):
        """
            Action à éxecuter en cas de survol de la zone graphique de l'objet par la souris.

            :param statut: Détermine si la souris vient de rentrer dans la zone ou si elle en est sorti.
            :type statut: bool

            Auteur : NOEL Océan
        """
        if statut == True:
            playsound(sound_mouse_pass, block=False)#son de passage de souris
            if self.texte == "" and self.image2 == "": #si on a bouton qui est cliquable, il devient transparent
                self.image.set_alpha(100)
            else :
                pop_up(self.texte,button = self,allow_return=False) #sinon, c'est un bouton qui doit afficher une pop up, on l'affiche
        else:
            if self.texte == "" and self.image2 == "":
                self.image.set_alpha(255)
        pygame.display.update()

    def mouse_click(self):
        """
            Action à éxecuter en cas de clique dans la zone graphique de l'objet par la souris. Par défaut il ne se passe rien.

            Auteur : NOEL Océan
        """
        pass

class Card(Graphic_area):
    """
         Classe qui décrit l'objet carte, qui peut etre soit une carte destination, soit une carte wagon, cette classe hérite de la classe Graphique_area qui permet de rendre un objet intéractif graphiquement.

        Auteur : NOEL Océan

        :param type: Définit le type de la carte. "destination" = Carte destination, "wagon" = Carte wagon.
        :type type: string
        :param player: Joueur de la partie.
        :type player: Object Player
        :param pioche: Pioche dans laquelle se trouve la carte.
        :type pioche: Object Draw_pile
        :param color: Décrit la couleur de la carte (utile seulement pour type "wagon"). Couleurs possibles pour les wagons, "rose","blanc","bleu","jaune","orange","noir","rouge","vert","tout"..
        :type color: string
        :param destination: Décrit la destination de la carte (utile seulement pour type "destination"). Destination donnée sous la forme : ("Ville1","Ville2")
        :type destination: tuple (string,string)
        :param points: Décrit les points associés à la carte (utile seulement pour type "destination").
        :type points: int
        :param position: Décrit la position associée à la carte en pourcentage.
        :type position: tuple (int,int)
        :param scale: Décrit taille associée à la carte en pourcentage.
        :type scale: float
        :param convert: Défini si il faut convertir l'image en jpeg.
        :type convert: bool
    """
    def __init__(self,type, player = "", pioche = "", color = "None", destination = ("None","None"),points = 0,position = (0,0),scale=1,convert = True):
        """
            Créer une carte avec le type et la couleur voulu ou la destination voulu et assigne automatiquement un chemin vers l'image associée.
        """
        self.destination = destination
        image = ""
        if type == "wagon":
            image = "Resources/Card_"+color+".png"
        elif type == "destination":
            image = "Resources/Card_"+self.destination[0]+"_"+self.destination[1]+".png"
        super().__init__(copy.deepcopy(position), scale, image,convert = convert)
        self.type = type
        self.color = color
        self.changed = False
        self.indice = 0 #indice de position de la carte dans la pioche, vaut 0 par défaut mais mise à jour uniquement lorsque les cartes on besoin d'etre visibles
        self.player = player #utile pour accéder aux pioches du joueur
        self.pioche = pioche #utile pour accéder à la pioche à laquelle elle appartient
        self.points = points #points que rapport la carte (seulement pour les cartes destinations)
        self.ok = False #booléen qui indique si une carte destination a été faite ou pas

    def represent(self):
        """
            Représente graphiquement la carte sur le plateau.

            Auteur : NOEL Océan
        """
        if self.changed == True: #Prise en compte du fait que les cartes wagons sont amenée à etre déplacée graphiquement
            #Determination de la position en pixels
            self.x = int(self.position[0] * pygame.display.Info().current_w)
            self.y = int(self.position[1] * pygame.display.Info().current_h)
            #Mise à l'échelle de l'affichage
            perso_heigth = pygame.display.Info().current_h*self.scale
            self.image = pygame.transform.scale(self.image, (int(perso_heigth*self.reso), int(perso_heigth)))
            # Centrage position
            if self.center == True :
                self.x, self.y = (int(self.x - self.image.get_width() / 2), int(self.y - self.image.get_height() / 2))
            self.changed = False


        #Affichage
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.image, (self.x, self.y))

    def mouse_click(self):
        """
            Action à éxecuter en cas de clique sur la carte.
            Appel les méthodes de pioche de cartes du joueur pour piocher la carte.

            Auteur : NOEL Océan
        """
        playsound(sound_draw_card, block=False)
        if self.type == "wagon":
            if self.player.status != "taking_road": #la carte est piochée seulement si elle a pas juste été sélectionnée pour choisir une couleur lors de l'action de prendre une route
                self.player.draw_wagon(self.indice,self.pioche)
        elif self.type == "destination" :
            self.image.set_alpha(255)
            self.player.draw_destination(self.indice,self.pioche)

class Draw_pile(Graphic_area):
    """
        Classe qui décrit l'objet paquet de carte, permet de définir les différentes pioches et mains des joueurs.

        Auteur : NOEL Océan

        :param cards: Cartes de la pioche.
        :type cards: list
        :param player: Joueur de la partie.
        :type player: Object Player
        :param type: Définit le type de pioche. "destination_pile" = pioche de cartes destination, "wagon_pile" = pioche de cartes wagon.
        :type type: string
        :param position: Décrit la position associée à la pioche en pourcentage.
        :type position: tuple (int,int)
        :param scale: Décrit la taille associée à la pioche graphiquement en pourcentage.
        :type scale: float
        :param image: Chemin de l'image associée à la pioche..
        :type image: string
    """

    def __init__(self,cards,player = "", type = "",position = (0,0),scale = 1,image = "Resources/Default_pioche.png"):
        """
            Créer un paquet de cartes avec les cartes choisis.

            Auteur : NOEL Océan
        """
        super().__init__(copy.deepcopy(position),scale,image,convert = True)
        self.cards = cards #Donne accès directement à la variable global cards du programme principale
        self.type = type #variable utile seulement pour pioche wagons ou destinations
        self.player = player #variable utile seulement pour pioche wagons ou destinations

    def mix(self):
        """
           Mélange le paquet de carte.

           Auteur : NOEL Océan
        """
        np.random.shuffle(self.cards)

    def draw(self,amount,position = 0):
        """
            Renvoi les cartes piochées en fonction du nombre et de la position demandé et les suppriment de la pioche.

            :param amount: Nombre de cartes à piocher.
            :type amount: int
            :param position: Position a partie de laquel piocher les cartes dans la pioche.
            :type position: int

            :return: Cartes piochées.
            :rtype: numpy Array

            Auteur : NOEL Océan
        """
        target = np.array([])
        for i in range(amount):
            target = np.append(target,self.cards[position])
            self.cards = np.delete(self.cards,position)
        return target

    def mouse_click(self):
        """
            Action à éxecuter en cas de clique sur la pioche.
            En fonction de la pioche, la méthode permet au joueur de piocher une carte wagon ou ouvre une fenetre pop_up qui lui permet de choisir des cartes destinations à piocher.

            Auteur : NOEL Océan
        """
        if self.type == "wagon_pile":
            playsound(sound_draw_card, block=False)
            self.player.draw_wagon(5, self)
        elif self.type == "destination_pile":
            playsound(sound_card_shuffle, block=False)
            if len(self.player.destination_cards) < 9 : #le joueur est limité a 9 cartes destinations (pour des raisons d'affichage)
                if self.player.draw_credit == 2 :
                    self.player.statut = "Drawing_destination"
                    self.player.draw_credit -= 2  # on retire 2 credits au joueur car il n epeut pas jouer après cette action
                    #mise d'un cache transparent
                    display_surface = pygame.display.get_surface()
                    cache = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
                    cache.set_alpha(128)
                    cache.fill((0, 0, 0))
                    display_surface.blit(cache, (0, 0))  # affichage du cache transparent
                    #initialisation des 3 premières cartes de la pioche de cartes destination
                    for i in range(3):
                        self.cards[i].player = self.player
                        self.cards[i].pioche = self
                        self.cards[i].indice = i
                    #affichage
                    cards = self.cards[0:3]
                    choice = pop_up("Choisisssez un premier objectif", objects=cards, button=Button((0, 0)),choices = True,allow_return = False)
                    if choice != -1 : #si le joueur à fait un choix, il peut en faire un deuxième
                        cards = self.cards[0:2] #on affiche que les deux dernière carte du paquet, elles correspondent à celles que le joueur n'a pas pioché
                        if len(self.player.destination_cards) < 2 : #si on est au début du jeu, on le force à prendre une deuxième carte, sinon il peut en prendre qu'une seule
                            choice = pop_up("Choisisssez un deuxième objectif", objects=cards, button=Button((0, 0)), choices=True,allow_return=False)
                        else :
                            choice = pop_up("Choisisssez un deuxième objectif", objects=cards, button=Button((0, 0)),choices=True, allow_return=True)
                        if choice != -1:
                            cards = self.cards[0:1]
                            pop_up("Choisissez un troisième objectif", objects=cards, button=Button((0, 0)), choices=True,allow_return=True)
                    self.player.statut = "None"
                else :
                    pop_up("Vous n'avez pas assez de crédits",Button((0, 0)))
            else :
                pop_up("Vous êtes limité a 9 objectifs", Button((0, 0)))

            #mise à jour graphique des cartes destinations réussies
            check_destinis(self.player.linked_cities, self.player.destination_cards, ckeck_or_addpoints=False)

class Player():
    """
        Classe qui décrit un joueur et lui assigne ses différents paquets de cartes.

        Auteur : NOEL Océan

        :param name: Nom du joueur.
        :type name: string
    """
    def __init__(self, name):
        """
            Créer un joueur avec le nom donné et ses cartes.

            Auteur : NOEL Océan
        """

        self.name = name
        self.wagon_cards = "" #cartes wagon du joueur
        self.destination_cards = "" #cartes destination du joueur
        self.wagons = 20 #chaque joueur commence avec 45 wagons
        self.draw_credit = 0 #nombre de carte que le joueur peut piocher (piocher une locomotive termine le tour donc coute 2 credits par exemple)
        self.status = "" #status du joueur qui permet de savoir si il est en train de faire une action ou pas*
        self.linked_cities = [] #villes reliées par le joueur (mise a jour à chaque fois qu'il prend une route en ajoutant couple ("ville1","ville2"))
        self.points = 0 #variable pour stocker le score du joueur
        self.used_cards = ""
        self.board = "" #permet de réactualiser partie graphique du plateau depuis joueur
        self.cards_bar = Draw_pile(np.array([Card("wagon",player = self,color="rose"),
                                            Card("wagon",player = self,color="blanc"),
                                            Card("wagon",player = self,color="bleu"),
                                            Card("wagon",player = self,color="jaune"),
                                            Card("wagon",player = self,color="orange"),
                                            Card("wagon",player = self,color="noir"),
                                            Card("wagon",player = self,color="rouge"),
                                            Card("wagon",player = self,color="vert"),
                                            Card("wagon",player = self,color="tout")])) #bar de cartes utiles pour la partie graphique ensuite

        self.cards_number = {"rose": 0, "blanc": 0, "bleu": 0, "jaune": 0, "orange": 0, "noir": 0, "rouge": 0, "vert": 0, "tout": 0}

    def draw_wagon(self,indice,pioche):
        """
            Permet au joueur de piocher une carte wagon lorsque c'est sont tour en vérifiant si il peut.

            :param indice: Position de la carte à piocher. Indice entre 0 et 4 => Le joueur veut piocher une des 5 cartes wagon face visible, Indice 5 => Le joueur veut piocher dans la pioche (cartes face cachées)
            :type indice: int
            :param pioche: Pioche de cartes wagons dans laquelle piocher.
            :type pioche: Object Draw_pile

            Auteur : NOEL Océan
        """

        if indice == 5 : #si le joueur pioche dans la pioche, il perd juste un crédit, et il ne peut plus piocher de locomotive face visible
            self.draw_credit -= 1 #on retire un crédit
            self.status = "drawing_wagon" #mise à jour du status du joueur
            self.wagon_cards = np.append(self.wagon_cards,pioche.draw(1,indice)) #on transfère la carte piocher vers les cartes du joueur
        else :
            if pioche.cards[indice].color == "tout" and self.draw_credit > 1 : #si c'est une locomotive et que le joueur à le droit de la piocher
                self.draw_credit -= 2  # on retire deux crédits
                self.wagon_cards = np.append(self.wagon_cards,pioche.draw(1,indice))
            elif pioche.cards[indice].color == "tout" : #sinon si il peut pas piocher la locomotive
                pop_up("Vous n'avez pas assez de crédit.",Button((0, 0)))
            else : #sinon si c'est une autre carte
                self.draw_credit -= 1  # on retire un crédit
                self.status = "drawing_wagon"  # mise à jour du status du joueur
                self.wagon_cards = np.append(self.wagon_cards,pioche.draw(1,indice))

        #mise a jour du nombre de carte en couleur du joueur
        self.cards_number[self.wagon_cards[-1].color] += 1

        if self.draw_credit == 0: #si le joueur n'a plus de crédit c'est la fin de son tour
            self.status = "None"

    def draw_destination(self,indice,pioche):
        """
            Permet au joueur de piocher une carte destination lorsque c'est sont tour.

            :param indice: Position de la carte à piocher. Indice entre 0 et 2.
            :type indice: int
            :param pioche: Pioche de cartes destinations dans laquelle piocher.
            :type pioche: Object Draw_pile

            Auteur : NOEL Océan
        """

        self.destination_cards = np.append(self.destination_cards, pioche.draw(1, indice))  #transfère la carte piochée de la pioche vers les cartes du joueur


    def take_route(self,road,verif = False,IA = False):
        """
            Permet au joueur de prendre une route lorsque c'est sont tour en vérifiant si il peut et renvoie un booléen ou rien en fonction de si c'est le joeur ou l'IA que tente de prendre une route.

            :param road: Route que le joueur veut prendre.
            :type road: Object Road
            :param verif: Défini si le joueur à le droit de prendre la route peut importe les conditions.
            :type verif: bool
            :param IA: Indique si c'est l'IA ou le joueur qui veut prendre la route.
            :type IA: bool

            :return: Booléen qui indique que l'IA peut prendre la route ou non.
            :rtype: bool or None

            Auteur : NOEL Océan
        """
        joker_use = 0 #variable pour gérer l'utilisation ou non de joker
        color_chose = road.color #variable pour gérer le choix de la couleur à utiliser lorsque la route le permet, elle vaut celle de la route par defaut

        self.status = "taking_road"

        #VERIFICATION
        if IA == False: #si c'est le joueur qui prend une route
            if road.taken == False and  verif == False and self.draw_credit == 2 and self.wagons >= len(road.sites):
                wagons_player = self.cards_number #dictionnaire qui compte les cartes du joueur en fonction des couleurs
                if road.color == "tout" : #si c'est une route où on peut mettre des wagons de la couleur souhaitée, il suffit d'avoir assez de wagon d'une même couleur ou d'avoir des jokers
                    if max(wagons_player.values()) >= len(road.sites): #si on a assez de wagons d'une meme couleur, on demande laquelle utiliser
                        color_possible = [] #on regard entre quelles couleur l'utilisateur à le choix
                        i = 0
                        for key in wagons_player:
                            if wagons_player[key] >= len(road.sites):
                                color_possible.append(i) #on ajoute la position de la couleur qu'on peut utiliser
                            i += 1
                        color_chose = pop_up("Choisissez quelle couleur poser : ",Button((0, 0)),
                                             [self.cards_bar.cards[i] for i in color_possible],allow_return=False).color # propose à l'utilisateur de choisir entre les wagons possibles et renvoie la couleur de la carte choisie
                        verif = True
                    elif max(wagons_player.values())+ wagons_player["tout"] >= len(road.sites): #si on a pas assez de wagons d'une meme couleur mais qu'on a assez de jokers, on demande quelle couleur utiliser
                        color_possible = []  # on regard entre quelles couleur l'utilisateur à le choix
                        i = 0
                        for key in wagons_player:
                            if wagons_player[key] >= len(road.sites)-wagons_player["tout"] and key != "tout": #on ne peut pas choisir la couleur joker dans ce cas
                                color_possible.append(i)  # on ajoute la position de la couleur qu'on peut utiliser
                            i += 1
                        color_chose = pop_up("Choisissez quelle couleur poser : ",Button((0, 0)),
                                             [self.cards_bar.cards[i] for i in color_possible],allow_return=False).color  #propose à l'utilisateur de choisir entre les wagons possibles et renvoie la couleur de la carte choisie
                        joker_use = len(road.sites) - wagons_player[color_chose] #nombre de joker a utiliser
                        verif = True
                    else :
                        pop_up("Vous n'avez pas assez de wagons    d'une même couleur ou de jokers", Button((0, 0)))
                else : #sinon si c'est une route avec une couleur définie
                    if wagons_player[road.color] >= len(road.sites):
                        verif = True
                    elif wagons_player[road.color]+ wagons_player["tout"] >= len(road.sites):
                        joker_use = len(road.sites) - wagons_player[color_chose]
                        verif = True
                    else :
                        pop_up("Il vous manque "+str(len(road.sites)-(wagons_player[road.color]+ wagons_player["tout"]))  +" Wagons "+str(road.color)+" pour    prendre cette route", Button((0, 0)))
            elif verif == False and self.draw_credit == 2 and self.wagons >= len(road.sites): #si la route est prise
                pop_up("Cette route est déjà prise",Button((0, 0)))
            elif self.wagons >= len(road.sites):
                pop_up("Vous n'avez pas assez de crédits", Button((0, 0)))
            else :
                pop_up("Vous n'avez plus assez de wagons", Button((0, 0)))

            if verif == True:
                # PRISE DE LA ROUTE
                self.draw_credit -= 2
                self.wagons -= len(road.sites)

                #on défausse les cartes utilisées de son paquet
                # pour aller plus vite, on ne déplace pas vraiment les cartes du joueur vers la défausse, on créer directement des nouvelles cartes dans la défause
                # ca evite un algorithme pour retrouver les cartes des couleurs concernées dans la liste de carte du joueur
                self.cards_number[color_chose] -= len(road.sites)-joker_use
                self.cards_number["tout"] -= joker_use

                for i in range(len(road.sites)-joker_use):
                    self.used_cards.append(Card("wagon", color = color_chose))
                for i in range(joker_use):
                    self.used_cards.append(Card("wagon", color = "tout"))

                #on ajoute des points au joueur qui dépendent de la taille de la route

                points = [1,2,4,7,10,15]
                for i in range(6):
                    if len(road.sites) == i+1 :
                        self.points += points[i]
                        break
                    elif len(road.sites) >= 7 :
                        self.points += points[5]
                        break

                #mise à jour des villes reliées par le joueur
                add_road(self.linked_cities,road)

                #comparaison avec ses cartes destinations et mise à jour graphique des cartes destinations réussies
                check_destinis(self.linked_cities, self.destination_cards, ckeck_or_addpoints=False)

                #ajout des wagons du joueurs sur les emplacements de la route
                for wagon in road.sites:
                    wagon.place_wagon("player")

                road.taken = True
                Update_Objects(self, "",self.board)  # mise à jour des variables des objets sur le plateau
                self.board.represent()  # actualisation graphique du plateau
                pygame.display.update()
                playsound(sound_take_road, block=True)
            self.status = "None"

        else : #sinon si c'est l'IA qui veut prendre une route
            if road.taken == False and verif == False and self.draw_credit == 2 and self.wagons >= len(road.sites):
                wagons_player = self.cards_number  # dictionnaire qui compte les cartes du joueur en fonction des couleurs
                if road.color == "tout":  # si c'est une route où on peut mettre des wagons de la couleur souhaitée, il suffit d'avoir assez de wagon d'une même couleur ou d'avoir des jokers
                    if max(wagons_player.values()) >= len(road.sites):  # si on a assez de wagons d'une meme couleur, on demande laquelle utiliser
                        color_possible = []  # on regard entre quelles couleur l'utilisateur à le choix
                        i = 0
                        for key in wagons_player:
                            if wagons_player[key] >= len(road.sites):
                                color_possible.append(i)  # on ajoute la position de la couleur qu'on peut utiliser
                            i += 1
                        rand = 0
                        if len(color_possible) > 1:
                            random.randint(0, len(color_possible)-1) #l'IA choisi une couleur au hazard parmi celles disponibles
                        color_chose = self.cards_bar.cards[color_possible[rand-1]].color
                        verif = True
                    elif max(list(wagons_player.values())[0:-1]) + wagons_player["tout"] >= len(road.sites):  # si on a pas assez de wagons d'une meme couleur mais qu'on a assez de jokers, on demande quelle couleur utiliser
                        color_possible = []  # on regard entre quelles couleur l'utilisateur à le choix
                        i = 0
                        for key in wagons_player:
                            if wagons_player[key] >= len(road.sites) - wagons_player["tout"] and key != "tout":  # on ne peut pas choisir la couleur joker dans ce cas
                                color_possible.append(i)  # on ajoute la position de la couleur qu'on peut utiliser
                            i += 1
                        rand = 0
                        if len(color_possible) > 1:
                            rand = random.randint(0,len(color_possible)-1)  # l'IA choisi une couleur au hazard parmi celles disponibles si il y en a plusieurs
                        color_chose = self.cards_bar.cards[color_possible[rand]].color
                        joker_use = len(road.sites) - wagons_player[color_chose]  # nombre de joker a utiliser
                        verif = True

                else:  # sinon si c'est une route avec une couleur définie
                    if wagons_player[road.color] >= len(road.sites):
                        verif = True
                    elif wagons_player[road.color] + wagons_player["tout"] >= len(road.sites):
                        joker_use = len(road.sites) - wagons_player[color_chose]
                        verif = True

            if verif == True:
                # PRISE DE LA ROUTE
                self.draw_credit -= 2
                self.wagons -= len(road.sites)

                # on défausse les cartes utilisées de son paquet
                # pour aller plus vite, on ne déplace pas vraiment les cartes du joueur vers la défausse, on créer directement des nouvelles cartes dans la défause
                # ca evite un algorithme pour retrouver les cartes des couleurs concernées dans la liste de carte du joueur
                self.cards_number[color_chose] -= len(road.sites) - joker_use
                self.cards_number["tout"] -= joker_use

                for i in range(len(road.sites) - joker_use):
                    self.used_cards.append(Card("wagon", color=color_chose))
                for i in range(joker_use):
                    self.used_cards.append(Card("wagon", color="tout"))

                # on ajoute des points au joueur qui dépendent de la taille de la route

                points = [1, 2, 4, 7, 10, 15]
                for i in range(6):
                    if len(road.sites) == i + 1:
                        self.points += points[i]
                        break

                # mise à jour des villes reliées par le joueur
                add_road(self.linked_cities, road)

                # comparaison avec ses cartes destinations et mise à jour graphique des cartes destinations réussies
                check_destinis(self.linked_cities, self.destination_cards, ckeck_or_addpoints=False)

                # ajout des wagons du joueurs sur les emplacements de la route
                for wagon in road.sites:
                    wagon.place_wagon("IA")

                road.taken = True
                self.board.represent()  # actualisation graphique du plateau
                pygame.display.update()
                playsound(sound_take_road, block=True)
                return True

            return False #on retourne False seulement quand tout le reste n'a pas retourner True

class Board():
    """
        Classe qui définit le plateau de jeu avec ses pioches et ses composantes graphiques.

        Auteur : NOEL Océan

        :param destination_pile: Pioche de cartes destination.
        :type destination_pile: Object Draw_pile
        :param wagon_pile: Pioche de cartes wagon.
        :type wagon_pile: Object Draw_pile
        :param roads: Liste des routes du plateau.
        :type roads: list
        :param buttons: Liste des bouttons à ajouter du plateau.
        :type buttons: list
        :param display_surface: Surface du plateau.
        :type display_surface: pygame Surface
        :param image: Chemin de l'image du plateau.
        :type image: string
    """

    def __init__(self,destination_pile,wagon_pile,roads,buttons,display_surface,image = 'Resources/Map.png'):
        """
            Initialisation du plateau avec ses pioches et composants.

            Auteur : NOEL Océan
        """
        self.destination_pile = destination_pile
        self.wagon_pile = wagon_pile
        self.roads = roads
        self.buttons = buttons
        self.display_surface = display_surface
        self.image = image


    def represent(self):
        """
            Permet de representer graphiquement le plateau avec ses pioches, ses routes et ses composants.

            Auteur : NOEL Océan
        """
        #Affichage plateau
        image = pygame.image.load('Resources/Map.png')
        image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        self.display_surface.blit(image, (0, 0))

        #Affichage pioches
        self.destination_pile.represent()
        self.wagon_pile.represent()

        #Affichage des cartes visibles
        for i in range(5):
            self.wagon_pile.cards[i].represent()

        #Affichage routes
        for road in self.roads:
            road.represent()

        #Affichage des boutons
        for button in self.buttons:
            button.represent()

class Road():
    """
        Classe qui définit une route du plateau avec ses emplacements.

        Auteur : NOEL Océan

        :param cities: Villes reliées par la route.
        :type cities: tuple (string,string)
        :param color: Couleur de la route.
        :type color: string
        :param player: Joueur de la partie.
        :type player: Object Player
        :param sites: Liste des emplacements de la route.
        :type sites: numpy Array
    """


    def __init__(self,cities,color,player = "",sites = np.array([])):
        """
            Initialise une route qui relie les deux villes données en paramètre.

            Auteur : NOEL Océan
        """
        self.cities = cities
        self.sites = sites
        self.taken = False #booléen pour savoir si la route est prise ou pas (change ca méthode de représentation en conséquence)
        self.taken_by = "" #indique qui de l'IA ou du joueur detient cette route
        self.color = color
        self.player = player

    def represent(self):
        """
            Represente graphiquement la route et représentant ses emplacements.

            Auteur : NOEL Océan
        """
        for site in self.sites :
            site.represent()

class Button(Graphic_area):
    """
        Classe qui définit les boutons d'affichage ou ceux avec lesquelles pourront intéragir le joeur.

        Auteur : NOEL Océan

        :param position: Position associée au bouton en pourcentage.
        :type position: tuple (int,int)
        :param scale: Taille associée au bouton en pourcentage.
        :type scale: float
        :param image: Chemin de l'image associé au bouton.
        :type image: string
        :param image2: Chemin de la deuxième image associée au bouton.
        :type image2: string
        :param texte: Texte associée au bouton.
        :type texte: string
        :param color: Indique la couleur du bouton (Aucun impact graphique, ce paramètre sert d'identifiant).
        :type color: string
        :param convert: Défini si il faut convertir l'image en jpeg pour rendre le bouton transparent au passage de la souris.
        :type convert: bool
        :param center: Indique si le bouton doit être centré par rapport à sa position ou non (par défaut la position correspond au coin supérieur gauche).
        :type center: bool
        :param player: Joueur de la partie.
        :type player: Object Player
    """
    def __init__(self,position,scale = 1.0,image = "Resources/default_button.png",image2 = "",texte = "",color="None",convert = False,center = False, player = ""):

        self.color = color
        self.free = True #pour savoir si l'emplacement est libre
        super().__init__(position, scale, image, image2, convert, center,texte)
        self.player = player

    def mouse_click(self):
        """
            Action à éxecuter en cas de clique sur le bouton.
            Méthode uniquement utilisée pour le bouton qui permet d'ouvrir une pop_up pour que le joueur visualise ses cartes destinations

            Auteur : NOEL Océan
        """
        if self.player != "":
            playsound(sound_card_shuffle, block=False)
            texte = "Vos cartes destinations :"
            objects = self.player.destination_cards
            pop_up(texte, objects=objects, button=Button((0, 0)),choices = False,allow_return = True)

class Wagon(Graphic_area):
    """
        Classe qui définit les wagons qui sont des emplacements de route.

        Auteur : NOEL Océan

        :param position: Position associée à l'emplacement en pourcentage.
        :type position: tuple (int,int)
        :param sens: Sens associée à l'emplacement en degrés.
        :type sens: float
        :param road: Route à laquelle appartient cet emplacement.
        :type road: Object Road
        :param scale: Taille associée à l'emplacement en pourcentage.
        :type scale: float
        :param convert: Défini si il faut convertir l'image en jpeg pour rendre l'emplacement transparent au passage de la souris.
        :type convert: bool
        :param center: Indique si l'emplacement doit être centré par rapport à sa position ou non (par défaut la position correspond au coin supérieur gauche).
        :type center: bool
    """
    selected = 0 #permet d'éviter qu'on puisse cliquer sur 2 wagons ou routes en même temps

    def __init__(self, position, sens, road, scale = 1.0, convert = True,center = False):
        """
           Initialisation d'un emplacement de wagon et ajout de l'emplacement à la liste des emplacements de sa route.

           Auteur : NOEL Océan
       """
        self.taken = False
        self.road = road
        self.color = road.color
        image = "Resources/Wagon_" + self.color + ".png" #valeur par défaut
        super().__init__(position, scale, image, sens=sens, convert=convert, center=center)
        self.image.set_alpha(255)
        self.road.sites = np.append(road.sites, [self])

    def place_wagon(self,type):
        """
              Place un wagon sur l'emplacement lorsque cet emplacement est pris par un joueur.

              :param type: Définit si c'est le joueur ou l'IA qui prend possesion de cet emplacement.
              :type type: string

              Auteur : NOEL Océan
          """
        if type == "player" :
            self.path = "Resources/Wagon_"+self.color+"_2.png"
            self.road.taken_by = "player"
        elif type == "IA" :
            self.path = "Resources/Wagon_" + self.color + "_3.png"
            self.road.taken_by = "IA"
        self.represent()
        self.taken = True

    def represent(self):
        """
            Représente graphiquement l'emplacement sur le plateau.

            Auteur : NOEL Océan
        """

        if self.path != "Resources/Wagon_"+self.color+".png" and self.taken == False:
            self.image = pygame.image.load(self.path)
            perso_heigth = pygame.display.Info().current_h * self.scale
            self.image = pygame.transform.scale(self.image, (int(perso_heigth * self.reso), int(perso_heigth)))
            self.image = pygame.transform.rotate(self.image, self.sens)
        #Affichage
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.image, (self.x, self.y))

    def mouse_click(self):
        """
            Action à éxecuter en cas de clique sur l'emplacement par la souris.
            Appel la méthode de prise de route du joueur.

            Auteur : NOEL Océan
        """
        if Wagon.selected == 1 : #permet d'eviter que le joueur puisse clique sur plusieurs emplacements en même temps
            self.road.player.take_route(self.road)

    def mouse_pass(self,statut):
        """
            Action à éxecuter en cas de survol de l'emplacement par la souris.
            Tout les emplacements qui sont dans la même route que celui-ci sont mis en transparence.

            :param statut: Détermine si la souris vient de rentrer dans la zone ou si elle en est sorti.
            :type statut: bool

            Auteur : NOEL Océan
        """

        if statut == True :
            Wagon.selected += 1
            if self.taken == False:
                playsound(sound_mouse_pass, block=False)
                for wagon in self.road.sites:
                    wagon.image.set_alpha(100)
        else:
            Wagon.selected -= 1
            if self.taken == False:
                for wagon in self.road.sites:
                    wagon.image.set_alpha(255)
        pygame.display.update()

class Boutton():
    """
        Classe spécifique pour définir les boutons du menu.

        Auteur : LEVRIER-MUSSAT Gautier

        :param image: image associée au bouton.
        :type image: pygame Surface
        :param pos: Position en pixel du boutton.
        :type pos: tuple (int,int)
        :param text_input: Texte du bouton.
        :type text_input: string
        :param font: Police du texte bouton.
        :type font: pygame font
        :param base_color: Couleur initiale du bouton.
        :type base_color: tuple (int,int,int)
        :param hovering_color: Couleur du bouton lorsque la souris passe au-dessus.
        :type hovering_color: tuple (int,int,int)
    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
            Mise à jour graphique du bouton.

            :param screen: Surface active actuel de pygame.
            :type screen: pygame Surface

            Auteur : LEVRIER-MUSSAT Gautier
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
            Renvoie vrai si la souris est sur le bouton.

            :param position: position de la souris en pixels.
            :type position: tuple (int,int)

            :return: Vrai si la souris est sur le bouton, Faux sinon.
            :rtype: bool

            Auteur : LEVRIER-MUSSAT Gautier
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
            Change la couleur du bouton si la souris est dessus.

            :param position: position de la souris en pixels.
            :type position: tuple (int,int)

            Auteur : LEVRIER-MUSSAT Gautier
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

