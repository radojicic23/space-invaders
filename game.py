import pygame, random, sys

from GUI.display import display_surface, WINDOW_WIDTH, WINDOW_HEIGHT
from GUI.alien import Alien


class Game:
    """A class to help control and update gameplay"""
    def __init__(self, player, background_group, alien_group, player_bullet_group, alien_bullet_group):
        """Initialize the game"""
        # Set game values
        self.round_number = 1
        self.score = 0
        
        self.player = player
        self.background_group = background_group
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        
        # Set sounds and music
        self.new_round_sound = pygame.mixer.Sound("Assets/new_round.wav")
        self.breach_sound = pygame.mixer.Sound("Assets/breach.wav")
        self.alien_hit_sound = pygame.mixer.Sound("Assets/alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("Assets/player_hit.wav")
        
        # Set font
        self.font = pygame.font.Font("Assets/Facon.ttf", 32)
    
    def update(self):
        """Update the game"""
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()
    
    def draw(self):
        """Draw the HUD and other information to display"""
        # Set colors
        WHITE = (255, 255, 255)
        
        # Set text 
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.centerx = WINDOW_WIDTH//2
        score_rect.top = 10
        
        round_text = self.font.render("Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)
        
        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)
        
        # Blit the HUD to the display
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        
        
    def shift_aliens(self):
        """Shift a wave of aliens down the screen and reverse direction"""
        # Determine if alien group has hit an edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= WINDOW_WIDTH:
                shift = True
        
        # Shift every alien down, change the direction, check for a breach
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                # Shift down
                alien.rect.y += 5 * self.round_number
                
                # Reverse the direction and move the alien off the edge so shift doesn't trigger
                alien.direction = -1 * alien.direction
                alien.rect.x += alien.direction * alien.velocity
                
                # Check if an alien reached the ship
                if alien.rect.bottom >= WINDOW_HEIGHT - 70:
                    breach = True
            
            # Aliens breached the line
            if breach:
                self.breach_sound.play()
                self.player.lives -= 1
                self.check_game_status("Aliens breached the line!", "Press 'Enter' to continue")
    
    def check_collisions(self):
        """Check for collisions"""
        # See if any bullet in the player bullet group hit an alien in the alien group
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, True):
            self.alien_hit_sound.play()
            self.score += 100
        
        # See if the player collided with any bullet in the alien bullet group
        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player_hit_sound.play()
            self.player.lives -= 1
            self.check_game_status("You've been hit!", "Press 'Enter' to continue")
            
    def check_round_completion(self):
        """Check to see if a player has completed a single round"""
        # If the alien group is empty you've completed the round
        if not (self.alien_group):
            self.score += 1000 * self.round_number
            self.round_number += 1
            self.start_new_round()
    
    def start_new_round(self):
        """Start a new round"""
        # Give player 1+ lives every round
        self.player.lives += 1
        # Create a grid of Aliens 11 columns and 5 rows
        for i in range(11):
            for j in range(4):
                alien = Alien(64 + i * 64, 64 + j * 64, self.round_number, self.alien_bullet_group)
                self.alien_group.add(alien)
        
        # Pause the game and promt user to start
        self.new_round_sound.play()
        self.pause_game("Space Invaders Round: " + str(self.round_number), "Press 'Enter to begin")
    
    def check_game_status(self, main_text, sub_text):
        """Check to see the status of the game and how the player died"""
        # Empty the bullet groups and reset player and remaining aliens
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()
            
        # Check if the game is over or if it is a simple round reset
        if self.player.lives == 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)
               
    def pause_game(self, main_text, sub_text):
        """Pauses the game"""
        global running
        
        # Set colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        
        # Create main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        
        # Create sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)
        
        # Blit the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()
        
        # Pause the game until the user hits enter
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                # The user wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    sys.exit()
    
    def reset_game(self):
        """Reset the game"""
        self.pause_game("Final Score: " + str(self.score), "Press 'Enter' to play again")
        
        # Reser game values
        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        
        # Empty groups
        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        
        # Start new game
        self.start_new_round()
        