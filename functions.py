import numpy as np
import pygame

def check_real_roads(player,new_road):
    """
    Fonction qui doit mettre à jour les villes reliées par l'utilisateur à chaque fois qu'il prend une route
    par exemple :
    si il avait déjà relié "ville1" à "ville2"
    et qu'il vient de relié "ville2" à "ville3"
    alors on ajoute à player.linked_cities : ("ville1","ville3") (pas sous forme d'objet route)
    """
    pass

def pop_up(texte,button,objects = np.array([]),choices=True,allow_return = True):
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
    perso_heigth = int(pygame.display.Info().current_h/2.325)
    perso_widht = int(pygame.display.Info().current_w/2.078)
    positions = []
    if len(objects) == 2 :
        perso_heigth = int(pygame.display.Info().current_h/2.735)  # hauteur variable en fonction du message
        positions = [(0.45, 0.5), (0.55, 0.5)]
    elif len(objects) >0 and len(objects)<=3:
        perso_heigth = int(pygame.display.Info().current_h/2.735)  # hauteur variable en fonction du message
        positions = [(0.5, 0.5), (0.4, 0.5), (0.6, 0.5)]
    elif len(objects) >3 and len(objects)<=6:
        perso_heigth = int(pygame.display.Info().current_h/1.631)
        positions = [(0.4, 0.36), (0.5, 0.36),(0.6, 0.36),
                     (0.4, 0.59), (0.5, 0.59), (0.6, 0.59)]
    elif len(objects) >6 and len(objects)<=9:
        perso_heigth = int(pygame.display.Info().current_h/1.162) # hauteur variable en fonction du message
        positions = [(0.4, 0.23), (0.5, 0.23), (0.6, 0.23),
                     (0.4, 0.46), (0.5, 0.46), (0.6, 0.46),
                     (0.4, 0.69), (0.5, 0.69), (0.6, 0.69)]
    elif len(objects) > 9 :
        print("Trop d'objets a afficher")
        objects = objects[0:9] #securiter pour pas dépasser en indices
        perso_heigth = int(pygame.display.Info().current_h/1.162) # hauteur variable en fonction du message
        positions = [(0.4, 0.23), (0.5, 0.23), (0.6, 0.23),
                     (0.4, 0.46), (0.5, 0.46), (0.6, 0.46),
                     (0.4, 0.69), (0.5, 0.69), (0.6, 0.69)]

    image = pygame.transform.scale(image, (perso_widht, int(perso_heigth)))

    # Centrage de la la position de la fenetre
    x = int(0.5 * pygame.display.Info().current_w)
    y = int(0.5 * pygame.display.Info().current_h)
    x, y = (int(x - image.get_width() / 2), int(y - image.get_height() / 2))

    # initialisation du texte
    l = int(pygame.display.Info().current_h/32.6)
    police = pygame.font.SysFont("Monospace", l, bold=True)
    texte2 = "" #variable pour gestion 2e ligne
    if len(texte) > 35: #si le texte est trop grand et doit aller sur une deuxième ligne
        texte2 = texte[35:]
        texte = texte[0:35]
        texte = police.render(texte, 1, (0, 0, 0))
        texte2 = police.render(texte2, 1, (0, 0, 0))
    else :
        texte = police.render(texte, 1, (0, 0, 0))



    end = False
    choice = -1

    # Ajout d'un bouton retour si besoin
    image2 = ""
    x2 = 0
    y2 = 0
    statut = False
    if allow_return == True:
        image2 = pygame.image.load("Resources\quit.png")
        image2 = image2.convert()
        h = int(pygame.display.Info().current_h /16)
        image2 = pygame.transform.scale(image2, (int(h*1.49), h))
        x2 = x + int(image2.get_width()/2.4)
        y2 = y

    # initialisation des éléments/Objets si besoin
    if len(objects) != 0:
        if objects[0].type == "wagon" :
            for i in range(len(objects)):
                objects[i].changed = True
                objects[i].position = positions[i]
                objects[i].scale = 0.12
                objects[i].center = True
        else :
            for i in range(len(objects)):
                objects[i].changed = True
                objects[i].position = positions[i]
                objects[i].scale = 0.22
                objects[i].center = True

    #initialisation du cache de fond
    if not (len(objects) !=0 and objects[0].type == "destination") : #on evite que le cache se rajoute plusieurs fois dans le cas du choix des cartes destinations
        cache = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
        cache.set_alpha(128)
        cache.fill((0, 0, 0))
        display_surface.blit(cache, (0, 0))  # affichage du cache transparent

    while end == False:

        if len(objects) != 0 :#si on affiche une fenetre avec des objets on représente le texte et les objets
            #Affichage du fond
            display_surface.blit(image, (x, y))

            #Affichage du texte en haut au centre de la fenetre
            display_surface.blit(texte, (int(x + (image.get_width() / 2) - (texte.get_width() / 2)),y + int(pygame.display.Info().current_h / 80)))

            #Affichage des éléments/Objets
            for object in objects:
                object.represent()

            #Affichage du bouton retour si besoin
            if allow_return == True:
                display_surface.blit(image2, (x2,y2))

        else : #sinon si on est dans le cas ou on affiche simplement l'image de fond à l'utilisateur avec le texte associé
            # Affichage du fond
            display_surface.blit(image, (x, y))

            #Affichage du texte au centre de la fenetre avec 1 ou 2 lignes
            if texte2 != "":  # si on doit afficher une deuxième ligne de texte
                ecart_interligne = int(pygame.display.Info().current_h / 40) #trouvé a taton
                display_surface.blit(texte, (int(x + (image.get_width() / 2) - (texte.get_width() / 2)),int(y + (image.get_height() / 2) - texte.get_height()-ecart_interligne)))
                display_surface.blit(texte2, (int(x + (image.get_width() / 2) - (texte2.get_width() / 2)),int(y + (image.get_height() / 2) - texte2.get_height()+ecart_interligne)))
            else:
                display_surface.blit(texte, (int(x + (image.get_width() / 2) - (texte.get_width() / 2)),int(y + (image.get_height() / 2) - texte.get_height())))

            #Affichage du bouton retour si besoin
            if allow_return == True:
                display_surface.blit(image2, (x2,y2))

        #condition d'arret pour fermer la pop-up : l'utilisateur choisi un objet, ou l'utilisateur retire sa souris du boutton dans le cas d'un boutton qui affiche juste une image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                if button.position != (0,0): #on vérifie qu'on a bien un boutton en paramètre, on agir que si c'est pas un bouton en (0,0) indiquant qu'il ne faut pas faire d'action
                    center = (button.x + button.image.get_width() / 2, button.y + button.image.get_height() / 2)
                    if abs(event.pos[0]-center[0]) > button.image.get_width()/2 or abs(event.pos[1] - center[1]) > button.image.get_height()/2 : #on vérifie que l'utilisateur n'est plus sur le bouton
                        end = True

                if allow_return == True: #verification passage de la souris sur le bouton return
                    check = get_pass_and_click(x2,y2,image2,event)
                    if check == "pass":
                        if statut == False:
                            image2.set_alpha(100)
                            statut = True
                    else:
                        if statut == True:
                            image2.set_alpha(255)
                            statut = False

                if choices == True: #vérification passage de la souris dessus
                    check_all_event(event, objects)

            if event.type == pygame.MOUSEBUTTONUP:
                #vérifier si il choisi un objet ou si il fait retour
                if allow_return == True: #verification retour
                    check = get_pass_and_click(x2,y2,image2,event)
                    if check == "click":
                        choice = -1
                        return choice

                # Possibilité de choisir un des objets si besoin
                if choices == True:
                    check_all_event(event, objects)
                    for obj in objects:
                        #vérification de passage sur un des objet
                        check = get_pass_and_click(obj.x,obj.y,obj.image,event)
                        #renvoie du choix pour la carte sur laquelle le joueur clique
                        if check == "click":
                            choice = 0  # indique qu'un choix à été fait
                            return obj #on renvoie l'objet

        pygame.display.update()

    return choice

def get_pass_and_click(x,y,surface,event):
    center = (x+int(surface.get_width() / 2), y+int(surface.get_height() / 2))  # position centrale de l'object
    if event.type == pygame.MOUSEMOTION:
        if abs(event.pos[0] - center[0]) <= surface.get_width() / 2 and abs(event.pos[1] - center[1]) <= surface.get_height() / 2:
            return "pass"
    if event.type == pygame.MOUSEBUTTONUP:
        if abs(event.pos[0] - center[0]) <= surface.get_width() / 2 and abs(event.pos[1] - center[1]) <= surface.get_height() / 2:
            return "click"

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
    colors = player.cards_number
    for color in colors :
        board.buttons[i].texte = str(colors[color]) #indice doit correspondre aux boutons dans le même ordre
        i+=1

    #mise à jour des boutons qui affichent du texte, respecter ordre
    board.buttons[i].texte = str(player.draw_credit)
    i += 1
    board.buttons[i].texte = str(player.wagons)
    i += 1
    board.buttons[i].texte = '0'
    i += 1
    board.buttons[i].texte = '45'

def show_visible_wagon(player,pioche,liste):

    #attribution des paramètres nécessaires aux cartes visibles pour l'intéraction avec l'utilisateur
    pioche.cards[0].position = (0.83, 0.16)
    pioche.cards[1].position = (0.935, 0.16)
    pioche.cards[2].position = (0.83, 0.29)
    pioche.cards[3].position = (0.935, 0.29)
    pioche.cards[4].position = (0.935, 0.42)

    pioche.cards[0].indice = 0
    pioche.cards[1].indice = 1
    pioche.cards[2].indice = 2
    pioche.cards[3].indice = 3
    pioche.cards[4].indice = 4

    pioche.cards[0].player = player
    pioche.cards[1].player = player
    pioche.cards[2].player = player
    pioche.cards[3].player = player
    pioche.cards[4].player = player

    pioche.cards[0].pioche = pioche
    pioche.cards[1].pioche = pioche
    pioche.cards[2].pioche = pioche
    pioche.cards[3].pioche = pioche
    pioche.cards[4].pioche = pioche

    for i in range(5):
        pioche.cards[i].center = True
        pioche.cards[i].scale = 0.13

    #mise à jour de la liste d'objet interactif

    for i in range(5):
        liste.pop(-1)
    for i in range(5):
        liste.append(pioche.cards[i])
        pioche.cards[i].changed = True


#/////POUBELLE/////