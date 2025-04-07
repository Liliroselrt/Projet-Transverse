import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Commandes du Jeu")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Police
pygame.font.init()
police = pygame.font.SysFont("AutourOne", 28)

def afficher_texte(surface, texte, x, y, couleur=NOIR):
    rendu = police.render(texte, True, couleur)
    surface.blit(rendu, (x, y))

def afficher_menu_touches(nb_joueur):
    fenetre.fill(BLANC)
    y = 50

    afficher_texte(fenetre, "=== Commandes du Jeu ===", 50, y)
    y += 50

    if nb_joueur == 1:
        afficher_texte(fenetre, "Mode 1 Joueur :", 50, y)
        y += 40
        afficher_texte(fenetre, "- Déplacement : Flèches directionnelles ou ZQSD", 70, y)
        y += 40
        afficher_texte(fenetre, "- Canne à pêche : Espace", 70, y)
    else:
        afficher_texte(fenetre, "Mode 2 Joueurs :", 50, y)
        y += 40
        afficher_texte(fenetre, "Joueur 1 :", 70, y)
        y += 40
        afficher_texte(fenetre, "- Déplacement : Z (haut), S (bas), Q (gauche), D (droite)", 90, y)
        y += 40
        afficher_texte(fenetre, "- Canne à pêche : A", 90, y)
        y += 50
        afficher_texte(fenetre, "Joueur 2 :", 70, y)
        y += 40
        afficher_texte(fenetre, "- Déplacement : Flèches directionnelles", 90, y)
        y += 40
        afficher_texte(fenetre, "- Canne à pêche : M", 90, y)

    pygame.display.flip()

def choisir_mode():
    nb_joueur = None
    while nb_joueur not in [1, 2]:
        choix = input("Entrez le nombre de joueurs (1 ou 2) : ")
        if choix in ["1", "2"]:
            nb_joueur = int(choix)
        else:
            print("Veuillez entrer 1 ou 2.")
    return nb_joueur

# Main
nb_joueur = choisir_mode()
afficher_menu_touches(nb_joueur)

# Boucle principale pour garder la fenêtre ouverte
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
