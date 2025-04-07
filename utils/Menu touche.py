import pygame
import pygame.freetype
import os
from utils.utils import *

def afficher_menu_touches(nb_joueur):
    print("\n=== Commandes du Jeu ===")

    if nb_joueur == 1:
        print("Mode 1 Joueur :")
        print("  - Déplacement : Flèches directionnelles ou ZQSD")
        print("  - Canne à pêche : Espace")

    else:
        print("Mode 2 Joueurs :")
        print("Joueur 1 :")
        print("- Déplacement : Z (haut), S (bas), Q (gauche), D (droite)")
        print("- Canne à pêche : A")
        print("Joueur 2 :")
        print("- Déplacement : Flèches directionnelles")
        print("- Canne à pêche : M")


def choisir_mode():
    while True:
        try:
            nb_joueur = int(input("Entrez le nombre de joueurs (1 ou 2) : "))
            if nb_joueur in [1, 2]:
                break
            else:
                print("Veuillez entrer 1 ou 2.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    afficher_menu_touches(nb_joueur)

