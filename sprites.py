import pygame
from pygame.locals import *
from settings import *



class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.vel_y = 0
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.direction = 1
        self.flip = False
        self.speed = 4
        self.in_air = True
        image = pygame.image.load('image/player.png')
        self.image = pygame.transform.scale(image, (int(image.get_width()*0.5), int(image.get_height()*0.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
        self.data = []
        self.score = 0

    def move(self,scroll_bg, platform_list):
        scroll = 0
        dx = 0
        dy = 0
        if self.moving_right:
            dx = self.speed
            self.flip = True
            self.direction = -1
        if self.moving_left:
            dx = - self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True
        
        
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # Check collision with the edges
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = self.rect.right - SCREEN_WIDTH
        if self.rect.left + dx < 0:
            dx = self.rect.left     

        # Check collusion with the platform
        # Check only when falling
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platform_list, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.rect.bottom < lowest.rect.centery:
                    self.rect.bottom = lowest.rect.top
                    dy = 0 
                    self.vel_y = 0
                    self.in_air = False
                              
        # Check if the player has bounced to the top of the screen
        if self.rect.top <= SCREEN_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy


        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll + scroll_bg

        return scroll
    
    def get_input(self):
        key = pygame.key.get_pressed()    
        if key[K_LEFT]:
            self.moving_left = True
            self.moving_right = False
        elif key[K_RIGHT]:
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_left = False
            self.moving_right = False
        if key[K_UP]:
            self.jump = True
        else:
            self.jump = False
    
    def update(self, platform_list):
        for platform in platform_list:
            self.data = [self.rect.left-platform.rect.left, self.rect.right-platform.rect.right]

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class AIPlayer(Player):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
    
    def eval(self, v, h, g):
        return self.brain.eval(v, h, g)
    
    def kill(self):
        super().kill()
        self.brain.fitness = self.score
    
    def update_data(self, platform_list):
        nearest_platform = min(platform_list, key=lambda platform: abs(platform.rect.centery - self.rect.centery))

        # Calculate the position of the player in relation to the nearest platform
        vertical_distance = nearest_platform.rect.top - self.rect.bottom
        horizontal_distance_left = nearest_platform.rect.topleft[0] - self.rect.bottomleft[0] if nearest_platform.rect.topleft[0] > self.rect.bottomleft[0] else self.rect.bottomleft[0] - nearest_platform.rect.topleft[0]
        horizontal_distance_right = nearest_platform.rect.topright[0] - self.rect.bottomright[0] if nearest_platform.rect.topright[0] > self.rect.bottomright[0] else self.rect.bottomright[0] - nearest_platform.rect.topright[0]

        self.data = [vertical_distance, horizontal_distance_left, horizontal_distance_right]

        return self.data

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('image/platform.png')
        self.image = pygame.transform.scale(image,(int(image.get_width()*0.3*width), int(image.get_height()*0.3)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, platform_list, scroll):
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            for platform in platform_list:
                if platform == self:
                    platform_list.remove(platform)

