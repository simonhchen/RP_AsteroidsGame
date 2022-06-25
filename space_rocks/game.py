# space_rocks/game.py
import pygame
from models import Spaceship, Rock
from utils import load_sprite

class SpaceRocks:
    def __init__ (self):
        # Initialize pygame and set the title
        pygame.init()
        pygame.display.set_caption("Space Rock")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((800,600))
        self.background = load_sprite("space", False)

        self.bullets = []

        self.ship = Spaceship((400, 300), self.bullets)

        self.rocks = [Rock(self.screen, self.ship.position) for _ in range(6)]

    def main_loop(self):
        while True:
            self._handleinput()
            self._game_logic()
            self._draw()

    def _handleinput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ship.shoot()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()

        if self.ship is None:
            return

        if is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()

    @property
    def game_objects(self):
        return [*self.rocks, *self.bullets, self.ship]

    def _game_logic(self):
        for obj in self.game_objects:
            obj.move(self.screen)

        rect = self.screen.get_rect()
        for bullet in self.bullets[:]:
            if not rect.collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for rock in self.rocks[:]:
                if rock.collides_width(bullet):
                    self.rocks.remove(rock)
                    self.bullets.remove(bullet)
                    break

        if self.ship:
            for rock in self.rocks[:]:
                if rock.collides_width(self.ship):
                    self.ship = None
                    break

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for obj in self.game_objects:
            obj.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(30)