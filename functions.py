import numpy as np
import pygame
from itertools import combinations
from datetime import datetime
import sys
import dijkstra as dj

def message(texte,button):
    button.texte = texte
    button.represent()

def pop_up(texte,button,objects = np.array([]),choices=True,allow_return = True):
    #affiche une fenetre pop up avec un message et la liste des objets étaler grace à leur .represent à des positions différentes
    #attend que l'utilisateur clique sur les objets étalers puis return l'objet choisi
    #penser à changer le status du joueur quand j'utilise ca pour que les objets ne soit pas cliquable comme d'habitude, ils doivent se renvoyer eux-mêmes à la place.
    # initialisation de la zone d'affichage
    image = ""
    decalage = pygame.display.Info().current_h/3 #initialisation d'un décalage pour les fenetre de cartes destination qui ne doivent pas recouvrir la carte (en pixels)
    decalage_prop = decalage/pygame.display.Info().current_h
    if button.image2 != "" : #si on veut une pop_up avec une image de fond particulière
        image = pygame.image.load(button.image2)
    else:
        image = pygame.image.load("Resources/pop_up.png")
    display_surface = pygame.display.get_surface()
    # Taille de l'affichage (dépend de la taille du texte et des objets)
    perso_heigth = int(pygame.display.Info().current_h/2.325)
    perso_widht = int(pygame.display.Info().current_w/2.078)
    positions = []
    if len(objects) == 2 :
        perso_heigth = int(pygame.display.Info().current_h/2.735)  # hauteur variable en fonction du message
        if objects[0].type == "destination" :
            positions = [(0.45, 0.5+decalage_prop), (0.55, 0.5+decalage_prop)]
        else :
            positions = [(0.45, 0.5), (0.55, 0.5)]
    elif len(objects) >0 and len(objects)<=3:
        perso_heigth = int(pygame.display.Info().current_h/2.735)  # hauteur variable en fonction du message
        if objects[0].type == "destination" :
            positions = [(0.5, 0.5+decalage_prop), (0.4, 0.5+decalage_prop), (0.6, 0.5+decalage_prop)]
        else :
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

    if len(objects) != 0 and objects[0].type == "destination" and len(objects) <= 3: #si on doit afficher moins de 3 cartes destinations, alors on les affichent plus bas que la carte
        y += decalage

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
        image2 = pygame.image.load("Resources/quit.png")
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

def Update_Objects(player,IA,board): #ajouter paramètre "IA"
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
    if IA != "": #car on peut appeler la fonction sans lui demander de mettre à jour les valeurs d'IA
        board.buttons[i].texte = str(IA.wagons)
    i += 1
    board.buttons[i].texte = str(player.points)
    i+=1
    if IA != "": #car on peut appeler la fonction sans lui demander de mettre à jour les valeurs d'IA
        board.buttons[i].texte = str(IA.points)

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

def add_road(linked_cities,road):
    link_found = 0 #stock le nombre de suite de villes auquelle on a ajouté des nouvelles villes
    first_link_found_index = 0
    for links in linked_cities :
        if link_found == 0 : #seulement si on avait pas trouvé de liens avant
            if road.cities[0] in links and road.cities[1] not in links: #on ajout l'autre composant a la liaison de villes si il n'est pas déjà dedans
                link_found += 1
                links.append(road.cities[1])
                first_link_found_index = linked_cities.index(links) #on récupère l'indice de la première liaison dans laquelle on a ajouté la nouvelle route
            elif road.cities[1] in links and road.cities[0] not in links:
                link_found += 1
                links.append(road.cities[0])
                first_link_found_index = linked_cities.index(links)
            elif road.cities[1] in links and road.cities[0] in links : #si les deux sont dedans on ne fais rien
                link_found += 1
                first_link_found_index = linked_cities.index(links)
        else : #sinon si on avait trouvé des liens avant, on fusionnera toutes les autres liaisons qui ont aussi un lien
            if road.cities[0] in links and road.cities[1] not in links:
                linked_cities[first_link_found_index] = linked_cities[first_link_found_index] + links
                linked_cities.remove(links)
                linked_cities[first_link_found_index].remove(road.cities[0]) #suppression du doublon car il est dans les deux liste déjà
            elif road.cities[1] in links and road.cities[0] not in links:
                linked_cities[first_link_found_index] = linked_cities[first_link_found_index] + links
                linked_cities.remove(links)
                linked_cities[first_link_found_index].remove(road.cities[1])
            elif road.cities[1] in links and road.cities[0] in links :
                linked_cities[first_link_found_index] = linked_cities[first_link_found_index] + links
                linked_cities.remove(links)
                linked_cities[first_link_found_index].remove(road.cities[0])
                linked_cities[first_link_found_index].remove(road.cities[1])

    if link_found == 0: #si aucun lien n'a pu être fait, on créer une nouvelle liaison
        linked_cities.append([road.cities[0],road.cities[1]])

def check_destinis(linked_cities,destination_cards,ckeck_or_addpoints = True):
    all_combinaisons = [] #stockage de toutes les combinaisons de villes que le joueur à réussi à avoir
    for links in linked_cities:
        all_combinaisons += list(combinations(links,2))
    all_combinaisons2 = []
    for combinaison in all_combinaisons :
        all_combinaisons2.append((combinaison[1],combinaison[0]))
    all_combinaisons = all_combinaisons+all_combinaisons2
    total_points = 0
    for card in destination_cards :
        if card.destination in all_combinaisons:
            if ckeck_or_addpoints == False : #si on veut juste mettre à jour l'aspect des cartes destinations du joueur
                card.image = pygame.image.load(card.path[:-4]+"_ok"+".png")
                card.ok = True
                card.changed = True
            else :
                total_points += card.points
        else :
            if ckeck_or_addpoints == True: #pas besoin de changer l'aspect des cartes ici
                total_points -= card.points
    return total_points

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"Resources/fontCorona.ttf", size)

def show_final_score(player,ia,level,FINAL_SCORE_MENU):
    f = open("Resources/logs/Results_game.txt",'a')
    f.write("/n"+str(datetime.now().date())+" ; "+str(datetime.now().time())[0:5]+" ; "+level+" : " +str(player.points)+' , '+str(ia.points))
    f.close()
    window = pygame.display.get_surface()
    ecart = int(pygame.display.Info().current_h / 10)
    end = False
    while not end:
        FINAL_SCORE_MOUSE_POS = pygame.mouse.get_pos()
        window.fill((255, 255, 255))

        FINAL_SCORES_TEXT = get_font(60).render("RESULTAT DE LA PARTIE", True, (193, 43, 28))
        FINAL_SCORES_RECT = FINAL_SCORES_TEXT.get_rect(center=(int(window.get_width()/2),int(window.get_height()/ 2- ecart)))
        window.blit(FINAL_SCORES_TEXT, FINAL_SCORES_RECT)

        if player.points >= ia.points :
            FINAL_SCORES_TEXT = get_font(45).render("Victoire "+str(player.points)+" à "+str(ia.points)+" points", True, (193, 43, 28))
            FINAL_SCORES_RECT = FINAL_SCORES_TEXT.get_rect(center=(int(window.get_width()/2 ),int(window.get_height()/ 2)))
            window.blit(FINAL_SCORES_TEXT, FINAL_SCORES_RECT)

        else:
            FINAL_SCORES_TEXT = get_font(45).render("Defaite "+str(player.points)+" à "+str(ia.points)+" points", True,(193, 43, 28))
            FINAL_SCORES_RECT = FINAL_SCORES_TEXT.get_rect(center=(int(window.get_width()/2 ),int(window.get_height()/ 2)))
            window.blit(FINAL_SCORES_TEXT, FINAL_SCORES_RECT)

        FINAL_SCORE_MENU.changeColor(FINAL_SCORE_MOUSE_POS)
        FINAL_SCORE_MENU.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FINAL_SCORE_MENU.checkForInput(FINAL_SCORE_MOUSE_POS):
                    end = True
        pygame.display.update()

def destination_cards_f():
    f = open("Resources/logs/Destination.txt", 'r')
    ligne = f.readlines()
    f.close()
    ligne = [c.strip().split(';') for c in ligne]
    return ligne

def intelligent_choice(roads,IA):
    #On génère le graphe qui modélise les difficultés de chaque chemins pour l'IA en fonction de ces cartes
    Map = create_graphe(roads,IA)

    #ensuite on choisi de se concentrer sur la carte destination qui a le chemin le plus facile à faire
    difficulty = [] #liste qui stocke les différentes difficultées des cartes destinations
    print("Carte destinations possibles : ")
    for destini_card in IA.destination_cards :
        if destini_card.ok == False:  # la carte est intéressante seulement si elle est pas déjà faites
            dijkstra = dj.DijkstraSPF(Map, destini_card.destination[0]) #création d'un graphe partant de la première ville de la carte destination
            distance = dijkstra.get_distance(destini_card.destination[1]) #calcul de la distance la plus courte jusqu'à la deuxième ville de la carte
            print(str(destini_card.destination) + " Difficulté : "+str(distance)+" Chemin : "+ str(dijkstra.get_path(destini_card.destination[1])))
            difficulty.append(distance) #ajout de cette distance à la liste difficulté
        else :
            difficulty.append(999)

    pos = difficulty.index(min(difficulty))#recupération de la position de la carte la plus simple à accomplir
    print("Carte destination Choisie : "+str(IA.destination_cards[pos].destination)+" "+str(difficulty[pos]))

    if difficulty[pos] <= 100 : #on donne à l'IA la carte destination la plus simple à réaliser seulement si elle est pas impraticable
        dijkstra = dj.DijkstraSPF(Map, IA.destination_cards[pos].destination[0])
        path = dijkstra.get_path(IA.destination_cards[pos].destination[1])#on récupère le chemin le plus court pour relier les villes de la carte
        print("Chemin : ",path)
        return get_roads(path,roads) #on renvoie les routes à prendre qui permettent de réaliser l'objectif rapidement
    else : #sinon l'IA doit repiocher de nouvelles carte destination
        return [] #on renvoie aucune routes

def intelligent_draw(roads,pioche,no_joker = False):
    """pour choix carte, prendre que les couleurs des routes qui permettent de faire un objectif,
            ou des jokers (si pas de couleurs bien trouvée); faire un orde de priorité des routes,
            comme ca on cherche toujours a finir une route en priorité et si y'a pas la couleur dan sla pioche,
            on tente avec deuxième route prio, puis joker si rien, et finalement pioche carte non visible si pas joker"""

    color_needed = []
    for road in roads :
        if road.color != "tout" and road.taken == False : #on ajoute pas la couleur joker comme une couleur souhaitée car on ne veut pas piocher des joker en priorité (care coute le prix de 2 cartes)
            color_needed.append(road.color) #on ajoute les couleurs recherchées dans une liste

    print("Searching for colors : ", color_needed)

    #on regarde chaque cartes de la pioche
    for i in range(5):
        if pioche.cards[i].color in color_needed:
            return i #on pioche cette carte

    #si aucune des couleure souhaitées sont dans la pioche visible, on pioche une joker (seulement si on est au premier tour)
    for i in range(5):
        if pioche.cards[i].color == "tout" and no_joker == False:
            return i #on pioche cette carte

    #et si il n'y a pas de joker non plus, on pioche une carte cachée
    return 5

def create_graphe(roads,IA):

    #création d'un graphe
    Map = dj.Graph()
    #Création des liaisons
    for road in roads :
        value = len(road.sites)
        if road.color == "tout":
            value -= 1 #on favorise les liaisons joker
        if road.taken == True and road.taken_by == "player" : #si la route est déjà prise par le joueur, on rend le chemin impraticable pour le graph
            value += 999
        elif road.taken == True and road.taken_by == "IA" : #sinon si la route est déjà prise, mais par l'IA, alors elle compte pour aucune difficulté
            value = 0
        Map.add_edge(road.cities[0],road.cities[1],value)
        Map.add_edge(road.cities[1], road.cities[0], value) #ajout dans les deux sens pour avoir un graphe non orienté
    return Map

def get_roads(path,roads):

    #extraire les routes nécessaire pour réaliser le chemin voulu
    road_needed = []
    for i in range(len(path)-1) : #extraction des routes a utiliser donc des couples de villes concernés
        cities = (path[i],path[i+1]) #couple de villes dans un sens
        cities_t = (path[i+1],path[i]) #couple de villes dans l'autre sens
        for road in roads: #on trouve les routes associées aux couples
            if (cities == road.cities or cities_t == road.cities) and road.taken == False :
                road_needed.append(road)

    return road_needed

#/////POUBELLE/////