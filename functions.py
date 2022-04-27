import numpy as np
import pygame

def player_wagon_cards(player):
    """
    Fonction qui doit parcourir les cartes du joueur et renvoyer sous forme de dictionnaire combien il à de cartes pour chaque couleur de wagon
    Penser à utiliser uniquement la liste de ses cartes wagons
    Penser à bien garder le même orde des couleurs que dans la class player pour le return
    """
    return {"rose": 1, "blanc": 2, "bleu": 3, "jaune": 4, "orange": 5, "noir": 6, "rouge": 7, "vert": 8, "tout": 9}

def check_real_roads(player,new_road):
    """
    Fonction qui doit mettre à jour les villes reliées par l'utilisateur à chaque fois qu'il prend une route
    par exemple :
    si il avait déjà relié "ville1" à "ville2"
    et qu'il vient de relié "ville2" à "ville3"
    alors on ajoute à player.linked_cities : ("ville1","ville3") (pas sous forme d'objet route)
    """
    pass

def pop_up(texte,button,objects = np.array([])):
    #affiche une fenetre pop up avec un message et la liste des objets étaler grace à leur .represent à des positions différentes
    #attend que l'utilisateur clique sur les objets étalers puis return l'objet choisi
    #penser à changer le status du joueur quand j'utilise ca pour que les objets ne soit pas cliquable comme d'habitude, ils doivent se renvoyer eux-mêmes à la place.

    # initialisation de la zone d'affichage
    image = ""
    if button.image2 != "" : #si on veut une pop_up avec une image de fond particulière
        image = pygame.image.load(button.image2)
    else:
        image = pygame.image.load("Resources\pop_up.png")
    display_surface = pygame.display.get_surface()
    # Taille de l'affichage (dépend de la taille du texte et des objets)
    #////ajout petit calcul en prenant hauteur premier objet et nombre de saut de ligne du texte
    perso_heigth = 400 #hauteur variable en fonction du message
    perso_widht = 800 #largeur fixe
    image = pygame.transform.scale(image, (perso_widht, int(perso_heigth)))
    # Centrage de la la position de la fenetre
    x = int(0.5 * pygame.display.Info().current_w)
    y = int(0.5 * pygame.display.Info().current_h)
    x, y = (int(x - image.get_width() / 2), int(y - image.get_height() / 2))

    # initialisation du texte
    police = pygame.font.SysFont("Monospace", 30, bold=True)
    texte = police.render(texte, 1, (0, 0, 0))

    end = False

    while end == False:

        if len(objects) != 0 :#si on affiche une fenetre avec des objets on représente le texte et les objets
            #Affichage du fond
            display_surface.blit(image, (x, y))

            #Affichage du texte en haut au centre de la fenetre
            display_surface.blit(texte, (int(x + (image.get_width() / 2) - (texte.get_width() / 2)),y + 10))

            #Affichage des éléments/Objets
            pass

        else : #sinon si on est dans le cas ou on affiche simplement l'image de fond à l'utilisateur
            # Affichage du fond
            display_surface.blit(image, (x, y))

        #condition d'arret pour fermer la pop-up : l'utilisateur choisi un objet, ou l'utilisateur retire sa souris du boutton dans le cas d'un boutton qui affiche juste une image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                if button.position != (0,0): #on vérifie qu'on a bien un boutton en paramètre
                    center = (button.x + button.image.get_width() / 2, button.y + button.image.get_height() / 2)
                    if abs(event.pos[0]-center[0]) > button.image.get_width()/2 or abs(event.pos[1] - center[1]) > button.image.get_height()/2 : #on vérifie que l'utilisateur n'est plus sur le bouton
                        end = True
            if event.type == pygame.MOUSEBUTTONUP:
                #vérifier si il choisi un objet,
                pass

        pygame.display.update()

def check_all_event(event,objects):
    """
        Vérifie si l'utilisateur place sa souris sur les zone ou clique sur les zones des objets mis en paramètre

        Paramètres :
            event(Object Pygame.event)
                Action réalisée par l'utilisateur à analyser.

            object(numpy.Array(Object))
                Objets pour lesquelles on veut vérifier si il y a une intéraction avec la souris
    """
    for object in objects :
        object.check_event(event)

def Update_Objects(player,board): #ajouter paramètre "IA"
    #fonction qui update tout les objets graphique à mettre à jour régulièrement
    #Update des nombres de wagons et de crédits du joueur et de l'IA
    #...
    #Update des boutons indiquant le nombre de cartes wagons du joueur
    i = 0
    colors = player_wagon_cards(player)
    for color in colors :
        board.buttons[i].texte = str(colors[color]) #indice doit correspondre aux boutons dans le même ordre
        i+=1

    #mise à jour des boutons qui affichent du texte, respecter ordre
    board.buttons[i].texte = '0'
    i += 1
    board.buttons[i].texte = '0'
    i += 1
    board.buttons[i].texte = '0'
    i += 1
    board.buttons[i].texte = '0'
    i += 1
    board.buttons[i].texte = '0'

def show_visible_wagon(pioche):

    pioche.cards[0].position = (0.94, 0.15)
    pioche.cards[1].position = (0.83, 0.15)
    pioche.cards[2].position = (0.83, 0.29)
    pioche.cards[3].position = (0.94, 0.29)
    pioche.cards[4].position = (0.94, 0.42)

    for i in range(5):
        pioche.cards[i].center = True
        pioche.cards[i].scale = 0.11

    for i in range(5):
        pioche.cards[i].represent()


#/////POUBELLE/////
def delete_cards(player,color,amount,pioche): #déjà fait en tant que méthode ?
    """
        Défausse un nombre de cartes de couleur donnés de la main du joueur.

        Parmètres :
            player(Object.Player)
                Joueur à qui on retire les cartes.

            color(string)
                Couleur des cartes à lui retirer.

            amount(int)
                Nombre de cartes à défausser.

            pioche(Object.Draw_pile)
                Pioche dans laquelle défausser les cartes.
    """
    deleted = 0
    i = 0
    while deleted != amount :
        card = player.wagon_cards.cards[i]
        if card.color == color:
            player.wagon_cards.draw(1,pioche,i-deleted)
            deleted += 1
    i += 1