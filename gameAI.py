import pygame
import sys 
from pygame.locals import *
from settings import *
import random

from sprites import *

import CGP

pygame.init()

font = pygame.font.SysFont("Lucia Sans", 30)

clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.SysFont('Futura', 30)
        
        # Number of platform jumped by each player
        self.jumped_platforms = []
        
        self.platform_list = []
        self.player_list = []
        self.brain_list = []
        self.platforms = pygame.sprite.Group()
        
        self.score = 0
        self.best_score = 0
        # CGP settings
        self.n_players = MU + LAMBDA
        self.global_max_fitness = 0
        self.max_fitness = 0
        self.current_generation = 0

        # create the initial population
        self.pop = CGP.create_population(self.n_players)


    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
    
    def game_score(self, scroll):
        """
        Show the current and best score of the best player
        """
        global points
        self.score += int(scroll)
        points = self.score//10
        # show the current score
        pygame.draw.rect(self.screen, 'White', (0, 0, SCREEN_WIDTH, 20))
        self.draw_text("SCORE: " + str(int(points)), font, 'Black', 0, 0)
        # show the best score so far
        if self.best_score < points:
            self.best_score = points
        self.draw_text("BEST SCORE: " + str(int(self.best_score)), font, 'Black', 250, 0)
        return int(points)


    def statistics(self):
        """
        Shows the number of players alive and the current generation
        """
        self.draw_text('Players Alive:' + str(len(self.player_list)), font, 'White', 0, 30)
        self.draw_text('Generation:' + str(self.current_generation) , font, 'White', 250, 30)

    
    def top_player(self):
        """
        Get the top player to update the screen and scroll
        """
        players_rect_y = []
        for player in self.player_list:
            players_rect_y.append(player.rect.y)
        min_y = min(players_rect_y)
        top_player_index = players_rect_y.index(min_y)
        return top_player_index

    
    def platforms_hit_update(self):
        """
        Update the total platforms jumped by each player
        """
        # check if the player jumped on a new platform
        for i, player in enumerate(self.player_list):
            for j, plat in enumerate(self.platform_list):
                hits = pygame.sprite.collide_rect(player, plat)
                if hits:
                    if j > self.jumped_platforms[i]:
                        self.brain_list[i].fitness += 7
                        self.jumped_platforms[i] = j
                    if j <= self.jumped_platforms[i]:
                        self.brain_list[i].fitness -= 0.1
                        
    
    def fitness_max(self):
        """
        Get the best fitness used to choose the mutation rate
        """
        list = [brain.fitness for brain in self.brain_list]
        if len(list) > 0:
            self.max_fitness = max(list)
        else: 
            self.max_fitness = self.max_fitness
        if self.global_max_fitness < self.max_fitness:
            self.global_max_fitness = self.max_fitness
        return self.max_fitness

    def try_move(self, player):
        """
        Choose the player movement based on the CGP
        """
        # data = [vertical_distance, horizontal_distance_left, horizontal_distance_right]
        data = player.update_data(self.platform_list)
        player.jump = True
        if player.eval(data[0], data[1], data[2])<-10:
            player.moving_left = True
            player.moving_right = False
        elif player.eval(data[0], data[1], data[2])>10:
            player.moving_left = False
            player.moving_right = True
        else:
            player.moving_left = False
            player.moving_right = False
            

    def remove(self, index):
        """
        Remove the player, its brain and the number of
        the platforms jumped from the lists
        """
        self.player_list.pop(index)
        self.brain_list.pop(index)
        self.jumped_platforms.pop(index)

    def generate_platform(self):
        # platform scale width
        p_w = random.randint(1, 2)
        platform = self.platform_list[-1]
        # define the min and max horizontal position
        x_min = max(0, platform.rect.x - MIN_PLATFORM_LENGTH * p_w - MAX_PLATFORM_GAP)
        x_max = min(SCREEN_WIDTH - MIN_PLATFORM_LENGTH * p_w, platform.rect.x + platform.rect.width+MAX_PLATFORM_GAP)
        # platform position
        p_x = random.uniform(x_min, x_max)
        p_y = platform.rect.y - random.randint(80, 100) 
        
        platform = Platform(p_x, p_y, p_w)
        self.platform_list.append(platform)

    
    def reset(self):
        """
        Create new generation
        """
        print(f'---------Generation: {self.current_generation}. Max score so far: {self.global_max_fitness}--------')
        self.max_fitness = 0
        self.score = 0
        self.current_generation += 1
        # empty all the current players if any
        # instantiate players
        self.player_list.clear()
        self.platform_list.clear()
        self.jumped_platforms.clear()

        _max_fitness = self.fitness_max()
        pb = MUT_PB
        if _max_fitness < 500:
            pb = MUT_PB * 3
        elif _max_fitness < 1000:
            pb = MUT_PB * 2
        elif _max_fitness < 2000:
            pb = MUT_PB * 1.5
        elif _max_fitness < 5000:
            pb = MUT_PB * 1.2
        
        platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
        self.platform_list.append(platform)

        for i in range(self.n_players):
            self.pop[i].fitness = 0
            self.player_list.append(AIPlayer(self.pop[i]))
            self.brain_list.append(self.pop[i])
            self.jumped_platforms.append(0)
        
        self.pop = CGP.evolve(self.pop, pb, MU, LAMBDA)
    
    
    
    def run(self):
        """
        Run the Game
        """
        counter = 150
        check = 0

        platform2 = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
        platform = Platform(SCREEN_WIDTH//2 + 70, SCREEN_HEIGHT -100, 2)
        self.platform_list.append(platform)
        self.platform_list.append(platform2)

        for i in range(self.n_players):
            self.pop[i].fitness = 0
            self.player_list.append(AIPlayer(self.pop[i]))
            self.brain_list.append(self.pop[i])
            self.jumped_platforms.append(0)
        
        while self.current_generation < N_GEN:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


            self.screen.fill('BLUE')
            
            if len(self.platform_list) < MAX_PLATFORM:
                self.generate_platform()

            top_player_index = self.top_player()

            self.platforms_hit_update()
            
            for i, player in enumerate(self.player_list):
                player.draw(self.screen)
                player.update(self.platform_list)
                if i == top_player_index:
                    scroll_bg = player.move(0, self.platform_list)
                else:
                    player.move(scroll_bg, self.platform_list)

                self.try_move(player)
                if player.rect.top > SCREEN_HEIGHT: 
                    self.brain_list[i].fitness -= 1           
                    self.remove(i)

            for plat in self.platform_list:
                plat.draw(self.screen)
                plat.update(self.platform_list, scroll_bg)

            # detect if the players are not moving for specific duration of time
            game_score = self.game_score(scroll_bg)

            self.statistics()

            # Check if the generation is stuck and doesn't progress
            counter -=1
            if counter == 0:
                # If the best player score is not progressing for the duration specified
                # penalise the players and create a new generation
                if check == game_score:
                    for i,player in enumerate(self.player_list):
                         self.brain_list[i].fitness -=1
                    self.reset()
                    counter = 150 
                else:
                    # Reset the counter and set the check score to the game score                         
                    check = game_score
                    counter = 150 
                    
            if len(self.player_list) == 0:
                self.reset()

            
            pygame.display.update()
            clock.tick(60)

