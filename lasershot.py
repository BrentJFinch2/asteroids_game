import pygame
from shot import Shot
import constants

class LaserShot(Shot):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = 3  # Slightly thicker than normal shots
    
    def draw(self, screen):
        # Draw a longer laser beam instead of a circle
        # Calculate the back end of the laser based on velocity direction
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()
            laser_length = 60  # Length of the laser beam
            start_pos = self.position
            end_pos = self.position - (direction * laser_length)
            
            pygame.draw.line(
                screen,
                "red",  # Bright red laser
                (int(start_pos.x), int(start_pos.y)),
                (int(end_pos.x), int(end_pos.y)),
                6  # Line thickness
            )
        else:
            # Fallback to circle if no velocity
            pygame.draw.circle(screen, "red", (int(self.position.x), int(self.position.y)), self.radius)
