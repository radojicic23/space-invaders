import pygame, random 

from GUI.display import WINDOW_WIDTH, WINDOW_HEIGHT


# Deffine bullet classes
class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the player"""
    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/green_laser.png"), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.velocity = 10
        bullet_group.add(self)
    
    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity
        
        # If the bullet is off the screen, kill it
        if self.rect.bottom < 0:
            self.kill()
        
        # Update player bullet
        self.mask = pygame.mask.from_surface(self.image)
        

class AlienBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the alien"""
    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/red_laser.png"), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.velocity = 10
        bullet_group.add(self)
    
    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity
        
        # If the bullet is off the screen, kill it
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
            
        # Update Alien Bullet mask
        self.mask = pygame.mask.from_surface(self.image)
