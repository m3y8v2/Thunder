import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Thunder!')

pygame.mixer.music.load('assets/thunder.mp3')

pygame.mixer.music.play(-1)

background_img = pygame.image.load('assets/background.jpg').convert()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_img = pygame.image.load('assets/player.png').convert_alpha()  
enemy_img = pygame.image.load('assets/enemy.png').convert_alpha()    
bullet_img = pygame.image.load('assets/bullet.png').convert_alpha()  

font = pygame.font.Font(None, 36)

player_speed = 5
enemies = pygame.sprite.Group()  
enemy_speed = 3
enemy_spawn_rate = 60  
enemy_bullet_rate = 100   
enemy_bullet_timer = enemy_bullet_rate  
bullet_speed = 10
bullets = pygame.sprite.Group()  
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += player_speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= player_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += player_speed

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def shoot_bullet(self):
        bullet_x = self.rect.centerx - bullet_img.get_width() // 2
        bullet_y = self.rect.top
        bullet = Bullet(bullet_x, bullet_y, True)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.bullet_timer = random.randint(0, enemy_bullet_rate)

    def update(self):
        self.rect.y += enemy_speed
        self.bullet_timer += 1
        if self.bullet_timer >= enemy_bullet_rate:
            self.bullet_timer = 0
            self.shoot_bullet()

    def shoot_bullet(self):
        bullet = Bullet(self.rect.centerx - bullet_img.get_width() // 2, self.rect.bottom, False)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player_bullet=False):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_player_bullet = is_player_bullet  

    def update(self):
        if self.is_player_bullet:
            self.rect.y -= bullet_speed
            # Check collision with enemies
            enemy_hit_list = pygame.sprite.spritecollide(self, enemies, True)
            if enemy_hit_list:
                self.kill()
                global score
                score += 100
        else:
            self.rect.y += bullet_speed
            # Check collision with player
            player_hit_list = pygame.sprite.spritecollide(self, [player], False)
            if player_hit_list:
                global game_state
                game_state = GAME_OVER

        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

player = Player()

GAME_RUNNING = 1
GAME_OVER = 2
game_state = GAME_RUNNING

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(background_img, (0, 0))  

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_RUNNING:
                if event.key == pygame.K_SPACE:
                    player.shoot_bullet()
            elif game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                    enemies.empty()
                    bullets.empty()
                    score = 0
                    game_state = GAME_RUNNING

    if game_state == GAME_RUNNING:
        
        player.update(keys)

        
        if random.randint(1, enemy_spawn_rate) == 1:
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_img.get_width())
            enemy_y = -enemy_img.get_height()
            enemy = Enemy(enemy_x, enemy_y)
            enemies.add(enemy)

        
        bullets.update()
        enemies.update()

        for enemy in enemies:
            if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
                game_state = GAME_OVER

        
        screen.blit(player.image, player.rect)
        enemies.draw(screen)
        bullets.draw(screen)

        
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_state == GAME_OVER:
        
        game_over_text = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(game_over_text, game_over_rect)

        
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
