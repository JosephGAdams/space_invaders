import pygame

class bullets(pygame.sprite.Sprite):
    def __init__(self, size, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]