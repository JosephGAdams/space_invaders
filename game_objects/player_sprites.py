import pygame

class players(pygame.sprite.Sprite):
    def __init__(self, size, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.lives = 3
        
        block = pygame.Surface((4, 4))
        block.fill((255, 255, 255))
        
        line_1 = [5, 4, 5, 6, 4, 5, 6, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                  1, 2, 3, 4, 5, 6, 7, 8, 9]
        line_2 = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,4, 4, 4, 4, 4, 4, 4, 4, 4,
                  5, 5, 5, 5, 5, 5, 5, 5, 5]
        
        position = zip([x * 4 for x in line_1], [x * 4 for x in line_2])
        for each in position:
            self.image.blit(block, (each[0], each[1]))
        
        