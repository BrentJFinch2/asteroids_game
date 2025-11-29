import pygame
import random
import math

from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, *args, **kwargs):
        super().__init__(x, y, radius, *args, **kwargs)
        self.points = self._generate_shape()
        self.radius = radius

    def _generate_shape(self):
        num_points = random.randint(8, 14)
        angle_step = 360 / num_points
        base_r = self.radius
        max_perturb = base_r * 0.3

        points = []
        for i in range(num_points):
            angle_deg = i * angle_step
            angle_rad = math.radians(angle_deg)

            if random.random() < 0.2:
                r = base_r + random.uniform(max_perturb, max_perturb * 2.0)
            else:
                r = base_r - random.uniform(max_perturb, max_perturb *1.5)
                r = max(base_r * 0.3, r)

            x = math.cos(angle_rad) * r
            y = math.sin(angle_rad) * r
            points.append(pygame.math.Vector2(x, y))
        return points

    def draw(self, screen):
        # Transform local offsets into world coordinates
        transformed_points = [
            (self.position.x + p.x, self.position.y + p.y)
            for p in self.points
        ]
        pygame.draw.polygon(screen, "white", transformed_points, width=1)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20,50)
            new_velocity_1 = self.velocity.rotate(random_angle)
            new_velocity_2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_1.velocity = new_velocity_1 * 1.2
            new_asteroid_2.velocity = new_velocity_2 * 1.2

    def get_score_value(self):
        return int(1200 / self.radius)
