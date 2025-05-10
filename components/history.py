import os    # Accès aux opérations système et chemins de fichiers
import json, sys    # Gestion JSON pour stocker/charger scores, accès aux paramètres système
import pygame    # Bibliothèque pour afficher l'historique avec Pygame

# Chemin vers le fichier JSON contenant les meilleurs scores
SCORE_FILE = os.path.join("resources", "data", "top_scores.json")

# Fonction pour sauvegarder un score dans le fichier JSON
def save_score(name, score):
    from datetime import datetime    # Import local pour récupérer la date actuelle
    
     # Crée le dossier si nécessaire
    if not os.path.exists(os.path.dirname(SCORE_FILE)):
        os.makedirs(os.path.dirname(SCORE_FILE))
    # Charge les scores existants si le fichier existe
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)
    else:
        scores = []    # Sinon initialise une liste vide

    # Ajout de la date au format JJ/MM/AAAA
    date_str = datetime.now().strftime("%d/%m/%Y")
    scores.append({"name": name, "score": score, "date": date_str})
    # Trie les scores par valeur décroissante et conserve les 5 meilleurs
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]
    # Écrit la liste mise à jour dans le fichier JSON
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

# Charge les 5 meilleurs scores sous forme de liste de tuples (nom, score)
def load_top_scores():
    # Si le fichier n'existe pas ou est vide, retourne une liste vide
    if not os.path.exists(SCORE_FILE) or os.path.getsize(SCORE_FILE) == 0:
        return []
    try:
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)
            # Retourne une liste de tuples (nom, score)
            return [(e["name"], e["score"]) for e in scores]
    except (json.JSONDecodeError, KeyError, TypeError):
        # En cas d'erreur de lecture, retourne une liste vide
        return []
# Charge l'historique complet avec noms, scores et dates pour l'affichage
def charger_historique():
    """Charge l'historique des scores dans le format attendu par afficher_historique."""
    if not os.path.exists(SCORE_FILE) or os.path.getsize(SCORE_FILE) == 0:
        return []
    try:
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)
            # Transforme les données pour inclure le champ 'date' attendu par afficher_historique
            historique = []
            for entry in scores:
                # Adapte le format des anciennes entrées qui pourraient ne pas avoir tous les champs
                historique.append({
                    "nom": entry.get("name", "Inconnu"),
                    "score": entry.get("score", 0),
                    "date": entry.get("date", "Non datée")
                })
            return historique
    except (json.JSONDecodeError, KeyError, TypeError):
        return []
        
# Affiche l'historique des parties à l'écran Pygame
def afficher_historique(screen, font):
    """Affiche l'historique des joueurs sans doublon"""
    # Fond d'écran
    background = pygame.image.load('resources/assets/images/fondRegle2.jpg')
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    screen.blit(background, (0, 0))

    # Titre
    title_text, title_rect = font.render("Historique des parties", (255, 255, 255))
    title_x = (screen.get_width() - title_rect.width) // 2
    screen.blit(title_text, (title_x, 50))

    # Charger les données depuis le fichier (ou la base de données)
    historique = charger_historique()

    # Utiliser un dictionnaire pour éliminer les doublons
    # La clé sera une combinaison du nom et du score (ou un identifiant unique)
    historique_unique = {}
    for joueur in historique:
        # Créer une clé unique pour chaque entrée
        cle = f"{joueur['nom']}_{joueur['score']}_{joueur['date']}"
        historique_unique[cle] = joueur

    # Convertir en liste pour l'affichage
    historique = list(historique_unique.values())

    # Afficher les données
    y_pos = 150
    for joueur in historique:
        info = f"{joueur['nom']} - Score: {joueur['score']} - Date: {joueur['date']}"
        text_surface, _ = font.render(info, (255, 255, 255))
        x_pos = (screen.get_width() - text_surface.get_width()) // 2
        screen.blit(text_surface, (x_pos, y_pos))
        y_pos += 40

    # Bouton retour
    back_button = pygame.Rect(screen.get_width() // 2 - 100, y_pos + 50, 200, 50)
    pygame.draw.rect(screen, (231, 76, 60), back_button, border_radius=10)

    text_surface, _ = font.render("Retour", (255, 255, 255))
    text_x = back_button.x + (back_button.width - text_surface.get_width()) // 2
    text_y = back_button.y + (back_button.height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

    # Attendre un clic pour revenir
    waiting = True
    while waiting:
        pygame.display.flip()    # Actualise l'écran
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False    # Quitte complètement
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    waiting = False     # Sort de la boucle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False    # Sort également sur Échap

    return True    # Retourne True pour indiquer un retour normal
