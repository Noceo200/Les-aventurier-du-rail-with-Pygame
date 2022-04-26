import copy
from functions import *
import pygame

class Graphic_area():

    def __init__(self,position,scale,image,image2 = "",convert = False,center = False,texte = ""):

        self.position = position
        self.path = image
        self.image = pygame.image.load(self.path) #chargement de l'image
        self.image2 = image2
        self.scale = scale
        self.passed = False #variable pour gestion evennements
        self.texte = texte #texte à mettre sur l'image
        self.center = center

        #Conversion en jpeg de l'image si nécessaire
        if convert == True:
            self.image= self.image.convert()
        #Determination de la position en pixels
        self.x = int(self.position[0] * pygame.display.Info().current_w)
        self.y = int(self.position[1] * pygame.display.Info().current_h)
        #Mise à l'échelle de l'affichage
        self.reso = self.image.get_width()/self.image.get_height()
        perso_heigth = pygame.display.Info().current_h*self.scale
        self.image = pygame.transform.scale(self.image, (int(perso_heigth*self.reso), int(perso_heigth)))
        # Centrage position
        if self.center == True :
            self.x, self.y = (int(self.x - self.image.get_width() / 2), int(self.y - self.image.get_height() / 2))
        #initialisation zone de texte
        if self.texte != "" and self.path == "Resources\default_button.png": #si le bouton a du texte et n'a pas d'image particulière, alors on affiche le texte sur l'image par defaut (sinon le texte sera afficher lors du passage de la souris sur le boutton)
            police = pygame.font.SysFont("Monospace", 30, bold=True)
            self.texte = police.render(self.texte, 1, (0, 0, 0))

    def represent(self):
        """
            Représente graphiquement la pioche sur le plateau.
        """
        #Affichage
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.image, (self.x, self.y))
        if self.texte != "" and self.path == "Resources\default_button.png": #donc si on a initialiser le texte pour le mettre au dessus de l'image
            display_surface.blit(self.texte, (int(self.x + (self.image.get_width()/2) - (self.texte.get_width()/2)), int(self.y + self.image.get_height()/2 - (self.texte.get_height()/2)))) #on place le texte au centre de l'image

    def check_event(self,event):
        """
            Vérifie si l'utilisateur place sa souris sur la zone ou clique sur la zone

            Paramètres :
                event(Object Pygame.event)
                    Action réalisée par l'utilisateur à analyser.
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
            Action à éxecuter en cas de survol de la zone par la souris

            Paramètres:
                enter(bool)
                    Défini si on rentre ou si on sort de la zone
        """
        if statut == True:
            if self.texte == "" and self.image2 == "": #si on a bouton qui est cliquable, il devient transparent
                self.image.set_alpha(100)
            else :
                pop_up(self.texte,button = self) #sinon, c'est un bouton qui doit afficher une pop up, on l'affiche
        else:
            if self.texte == "" and self.image2 == "":
                self.image.set_alpha(255)

    def mouse_click(self):
        """
            Action à éxecuter en cas de clique dans la zone par la souris
        """
        pass

class Card(Graphic_area):
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
    def __init__(self,type, color = "None", destination = ("None","None"),position = (0,0),scale=1):
        """
            Créer une carte avec le type et la couleur voulu ou la destination voulu.
        """
        image = ""
        if type == "wagon":
            image = "Resources\Card_"+color+".png"
        elif type == "destination":
            image = "Resources\Card_ville0_ville1.png"
        super().__init__(copy.deepcopy(position), scale, image,convert = True)
        self.type = type
        self.color = color
        self.destination = destination

class Draw_pile(Graphic_area):
    """
       Classe qui décrit l'objet paquet de carte
       (Utile pour définir les différentes pioches et mains des joueurs)

       Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

       Paramètres :
            cards(numpy.array)
                array numpy de toutes les cartes qui composent le paquet de carte.

            position(int,int)
                Position graphique en pourcentage, par exemple, (0.5,0.5) place l'objet au milieu.

            scale(float)
                Multiplicateur de taille d'affichage.

            image(string)
                Chemin vers le fichier image qui représente l'objet.
    """
    def __init__(self,cards,position = (0,0),scale = 1,image = "Resources\Default_pioche.png"):
        """
            Créer un paquet de cartes avec les cartes choisis.
        """
        super().__init__(copy.deepcopy(position),scale,image,convert = True)
        self.cards = cards #Donne accès directement à la variable global cards du programme principale

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

class Player():
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
                - indice entre 1 et 5 => Le joueur veut piocher une des 5 cartes wagon face visible
                - indice = 6 => Le joueur veut piocher dans la pioche (cartes face cachées)

            pioche(Object.Draw_pile)
                paquet de cartes qui correspond à la pioche pour les cartes wagon
        """

        if indice == 6 : #si le joueur pioche dans la pioche, il perd juste un crédit, et il ne peut plus piocher de locomotive face visible
            self.draw_credit -= 1 #on retire un crédit
            self.status = "drawing_wagon" #mise à jour du status du joueur
            pioche.draw(1,self.wagon_cards,-indice) #on transfère la carte piocher vers les cartes du joueur
        else :
            if pioche.cards[-indice].color == "tout" and self.draw_credit > 1 : #si c'est une locomotive et que le joueur à le droit de la piocher
                self.draw_credit -= 2  # on retire deux crédits
                pioche.draw(1, self.wagon_cards, -indice)
            elif pioche.cards[-indice].color == "tout" : #sinon si il peut pas piocher la locomotive
                #message("Vous ne pouvez pas piocher une locomotive après avoir piocher une première carte",5) #Affiche du message pendant 5s
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

        self.draw_credit -= 1  # on retire un crédit de pioche
        self.status = "drawing_destination1"  # mise à jour du status du joueur
        pioche.draw(1, self.destination_cards, -indice) #transfère la carte piochée de la pioche vers les cartes du joueur

        #Dans le programme principale le joueur peut de nouveau piocher ou peut arreter

        if self.draw_credit == -1: #le joueur peut piocher jusqu'a 3 cartes destination, son tour se termine donc quand il a -1 credits
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
                                         [self.cards_bar.cards[i] for i in color_possible]).color # propose à l'utilisateur de choisir entre les wagons possibles et renvoie la couleur de la carte choisie
                    verif = True
                elif max(wagons_player.items())+wagons_player["tout"] >= len(road.sites): #si on a pas assez de wagons d'une meme couleur mais qu'on a assez de jokers, on demande quelle couleur utiliser
                    color_possible = []  # on regard entre quelles couleur l'utilisateur à le choix
                    i = 0
                    for key in wagons_player:
                        if wagons_player[key] >= len(road.sites)-wagons_player["tout"]:
                            color_possible = np.append(color_possible,0)  # on ajoute la position de la couleur qu'on peut utiliser
                        i += 1
                    color_chose = pop_up("Vous avez "+str(wagons_player["tout"])+" jokers, "
                                         +"choisissez quels wagons de la même couleur poser, il en faut " + str(len(road.sites)-wagons_player["tout"]),
                                         [self.cards_bar.cards[i] for i in color_possible]).color  #propose à l'utilisateur de choisir entre les wagons possibles et renvoie la couleur de la carte choisie
                    joker_use = len(road.sites) - wagons_player[color_chose] #nombre de joker a utiliser
                    verif = True
                else :
                    pass
                    #message("Vous n'avez pas assez de wagons d'une même couleur, choisissez une autre route ou une autre action",4)
            else : #sinon si c'est une route avec une couleur définie
                if wagons_player[road.color] >= len(road.sites):
                    verif = True
                elif wagons_player[road.color]+ wagons_player["tout"] >= len(road.sites):
                    joker_use = len(road.sites) - wagons_player[color_chose]
                    verif = True
                else :
                    pass
                    #message("Vous n'avez pas assez de wagons "+str(road.color)+", il en faut "+str(len(road.sites)),4)
        elif verif == False :
            pass
            #message("Cette routes est déjà prise",2)

        if verif == True:
            # PRISE DE LA ROUTE
            self.draw_credit -= 2
            self.status = "None"
            self.wagons -= len(road.sites)

            #on défausse les cartes utilisées de son paquet
            """delete_cards(self,color_chose,len(road.sites)-joker_use,pioche)
            delete_cards(self,"tout",joker_use,pioche)"""
            #à envoyer dans pioche défausse de board

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

            buttons(numpy.Array(Object.Button))
                Boutons présents sur le plateau.

            display_surface(Object Pygame.Surface)
                Zone d'affichage du plateau.

            image(string)
                Chemin vers le fichier image qui représente l'objet'.
    """

    def __init__(self,destination_pile,wagon_pile,cities,roads,buttons,display_surface,image = 'Resources\Map.png'):
        """
            Créer un plateau avec les pioches.
        """
        self.destination_pile = destination_pile
        self.wagon_pile = wagon_pile
        self.cities = cities
        self.roads = roads
        self.buttons = buttons
        self.display_surface = display_surface
        self.image = image


    def represent(self):
        """
            Permet de representer graphiquement le plateau avec ses pioches, ses routes et ses villes.
        """
        #Affichage plateau
        image = pygame.image.load('Resources\Map.png')
        image = pygame.transform.scale(image, (pygame.display.Info().current_w, pygame.display.Info().current_h))
        self.display_surface.blit(image, (0, 0))

        #Affichage pioches
        self.destination_pile.represent()
        self.wagon_pile.represent()

        #Affichage villes
        for city in self.cities :
            city.represent()

        #Affichage routes
        for road in self.roads:
            road.represent()

        #Affichage des boutons
        for button in self.buttons:
            button.represent()

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
        self.sites = sites
        self.taken = False #booléen pour savoir si la route est prise ou pas (change ca méthode de représentation en conséquence)
        self.color = color

    def represent(self):
        """
            Permet de representer graphiquement la route.
        """
        for site in self.sites :
            site.represent()

class City(Graphic_area):
    """
       Classe qui décrit une ville.

       Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

       Paramètres :
              name(string)
                Nom pour identifier la ville dans le programme.

              position(int,int)
                Position en pourcentage de la ville, par exemple, (0.5,0.5) place la ville au milieu.

              scale(float)
                Multiplicateur de taille d'affichage.

              image(string)
                Chemin vers le fichier image qui représente la ville.
   """

    def __init__(self,name,position,scale = 1.0,image = "Resources\City.png"):
        """
           Créer une ville avec un nom, son image et sa position.
       """
        super().__init__(copy.deepcopy(position), scale, image)
        self.name = name

class Button(Graphic_area):
    """
        Créer un objet de type boutton qui sera interactif.

        Paramètres :
            position(int,int)
                Position graphique en pourcentage, par exemple, (0.5,0.5) place l'objet au milieu.

            scale(float)
                Multiplicateur de taille d'affichage.

            image(string)
                Chemin vers le fichier image qui représente l'objet.

            texte(string)
                Texte à afficher lorsque la souris passe dessus.

            color(string)
                Couleur de la zone intéractive (Pour les emplacements de wagons).

            convert(Bool)
                Permet de convertir image en jpeg si besoin.

            center(Bool)
                Permet de centrer l'image si besoin.
    """
    def __init__(self,position,scale = 1.0,image = "Resources\default_button.png",image2 = "",texte = "",color="None",convert = False,center = False):

        self.color = color
        self.free = True #pour savoir si l'emplacement est libre
        super().__init__(position, scale, image, image2, convert, center,texte)

class Group():
    #seulement pour partie graphique
    #permet que si joueur clique sur un des emplacement libre sur le plateau, on puisse accéder au groupe d'emplacements qui représente la route en question
    pass

#///////POUBELLE//////////

class Wagon(Graphic_area): #pas besoin car c'est bouton emplacement sui va juste changer d'image
    """
       Classe qui décrit un Wagon.

       Auteurs : NOEL Océan, LEVRIER-MUSSAT Gautier

       Paramètres :
              color(string)
                Couleur du wagon.
   """

    def __init__(self, color, scale = 1.0):
        """
           Créer un wagon.
       """

        position = (0,0)
        image = "Resources\Wagon_bleu_v.png" #valeur par défaut
        super().__init__(copy.deepcopy(position), scale, image)
        self.color = color

    def place_wagon(self,sens,position):
        """
            Place un wagon sur le plateau.

            Paramètres:
                sens(bool)
                    Défini le sens dans lequel représenter le wagon. (True = verticale, False = horizontale)

                position(int,int)
                    Position du wagon à placer.
        """
        if sens == True :
            self.image = "Resources\Wagon_"+self.color+"_v.png"
        else :
            self.image = "Resources\Wagon_"+self.color+"_h.png"

        self.position = position

        self.represent()

        def represent(self):
            """
                Surcharge de la méthode pour représenter un objet.
            """
            # Chargement de la bonne image à chaque fois qu'on appel la méthode
            image = pygame.image.load(self.image)
            # Determination de la position en pixels
            self.x = self.position[0]
            self.y = self.position[1]
            # Mise à l'échelle de l'affichage
            self.reso = image.get_width() / image.get_height()
            # Mise à l'échelle de l'affichage
            perso_heigth = pygame.display.Info().current_h * self.scale
            self.image = pygame.transform.scale(image, (int(perso_heigth * self.reso), int(perso_heigth)))
            # Affichage
            display_surface = pygame.display.get_surface()
            display_surface.blit(self.image, (self.x, self.y))

