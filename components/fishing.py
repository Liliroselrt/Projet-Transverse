import pygame
import math
import numpy as np


class FishingLine:
    def __init__(self, rod_x, rod_y, max_length, boat_y):
        self.rod_x = rod_x
        self.rod_y = rod_y
        self.max_length = max_length
        self.current_length = 0
        self.is_casting = False
        self.segments = 20  # Number of line segments for smoother curve
        self.hook_x = rod_x
        self.hook_y = rod_y

        # Physics parameters
        self.gravity = 9.81
        self.initial_velocity = 60.0
        self.angle_rad = math.radians(60)  # 60 degrees launch angle

        # Water line parameters (y-coordinate where water begins)
        self.water_level = boat_y + 30
        self.hook_in_water = False
        self.water_entry_x = rod_x
        self.sinking_speed = 4.5
        self.sinking_depth = 0

    def update(self, rod_x, rod_y, is_casting, delta_time):
        # Calculer le déplacement du bateau/canne à pêche
        rod_movement = rod_x - self.rod_x

        # Mettre à jour la position de la canne
        self.rod_x = rod_x
        self.rod_y = rod_y
        self.is_casting = is_casting

        # Si l'hameçon est dans l'eau et que le bateau bouge, ajuster le point d'entrée dans l'eau
        if self.hook_in_water and rod_movement != 0:
            # Effet d'amortissement pour un mouvement plus réaliste
            dampening = 0.7  # Facteur d'amortissement (0-1)
            self.water_entry_x += rod_movement * dampening
            self.hook_x = self.water_entry_x  # Mettre à jour la position horizontale de l'hameçon

        # Reset state when not casting
        if not is_casting:
            self.current_length = 0
            self.hook_x = rod_x
            self.hook_y = rod_y
            self.hook_in_water = False
            self.sinking_depth = 0
            return

        # Le reste du code reste inchangé...
        if is_casting and self.current_length < self.max_length:
            self.current_length += 5
            if self.current_length > self.max_length:
                self.current_length = self.max_length

        if self.current_length > 0:
            t = (self.current_length / self.max_length) * 2.0

            if not self.hook_in_water:
                x_offset = self.initial_velocity * math.cos(self.angle_rad) * t * 10
                y_offset = self.initial_velocity * math.sin(self.angle_rad) * t * 10 - 0.5 * self.gravity * (
                            t * 10) ** 2

                self.hook_x = self.rod_x + x_offset
                self.hook_y = self.rod_y - y_offset

                if self.hook_y >= self.water_level:
                    self.hook_in_water = True
                    self.water_entry_x = self.hook_x
                    self.hook_y = self.water_level
            else:
                self.hook_x = self.water_entry_x
                self.sinking_depth = min(self.sinking_depth + self.sinking_speed, 450)
                self.hook_y = self.water_level + self.sinking_depth

    def get_hook_position(self):
        return (self.hook_x, self.hook_y)

    def draw(self, screen):
        if self.current_length <= 0:
            return

        # Draw the fishing line
        points = []

        # Start at rod position
        points.append((self.rod_x, self.rod_y))

        if not self.hook_in_water:
            # When hook is in air, draw a smooth arc
            for i in range(1, self.segments):
                segment_t = (i / self.segments) * (self.current_length / self.max_length) * 2.0

                x_offset = self.initial_velocity * math.cos(self.angle_rad) * segment_t * 10
                y_offset = self.initial_velocity * math.sin(self.angle_rad) * segment_t * 10 - 0.5 * self.gravity * (
                            segment_t * 10) ** 2

                x = self.rod_x + x_offset
                y = self.rod_y - y_offset

                points.append((x, y))

            # Add hook position as the last point
            points.append((self.hook_x, self.hook_y))
        else:
            # When hook is in water, first draw a stable arc to water entry point
            water_reached = False
            for i in range(1, self.segments + 1):
                # Use fixed percentage for stability
                percent = i / self.segments

                # Calculate path from rod to water entry point using a simple curve
                x = self.rod_x + (self.water_entry_x - self.rod_x) * percent

                # Create a curved path using a quadratic function
                # Midpoint is higher than start and end
                h = min(50, abs(self.water_entry_x - self.rod_x) * 0.2)  # Height of arc
                rel_x = percent - 0.5  # -0.5 to 0.5
                y = self.rod_y + (self.water_level - self.rod_y) * percent - h * (1 - 4 * rel_x * rel_x)

                # Stop if we've passed the water level
                if y > self.water_level and not water_reached:
                    water_reached = True
                    points.append((x, self.water_level))
                    break

                points.append((x, y))

            # If we never hit water in the arc, add water entry point
            if not water_reached:
                points.append((self.water_entry_x, self.water_level))

            # Add vertical line in water down to hook
            for i in range(1, 5):
                depth_factor = i / 4
                points.append((self.water_entry_x, self.water_level + self.sinking_depth * depth_factor))

            # Always add the final hook position
            points.append((self.hook_x, self.hook_y))

        # Draw the line
        if len(points) > 1:
            pygame.draw.lines(screen, (139, 69, 19), False, points, 2)

        # Draw hook
        if self.current_length > 10:
            hook_pos = (self.hook_x, self.hook_y)
            pygame.draw.circle(screen, (192, 192, 192), hook_pos, 5)

        # Draw water line for reference
        #pygame.draw.line(screen, (0, 105, 148), (0, self.water_level), (screen.get_width(), self.water_level), 2)
