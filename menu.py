from objects import *
from pygame import mixer
from importlib import reload

pygame.init()#lancement pygame

SCREEN = pygame.display.set_mode((1280, 720))#definition de l'ecran
pygame.display.set_caption("Menu")

BG = pygame.image.load("Resources/dessinmenu.png")

# Background sound
mixer.music.load("Resources/Songs/l'aventurier.wav") #lancement de la musique
mixer.music.play(-1)
back_ground_music = "Resources/Songs/background_theme.mp3"

first = True #variable pour indiquer premier lancement jeu

def get_font(size):
    """
        Retourne la police voulue, de la taille voulue
        Paramètres :
            size(int):
             Taille de police voulue.
    """
    return pygame.font.Font(r"Resources/fontCorona.ttf", size)

Game = ""

def play():
    """
        Affiche le menu de jeu avec les différents niveaux de difficulté du joueur
        Permet de retourner dans le menu principal
    """
    changed = False
    global SCREEN
    global BG
    global first
    global Game
    while True:
        if changed == True:
            SCREEN = pygame.display.set_mode((1280, 720))#réglage de la taille de l'écran
            pygame.display.set_caption("Menu")#ecriture du nom de la fenetre qui s'ouvre

            BG = pygame.image.load("Resources/dessinmenu.png")

            # Background sound
            mixer.music.load("Resources/Songs/l'aventurier.wav")#chargement de la musique de fond
            mixer.music.play(-1)
            changed = False

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((0, 0, 0))#initialisation de l'ecran avec un fond noir

        PLAY_TEXT = get_font(90).render("Prêt pour la grande aventure ?", True, (255, 255, 255))#Ecriture de texte avec sa taille et sa couleur
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 80))#definition d'un rectangle dans lequel le texte va se situer
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)#affichage du texte dans le rectangle

        PLAY_DEBUTANT = Boutton(image=None, pos=(640, 310),
                          text_input="DEBUTANT", font=get_font(75), base_color=(255, 255, 255), hovering_color=(193, 43, 28))#definition d'un bouton sur lequel on peut apputer qui change de couleur
        PLAY_INTERMEDIAIRE = Boutton(image=None, pos=(640, 400),
                          text_input="INTERMEDIAIRE", font=get_font(75), base_color=(255, 255, 255), hovering_color=(193, 43, 28))
        PLAY_BACK = Boutton(image=None, pos=(640, 580),
                           text_input="RETOUR", font=get_font(75), base_color=(255, 255, 255), hovering_color=(193, 43, 28))

        PLAY_DEBUTANT.changeColor(PLAY_MOUSE_POS)
        PLAY_DEBUTANT.update(SCREEN)
        PLAY_INTERMEDIAIRE.changeColor(PLAY_MOUSE_POS)
        PLAY_INTERMEDIAIRE.update(SCREEN)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:#quitter le menu sans bug dans le shell
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:#si l'on appuie sur du texte cliquable
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):#retour au menu principal
                    main_menu()
                if PLAY_DEBUTANT.checkForInput(PLAY_MOUSE_POS):
                    mixer.music.stop()#couper la musique
                    if first == True:
                        import Game
                        first = False
                    else:
                        reload(Game)
                    # lancement de la music de fond


                    mixer.music.load(back_ground_music)
                    mixer.music.play(-1)
                    Game.game("debutant")
                    changed = True


                if PLAY_INTERMEDIAIRE.checkForInput(PLAY_MOUSE_POS):
                    mixer.music.stop()#couper la musique
                    if first == True:
                        import Game
                        first = False
                    else:
                        reload(Game)
                    # lancement de la music de fond
                    mixer.music.load(back_ground_music)
                    mixer.music.play(-1)#la musique va se repeter à l'infini
                    Game.game("intermediaire")
                    changed = True

        pygame.display.update()


def options():
    """
        Affiche le réglage des paramètre de son dans le menu option
        Permet de retourner dans le menu principal
    """

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((255, 255, 255))

        OPTIONS_TEXT = get_font(45).render("REGLAGES DU JEU", True, (0, 0, 0))
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 80))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Boutton(image=None, pos=(640, 580),
                              text_input="RETOUR", font=get_font(75), base_color=(0, 0, 0), hovering_color=(193, 43, 28))
        OPTIONS_MUSIC_OFF = Boutton(image=None, pos=(640, 260),
                              text_input="COUPER LA MUSIQUE", font=get_font(75), base_color=(0, 0, 0), hovering_color=(193, 43, 28))
        OPTIONS_MUSIC_ON = Boutton(image=None, pos=(640, 380),
                                   text_input="REMETTRE LA MUSIQUE", font=get_font(75), base_color=(0, 0, 0),
                                   hovering_color=(193, 43, 28))

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_MUSIC_OFF.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUSIC_OFF.update(SCREEN)
        OPTIONS_MUSIC_ON.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MUSIC_ON.update(SCREEN)

        for event in pygame.event.get():
            music = 1
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_MUSIC_OFF.checkForInput(OPTIONS_MOUSE_POS):
                    mixer.music.stop()
                    music = 0
                if OPTIONS_MUSIC_ON.checkForInput(OPTIONS_MOUSE_POS):
                    mixer.music.play(-1)

        pygame.display.update()

def rules():
    """
        Affiche une image explicitant les règles du jeu
        Permet de retourner dans le menu principal
    """
    regles1 = pygame.image.load(r'Resources/regles1.png')#chargement d'une image
    regles2 = pygame.image.load(r'Resources/regles2.png')

    while True:
        RULES_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill((189, 196, 200))
        SCREEN.blit(regles1,(110,0))#affichage de la premiere moitie de la photo, positionnee en haut du côté gauche
        SCREEN.blit(regles2, (640, 0))#affichage de la seconde moitié de la photo




        RULES_BACK = Boutton(image=None, pos=(640, 700),
                               text_input="RETOUR", font=get_font(35), base_color=(0, 0, 0),
                               hovering_color=(193, 43, 28))#bouton retour au menu principal
        RULES_BACK.changeColor(RULES_MOUSE_POS)
        RULES_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RULES_BACK.checkForInput(RULES_MOUSE_POS):
                    main_menu()
        pygame.display.update()


def scores():
    """
        Affiche le score des anciennes parties jouées
        Permet de retourner dans le menu principal
    """
    f = open("Resources/logs/Results_game.txt")#lecture du fichier
    lignes = f.readlines()
    f.close()
    lignes = [c.strip() for c in lignes]#stockage du fichier, ligne par ligne



    while True:
        RULES_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill((255, 255, 255))#affichage d'un fond blanc

        SCORES_TEXT = get_font(60).render("HISTORIQUE DES PARTIES", True, (193, 43, 28))
        SCORES_RECT = SCORES_TEXT.get_rect(center=(640, 80))
        SCREEN.blit(SCORES_TEXT, SCORES_RECT)

        SCORES_TEXT = get_font(45).render("DATE | HEURE | NIVEAU IA | POINTS JOUEUR | POINTS IA |", True, (193, 43, 28))
        SCORES_RECT = SCORES_TEXT.get_rect(center=(640, 140))
        SCREEN.blit(SCORES_TEXT, SCORES_RECT)

        if len(lignes)<10:
            for i in range (len(lignes)): #pour n'afficher que les 9 dernièrs résultats de parties
                SCORES_TEXT = get_font(45).render(lignes[len(lignes)-1-i], True, (0, 0, 0))#definition de la taille, couleur et position par rapport au fichier texte
                SCORES_RECT = SCORES_TEXT.get_rect(center=(640, 200+40*i))
                SCREEN.blit(SCORES_TEXT, SCORES_RECT)
        else :
            lignes.pop(0)#retire la partie la plus ancienne jouée
            for i in range (len(lignes)):
                SCORES_TEXT = get_font(45).render(lignes[len(lignes)-1-i], True, (0, 0, 0))
                SCORES_RECT = SCORES_TEXT.get_rect(center=(640, 200+40*i))
                SCREEN.blit(SCORES_TEXT, SCORES_RECT)

        RULES_BACK = Boutton(image=None, pos=(640, 640),
                             text_input="RETOUR", font=get_font(60), base_color=(0, 0, 0),
                             hovering_color=(193, 43, 28))
        RULES_BACK.changeColor(RULES_MOUSE_POS)
        RULES_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RULES_BACK.checkForInput(RULES_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu():
    """
        Affiche le menu principal
        Permet de rejoindre les diférents menus (Play,Rules,Scores,Options)
    """
    while True:
        SCREEN.blit(BG, (0, 0))#affichage de l'image au centre de l'ecran

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(95).render("LES AVENTURIERS DU RAIL", True, (193, 43, 28))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Boutton(image=pygame.image.load("Resources/Play Rect.png"), pos=(640, 250),#definition des différents boutons avec leur taille, couleur et position
                             text_input="JOUER", font=get_font(85), base_color=(255, 255, 255), hovering_color=(193, 43, 28))
        OPTIONS_BUTTON = Boutton(image=pygame.image.load("Resources/Play Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(85), base_color=(255, 255, 255), hovering_color=(193, 43, 28))
        QUIT_BUTTON = Boutton(image=pygame.image.load("Resources/Play Rect.png"), pos=(640, 550),
                             text_input="QUITTER", font=get_font(85), base_color=(255, 255, 255), hovering_color=(193, 43, 28))
        RULES_BUTTON = Boutton(image=None, pos=(1130, 680),
                              text_input="REGLES", font=get_font(35), base_color=(255, 255, 255),
                              hovering_color=(193, 43, 28))
        SCORES_BUTTON = Boutton(image=None, pos=(100, 680),
                               text_input="SCORES", font=get_font(35), base_color=(255, 255, 255),
                               hovering_color=(193, 43, 28))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, RULES_BUTTON,SCORES_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)#si l'on passe la sourie sur un des boutons, il change de couleur
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):#lancer le menu play lorsque l'on clique
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):#lancer le menu options lorsque l'on clique
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):#sortir du jeu
                    pygame.quit()
                    sys.exit()
                if RULES_BUTTON.checkForInput(MENU_MOUSE_POS):#lancer le menu règles lorsque l'on clique
                    rules()
                if SCORES_BUTTON.checkForInput(MENU_MOUSE_POS):#lancer le menu scores lorsque l'on clique
                    scores()

        pygame.display.update()

if __name__ == '__main__' :
    main_menu()