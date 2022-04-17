import numpy as np

def player_wagon_cards(player):
    """
    Fonction qui doit parcourir les cartes du joueur et renvoyer sous forme de dictionnaire combien il à de cartes pour chaque couleur de wagon
    Penser à utiliser uniquement la liste de ses cartes wagons
    Penser à bien garder le même orde des couleurs que dans la class player pour le return
    """
    pass

def check_real_roads(player,new_road):
    """
    Fonction qui doit mettre à jour les villes reliées par l'utilisateur à chaque fois qu'il prend une route
    par exemple :
    si il avait déjà relié "ville1" à "ville2"
    et qu'il vient de relié "ville2" à "ville3"
    alors on ajoute à player.linked_cities : ("ville1","ville3") (pas sous forme d'objet route)
    """
    pass

def message(message,time):
    #seulement pour partie graphique
    #affichage d'un message dans un cadre quelque part pendant un temps donnée avant de disparaitre (multithread ?)
    #prend en paramètre message à afficher + temps d'affichage
    pass

def pop_up(message,objects):
    #affiche une fenetre pop up avec un message et la liste des objets étaler grace à leur .represent à des positions différentes
    #attend que l'utilisateur clique sur les objets étalers puis return l'objet choisi
    #penser à changer le status du joueur quand j'utilise ca pour que les objets ne soit pas cliquable comme d'habitude, ils doivent se renvoyer eux-mêmes à la place.
    pass

def delete_cards(player,color,amount,pioche):
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