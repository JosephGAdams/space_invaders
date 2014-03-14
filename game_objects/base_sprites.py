import pygame

class bases(pygame.sprite.Sprite):
    def __init__(self, size, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.health = 100

class base_pieces(pygame.sprite.Sprite):
    def __init__(self, size, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]