import pygame

class enemies(pygame.sprite.DirtySprite):
    def __init__(self, size, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.y_range = range(self.rect.y, self.rect.y + 100)
        self.can_fire = False
        self.is_firing = False
        self.lives = 3
        
        block = pygame.Surface((4, 4))
        block.fill(colour)
        
        pos_1 = [3, 8, 4, 7, 3, 4, 5, 6, 7, 8, 2, 3, 5, 6, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                 1, 3, 4, 5, 6, 7, 8, 10, 1, 3, 8, 10, 4, 7]
        pos_2 = [0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7]
            
        new_pos = zip([x * 4 for x in pos_1], [y * 4 for y in pos_2])

        for each in new_pos:
            self.image.blit(block, (each[0], each[1]))