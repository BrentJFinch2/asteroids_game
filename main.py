import pygame
import sys
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS
from logger import log_state, log_event

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000

    score_font = pygame.font.SysFont(None, 30)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    my_player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    player_lives = 3
    player_alive = True
    is_invincible = False
    respawn_timer = 0
    invincibility_timer = 0
    player_visible = True
    blink_timer = 0

    Shot.containers = (shots, updatable, drawable)

    Explosion.containers = (explosions, updatable, drawable)

    score = 0
    game_over = False

    while not game_over:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        if not player_alive:
            respawn_timer -= dt
            if respawn_timer <= 0:
                my_player.reset_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player_alive = True
                my_player.alive = True
                is_invincible = True
                my_player.invincible = True
                invincibility_timer = 2.0
                my_player.visible = True
                my_player.blink_timer = 0.0

        if is_invincible:
            invincibility_timer -= dt
            my_player.blink_timer -= dt
            if my_player.blink_timer <= 0:
                my_player.visible = not my_player.visible
                my_player.blink_timer = 0.1
            if invincibility_timer <= 0:
                is_invincible = False
                my_player.is_invincible = False
                my_player.visible = True
        else:
            my_player.visible = True

        updatable.update(dt)

        if player_alive:
            for a in asteroids:
                if a.collides_with(my_player):
                    if is_invincible:
                        continue

                    log_event("player_hit")
                    explosion = Explosion(my_player.position.x, my_player.position.y, 0)
                    player_lives -= 1
                    player_alive = False
                    my_player.alive = False
                    respawn_timer = 2.0

                    if player_lives == 0:
                        game_over = True

                    break

                for s in shots:
                    if s.collides_with(a):
                        log_event("asteroid_shot")
                        a.split()
                        score += a.get_score_value()
                        explosion = Explosion(a.position.x, a.position.y, 0)
                        s.kill()
        for d in drawable:
            d.draw(screen)
        score_text = score_font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        lives_text = score_font.render(f"Lives: {player_lives}", True, "white")
        screen.blit(lives_text, (10, 30))
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
