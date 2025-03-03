import pygame

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu du Jeu")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)

# Police
font = pygame.font.Font(None, 50)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Boucle du menu
menu_running = True
while menu_running:
    fenetre.fill(BLANC)
    draw_text("Menu du Jeu", font, NOIR, fenetre, largeur // 2, 100)
    draw_text("1. Jouer", font, VERT, fenetre, largeur // 2, 250)
    draw_text("2. Quitter", font, ROUGE, fenetre, largeur // 2, 350)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("Démarrer le jeu (logique à implémenter)")
                menu_running = False  # Remplacez ceci par le lancement du jeu
            elif event.key == pygame.K_2:
                menu_running = False

# Police
font = pygame.font.Font(None, 50)
font_grand = pygame.font.Font(None, 70)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Scores des joueurs (à remplacer par les vrais scores après une partie)
score_joueur1 = 50
score_joueur2 = 80

# Détermination du gagnant
if score_joueur1 > score_joueur2:
    gagnant, perdant = ("Joueur 1", score_joueur1, "Joueur 2", score_joueur2)
    couleur_gagnant, couleur_perdant = VERT, ROUGE
elif score_joueur2 > score_joueur1:
    gagnant, perdant = ("Joueur 2", score_joueur2, "Joueur 1", score_joueur1)
    couleur_gagnant, couleur_perdant = VERT, ROUGE
else:
    gagnant, perdant = ("Joueur 1", score_joueur1, "Joueur 2", score_joueur2)
    couleur_gagnant, couleur_perdant = NOIR, NOIR  # Match nul

# Affichage des résultats
result_running = True
while result_running:
    fenetre.fill(BLANC)
    draw_text("Résultats", font, NOIR, fenetre, largeur // 2, 100)
    draw_text(f"{gagnant}: {score_joueur1 if gagnant == 'Joueur 1' else score_joueur2} pts", font_grand,
              couleur_gagnant, fenetre, largeur // 2, 250)
    draw_text(f"{perdant}: {score_joueur2 if perdant == 'Joueur 2' else score_joueur1} pts", font, couleur_perdant,
              fenetre, largeur // 2, 400)
    draw_text("Appuyez sur une touche pour quitter", font, NOIR, fenetre, largeur // 2, 500)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            result_running = False
        elif event.type == pygame.KEYDOWN:
            result_running = False

# Quitter proprement
pygame.quit()

# Mise a jour des points en direct
import pygame
import random

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de collecte")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)
MARRON = (165, 42, 42)

# Police
font = pygame.font.Font(None, 50)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Scores initiaux des joueurs
score_joueur1 = 0
score_joueur2 = 0

# Positions des joueurs
joueur1 = pygame.Rect(200, 500, 50, 50)
joueur2 = pygame.Rect(600, 500, 50, 50)

# Création des objets (déchets et poissons)
objets = []
for _ in range(10):
    type_objet = random.choice(["dechet", "poisson"])
    objets.append({
        "rect": pygame.Rect(random.randint(100, 700), random.randint(100, 400), 30, 30),
        "type": type_objet,
        "color": VERT if type_objet == "dechet" else MARRON
    })

# Boucle du jeu
running = True
while running:
    fenetre.fill(BLANC)

    # Affichage des scores
    draw_text(f"Joueur 1: {score_joueur1} pts", font, ROUGE, fenetre, 200, 50)
    draw_text(f"Joueur 2: {score_joueur2} pts", font, BLEU, fenetre, 600, 50)

    # Affichage des joueurs
    pygame.draw.rect(fenetre, ROUGE, joueur1)
    pygame.draw.rect(fenetre, BLEU, joueur2)

    # Affichage des objets
    for objet in objets:
        pygame.draw.rect(fenetre, objet["color"], objet["rect"])

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouvements des joueurs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        joueur1.x -= 5
    if keys[pygame.K_d]:
        joueur1.x += 5
    if keys[pygame.K_LEFT]:
        joueur2.x -= 5
    if keys[pygame.K_RIGHT]:
        joueur2.x += 5

    # Vérification de la collecte d'objets
    for objet in objets[:]:
        if joueur1.colliderect(objet["rect"]):
            if objet["type"] == "dechet":
                score_joueur1 += 3
            else:
                score_joueur1 -= 1
            objets.remove(objet)
        elif joueur2.colliderect(objet["rect"]):
            if objet["type"] == "dechet":
                score_joueur2 += 3
            else:
                score_joueur2 -= 1
            objets.remove(objet)

# Quitter proprement
pygame.quit()
