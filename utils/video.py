import pygame
import cv2

def start_video(screen, clock, WIDTH, HEIGHT):
    # Recherche vidéo
    cap = cv2.VideoCapture("resources/animation/animation.mpg")

    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la vidéo")
    else:
        # Afficher la vidéo
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Redimensionner correctement en préservant les proportions
            frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)

            # Conversion correcte pour Pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pygame_frame = pygame.image.frombuffer(frame.tobytes(), (WIDTH, HEIGHT), "RGB")

            # Gestion de l'image
            screen.blit(pygame_frame, (0, 0))
            pygame.display.flip()

            # Permettre de quitter pendant la vidéo avec ESC
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    cap.release()
                    break

            clock.tick(30)  # 30 FPS pour la vidéo, plus stable que delay

    cap.release()  # Arrêt de la vidéo
