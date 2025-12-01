import pygame
from circleshape import CircleShape
import constants

class Powerup(CircleShape):
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, constants.POWERUP_RADIUS)
        self.powerup_type = powerup_type  # e.g., "shield", "speed", "triple_shot"
        self.velocity = pygame.Vector2(0, 50)  # Slowly drifts downward
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def draw(self, screen):
        # We'll draw different colors based on type
        color = self.get_color()
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.radius, 2)
    
    def get_color(self):
        # Different colors for different power-up types
        colors = {
            "shield": "cyan",
            "speed": "yellow",
            "triple_shot": "magenta",
            "laser_shot": "blue",
        }
        return colors.get(self.powerup_type, "white")
