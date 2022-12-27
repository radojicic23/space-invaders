import pygame, random
from GUI.display import WINDOW_WIDTH, WINDOW_HEIGHT
from GUI.bullet import PlayerBullet


class Player(pygame.sprite.Sprite):
    """A class to model a spaceship the user can controll"""
    def __init__(self, bullet_group):
        """Initialize the player"""
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/space_ship.png"), (80, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT
        
        self.lives = 5
        self.velocity = 9
        
        self.bullet_group = bullet_group
        
        self.shoot_sound = pygame.mixer.Sound("Assets/player_fire.wav")
    
    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()
        
        # Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        
        # Update player mask 
        self.mask = pygame.mask.from_surface(self.image)
    
    def fire(self):
        """Fire a bullet"""
        # Restrict the number of bullets on screen at a time
        if len(self.bullet_group) < 3:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)
    
    def reset(self):
        """Reset the player position"""
        self.rect.centerx = WINDOW_WIDTH//2
    
 