import pygame


class Piece(pygame.sprite.Sprite):
    def __init__(self, x, y, name, width, height):
        super().__init__()
        # self.surf = pygame.Surface((width, height))
        # self.surf.fill((120, 120, 120))
        # self.rect = self.surf.get_rect()

        self.x = x
        self.y = y

        self.image = pygame.image.load(f'images/{name}.png')
        self.image = pygame.transform.scale(self.image, (width, height))
