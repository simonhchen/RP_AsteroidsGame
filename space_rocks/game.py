# space_rocks/game.py
import pygame
from models import Spaceship
from utils import load_sprite

class SpaceRocks():
    def __init__ (self):
        # Initialize pygame and set the title
        pygame.init()
        pygame.display.set_caption("Space Rock")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((800,600))
        self.background = load_sprite("space", False)

        self.ship = Spaceship((400, 300))

    def main_loop(self):
        while True:
            self._handleinput()
            self._game_logic()
            self._draw()

    def _handleinput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()
        elif is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()

    def _game_logic(self):
        self.ship.move(self.screen)

    def _draw(self):
        """draw function. Rock and ship needs to be after background rock and ship is not overwritten"""
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)