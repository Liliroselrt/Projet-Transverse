import os
import json, sys
import pygame

SCORE_FILE = os.path.join("resources", "data", "top_scores.json")

def save_score(name, score):
    if not os.path.exists(os.path.dirname(SCORE_FILE)):
        os.makedirs(os.path.dirname(SCORE_FILE))
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)
    else:
        scores = []

    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def load_top_scores():
    if not os.path.exists(SCORE_FILE) or os.path.getsize(SCORE_FILE) == 0:
        return []
    try:
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)
            return [(e["name"], e["score"]) for e in scores]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def afficher_historique(screen, font):
    scores = load_top_scores() or [("Aucun score", 0)]
    width, height = screen.get_size()

    # arrière-plan semi-transparent
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # titre
    title_surf, _ = font.render("TOP 5 SCORES", (255, 255, 255))
    screen.blit(title_surf, ((width - title_surf.get_width()) // 2, 80))

    # lignes de scores
    y = 160
    for nom, score in scores:
        line_surf, _ = font.render(f"{nom}  :  {score}", (255, 255, 255))
        screen.blit(line_surf, ((width - line_surf.get_width()) // 2, y))
        y += 60

    # bouton retour
    back_rect = pygame.Rect(width // 2 - 100, y + 40, 200, 60)
    pygame.draw.rect(screen, (52, 152, 219), back_rect, border_radius=10)
    back_txt, _ = font.render("RETOUR", (255, 255, 255))
    screen.blit(back_txt, (back_rect.x + (back_rect.width - back_txt.get_width()) // 2,
                           back_rect.y + (back_rect.height - back_txt.get_height()) // 2))

    pygame.display.flip()

    # boucle d’attente
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                waiting = False
