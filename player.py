import pygame
from circleshape import CircleShape
from shot import Shot
from lasershot import LaserShot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.direction = pygame.Vector2(0, 1)
        self.speed = PLAYER_SPEED
        self.shot_cooldown_timer = 0
        self.alive = True
        self.is_invincible = False
        self.visible = True
        self.blink_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if not self.alive or not self.visible:
            return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation +=  PLAYER_TURN_SPEED * dt
        self.direction = pygame.Vector2(0, 1).rotate(self.rotation)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.speed  * dt
        self.position += rotated_with_speed_vector

    def update(self, dt, triple_shot=False, laser_shot=False):
        if not self.alive:
            return None

        keys = pygame.key.get_pressed()
        shot = None

        if keys[pygame.K_LEFT]:
            self.rotate(-dt) # ?
        if keys[pygame.K_RIGHT]:
            self.rotate(dt) # ?
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cooldown_timer <= 0:
                self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                return self.shoot(triple_shot, laser_shot)

        self.shot_cooldown_timer -= dt
        self.shot_cooldown_timer = max(0, self.shot_cooldown_timer)

        self.wrap_position()

        return shot

    def shoot(self, triple_shot=False, laser_shot=False):
        if laser_shot:
            shot = LaserShot(self.position.x, self.position.y)
            shot.velocity = self.direction * PLAYER_SHOOT_SPEED * 1.5
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = self.direction * PLAYER_SHOOT_SPEED
    
        if triple_shot:
            # Return a list of three shots
            import math

            if laser_shot:
                left_shot = LaserShot(self.position.x, self.position.y)
                right_shot = LaserShot(self.position.x, self.position.y)
                speed = PLAYER_SHOOT_SPEED * 1.5
            else:
                left_shot = Shot(self.position.x, self.position.y)
                right_shot = Shot(self.position.x, self.position.y)
                speed = PLAYER_SHOOT_SPEED * 1.5

            # Left shot (rotated -15 degrees)
            left_shot = Shot(self.position.x, self.position.y)
            angle_left = math.radians(-15)
            rotated_left = self.direction.rotate_rad(angle_left)
            left_shot.velocity = rotated_left * PLAYER_SHOOT_SPEED
        
            # Right shot (rotated +15 degrees)
            right_shot = Shot(self.position.x, self.position.y)
            angle_right = math.radians(15)
            rotated_right = self.direction.rotate_rad(angle_right)
            right_shot.velocity = rotated_right * PLAYER_SHOOT_SPEED
        
            return [left_shot, shot, right_shot]
        else:
            return shot

    def reset_position(self, x, y):
        self.position.update(x, y)
        self.velocity.update(0, 0)
        self.rotation = 0
        self.shot_cooldown_timer = 0

