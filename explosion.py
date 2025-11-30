import pygame
import random
import math

from circleshape import CircleShape
from constants import LINE_WIDTH

class Explosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.time_alive = 0
        self.duration = 0.25

        # --- Flickering starburst ---
        self.num_spikes = 8
        self.small_radius = 8
        self.large_radius = 16
        self.current_radius = self.small_radius

        # --- Expanding circle ---
        self.circle_start_radius = 5
        self.circle_end_radius = 40
        self.circle_radius = self.circle_start_radius

    def update(self, dt):
        self.time_alive += dt
        if self.time_alive >= self.duration:
            self.kill()
            return

        # --- Flickering starburst ---
        phase_length = self.duration / 4
        phase_index = int(self.time_alive / phase_length)

        if phase_index == 0 or phase_index == 2:
            current_radius = self.small_radius
        else:
            current_radius = self.large_radius

        self.current_radius = current_radius

        # --- Expanding circle ---
        progress = self.time_alive / self.duration
        self.circle_radius = (
            self.circle_start_radius
            + (self.circle_end_radius - self.circle_start_radius) * progress
        )

    def draw(self, screen):
        center_x = self.position.x
        center_y = self.position.y

        # --- Flickering starburst ---
        for i in range(0, 8):
            angle = 2* math.pi * i / self.num_spikes

            dx = math.cos(angle) * self.current_radius
            dy = math.sin(angle) * self.current_radius

            end_x = center_x + dx
            end_y = center_y + dy

            pygame.draw.line(screen, "yellow", (center_x, center_y), (end_x, end_y), LINE_WIDTH)

            # --- Expanding circle ---
            pygame.draw.circle(screen, "yellow", (center_x, center_y), self.circle_radius, LINE_WIDTH)

    @property
    def alive(self):
        return self.time_alive < self.duration
