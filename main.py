import pygame
import random
import sys

from pygame.locals import *
from game_objects.enemy_sprites import enemies
from game_objects.player_sprites import players
from game_objects.bullet_sprites import bullets
from game_objects.base_sprites import bases, base_pieces

enemy = enemies
player = players
weapon = bullets
base = bases
base_piece = base_pieces


class main_code:
    def main(self):
        self.clock = pygame.time.Clock()
        self.size = width, height = 800, 600
        #Set the size of the invader sprites
        self.sprite_size = sprite_width, sprite_height = 44, 32
        
        display = pygame.display.set_mode(self.size)
        caption = pygame.display.set_caption("Space Invaders V1.0")
        
        #Define sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.base_sprites = pygame.sprite.Group()
        self.base_one = pygame.sprite.Group()
        self.base_two = pygame.sprite.Group()
        self.base_three = pygame.sprite.Group()
        
        #Create invaders, ships, bases, add to groups
        self.invaders = self.create_invaders()
        self.ship = player(self.sprite_size, (0, 255, 0), (50, height - self.sprite_size[1]))
        sprite_base_one = self.create_bases(self.base_sprites, self.base_one, 1)
        sprite_base_two = self.create_bases(self.base_sprites, self.base_two, 2)
        sprite_base_three = self.create_bases(self.base_sprites, self.base_three, 3)
        self.all_sprites.add(self.ship)
        self.player_sprites.add(self.ship)
        
        #Set up font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        
        #Set up default settings
        self.starting_y_position = min([x.rect.y for x in self.invaders])
        enemy_position = self.check_enemy_position(self.invaders)
        self.bullet_in_play = False
        self.movement = "right"
        self.playing = True
        self.finish = False
        self.end_game = False
        self.score = 0
        self.rebuild = 0
        self.new_life = 0
        self.anim_counter = 0
        
        self.win_board = pygame.Surface((200, 30))
        self.win_board.set_colorkey((0, 0, 0))
        self.win_board.fill((0, 0, 0))
        output = self.font.render("Game Over", 1, (0, 255, 0))        
        self.win_board.blit(output, (0, 0))
        
        self.replay_board = pygame.Surface((200, 30))
        self.replay_board.set_colorkey((0, 0, 0))
        self.replay_board.fill((0, 0, 0))
        game_replay = self.font.render("To play again, press P", 1, (0, 255, 0))
        self.replay_board.blit(game_replay, (0, 0))
        
        self.game_board = pygame.Surface((200, 30))
        self.game_board.fill((0, 0, 0))
        game_quit = self.font.render("To quit, press Q", 1, (0, 255, 0))
        self.game_board.blit(game_quit, (0, 0))
        
        while 1: 
            self.run_code(display)
    
    def splash_screen(self, display):
        pass
        
                
    def run_code(self, display):       
        if self.ship.lives < 0:
            self.end_game = True
        if self.end_game == False:
            self.score_effects()
            
            #set up score display
            self.score_box = pygame.Surface((200, 30))
            self.score_box.set_colorkey((0, 0, 0))
            text = self.font.render("Score: {}".format(str(self.score)), 1, (0, 255, 0))
            textpos = text.get_rect()
            self.score_box.blit(text, textpos)
            
            #set up life display
            self.life_box = pygame.Surface((200, 30))
            self.life_box.set_colorkey((0, 0, 0))
            life_text = self.font.render("Lives: {}".format(str(self.ship.lives)), 1, (0, 255, 0))
            life_text_pos = life_text.get_rect()
            self.life_box.blit(life_text, life_text_pos)
            
            #Take in keyboard input, allow multiple keys to be pressed
            key = pygame.key.get_pressed()
            self.move_ship(self.ship, key)
            self.fire_ship(self.ship, self.invaders, key)
            
            try:
                self.move_bullet(self.enemy_bullets, self.invaders, "invader")
            except:
                pass
            try:
                self.move_bullet(bullets, self.invaders, "player")
            except:
                pass
    
            self.move_invaders(self.invaders)
            if key[K_DOWN]:
                self.ship.lives = -1
                
            #If there are no more enemies create a new wave
            if len(self.invaders) < 1:
                self.invaders = self.create_invaders()
                
        elif self.end_game == True:
            self.remove_sprites(self.invaders)
            key = pygame.key.get_pressed()
            if key[K_p]:
                # Bad way of starting over? // YES, takes more ram, move play into own function!!!
                main_code().main()
            elif key[K_q]:
                pygame.quit()
                sys.exit()
            
        #Check for exit conditions
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        draw_items = [self.bullet_sprites, self.enemy_bullets, self.invaders, self.player_sprites,
                      self.base_sprites]
        
        blit_items = [(self.score_box, 10, 20), (self.life_box, self.size[0] - 200, 20)]
        
        self.blit_screen(display, draw_items, blit_items)
        
    def blit_screen(self, display, draw_items, blit_items):
        display.fill((0, 0, 0))
        for each in draw_items:
            each.draw(display)
        for each in blit_items:
            display.blit(each[0], (each[1], each[2]))

        if self.end_game == True:
            display.blit(self.win_board, (self.size[0] / 2, self.size[1] / 2))
            display.blit(self.replay_board, (self.size[0] / 2, self.size[1] / 2 + 30))
            display.blit(self.game_board, (self.size[0] / 2, self.size[1] / 2 + 60))
        pygame.display.flip()
        self.clock.tick(30)
            
    def score_effects(self):
        if self.rebuild == 1000:
            for each in self.base_sprites:
                each.kill()
            self.create_bases(self.base_sprites, self.base_one, 1)
            self.create_bases(self.base_sprites, self.base_two, 2)
            self.create_bases(self.base_sprites, self.base_three, 3)
            self.rebuild = 0
        if self.new_life == 1000:
            for each in self.player_sprites:
                each.lives += 1
                self.new_life = 0
                break
            
    def fire_ship(self, ship, invaders, key):
        if key[K_SPACE] or key[K_UP]:
            if self.bullet_in_play != True: 
                new_bull = weapon((2, 10), (255, 255, 255), 
                           (ship.rect.x + self.sprite_size[0] / 2, ship.rect.y))
                self.bullet_sprites.add(new_bull)
                self.bullet_in_play = True
        for each in invaders:
            if each.can_fire == True:
                # Change change of enemy firing higher = < chance
                i = random.randint(0, len(invaders) * 10)
                new_bullet = weapon((2, 10), (255, 255, 255),
                (each.rect.x + self.sprite_size[0] / 2, each.rect.y))
                if i == 8:
                    self.enemy_bullets.add(new_bullet)
            
    def move_ship(self, ship, key):
        if key[K_LEFT]:
            if ship.rect.x > 0:
                ship.rect.x -= 10
        if key[K_RIGHT]:
            if ship.rect.x <= self.size[0] - self.sprite_size[0]:
                ship.rect.x += 10
            
    def create_invaders(self):
        invaders = pygame.sprite.Group()
        x_position, y_position, row_counter, sprite_counter = 50, 0, 0, 0
        while sprite_counter != 55:
            if row_counter % 11 == 0:
                y_position += self.sprite_size[1] + self.sprite_size[1] / 2
                x_position = self.sprite_size[0]
            new_enemy = enemy(self.sprite_size, (255, 255, 255), (x_position, y_position))
            invaders.add(new_enemy)
            self.all_sprites.add(new_enemy)
            x_position += self.sprite_size[0] + self.sprite_size[0] / 2
            sprite_counter += 1
            row_counter += 1
        return invaders
    
    def remove_sprites(self, invaders):
        for each in self.bullet_sprites:
            each.kill()
        for each in self.enemy_bullets:
            each.kill()
        for each in invaders:
            each.kill()
            break
    
    def move_bullet(self, bullets, invaders, shooter):
        if shooter == "player":
            for bullet in self.bullet_sprites:
                if len(self.bullet_sprites) > 1:
                    bullet.kill()
                kill = pygame.sprite.spritecollide(bullet, invaders, True)
                demolish = pygame.sprite.spritecollide(bullet, self.base_sprites, False)
                
                for each in demolish:
                    each.health -= 10
                    if each.health == 0:
                        each.kill()
                    bullet.kill()
                    self.score -= 10
                    self.bullet_in_play = False
                    
                for victim in kill:
                    bullet.kill()
                    self.bullet_in_play = False
                    self.score += 10
                    self.rebuild += 10
                    self.new_life += 10
                    enemy_position = self.check_enemy_position(invaders)
                                                
                bullet.rect.y -= 20
                if bullet.rect.y < 0:
                    bullet.kill()
                    self.bullet_in_play = False
        
        elif shooter == "invader":
            for bullet in self.enemy_bullets:
                killer = pygame.sprite.spritecollide(bullet, self.player_sprites, False)
                demolish = pygame.sprite.spritecollide(bullet, self.base_sprites, False)
                
                for each in demolish:
                    each.health -= 10
                    if each.health == 0:
                        each.kill()
                    bullet.kill()
                    self.bullet_in_play = False
                    
                for each in killer:
                    if each.lives <= 0:
                        each.kill()
                        self.end_game = True
                    bullet.kill()
                    each.lives -= 1
                    each.rect.x = self.size[0] / 2                    
                    
                bullet.rect.y += 20
                if bullet.rect.y > self.size[1]:
                    bullet.kill()
        
    def move_invaders(self, invaders):
        if self.movement == "right":
            for each in invaders:
                each.rect.x += 1
                if each.rect.x >= self.size[0] - self.sprite_size[0]:
                    self.movement = "left"
                    for enemy in invaders:
                        enemy.rect.y += 4   
        elif self.movement == "left":
            for each in invaders:
                each.rect.x -= 1
                if each.rect.x <= 0:
                    self.movement = "right"
                    for enemy in invaders:
                        enemy.rect.y += 4
                        
        ship_collision = pygame.sprite.spritecollide(self.ship, invaders, False)
        
        for impact in ship_collision:
            self.ship.lives -= 1
            self.ship.rect.x = self.size[0] / 2
            return_position = min([x.rect.y for x in invaders])
            position_difference = return_position - self.starting_y_position
            for each in invaders:
                each.rect.y -= position_difference
        terrain_collision = pygame.sprite.groupcollide(self.base_sprites, invaders, True, False)
                        
    def create_bases(self, base_list, base_part_list, base_number):
        if base_number == 1:
            x_pos, y_pos = 120, 500
        elif base_number == 2:
            x_pos, y_pos = 320, 500
        elif base_number == 3:
            x_pos, y_pos = 520, 500
            
        base_object = base((80, 40), (0, 0, 0), (x_pos, y_pos))
        base_list.add(base_object)
        
        block = pygame.Surface((4, 4))
        block.set_colorkey((0, 0, 0))
        block.fill((0, 255, 0))
        piece_line_one = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                          1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                          1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                          1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                          1, 2, 3, 4, 16, 17, 18, 19]
        
        piece_line_two = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                          2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                          3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                          4, 4, 4, 4, 4, 4, 4, 4,]
        pieces = zip([x * 4 for x in piece_line_one], [x * 4 for x in piece_line_two])
        for each in pieces:
            sprite_block = base_piece((4, 4), (0, 255, 0), (each[0], each[1]))
            base_object.image.blit(sprite_block.image, (sprite_block.rect.x, sprite_block.rect.y))
            sprite_block.rect.x = x_pos + sprite_block.rect.x
            sprite_block.rect.y = y_pos + sprite_block.rect.y
            base_part_list.add(sprite_block)
            
    def check_enemy_position(self, invaders):
        for enemy in invaders:
            enemy.can_fire = True
            for other in invaders:
                if other.rect.y > enemy.rect.y and other.rect.x == enemy.rect.x:
                    # if the other is lower that the enemy (y) and in line with it (x)
                    enemy.can_fire = False
                    break
            
if __name__ == "__main__":
    main_code().main()