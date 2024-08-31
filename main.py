import pygame
import sys
import random

# Initialiseer pygame
pygame.init()

# Scherminstellingen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple FPS")

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Speler instellingen
player_size = 50
player_color = BLACK
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_size - 10
player_speed = 5

# Kogel instellingen
bullet_size = 10
bullet_color = RED
bullets = []  # Lijst om alle kogels bij te houden
bullet_speed = 10

# Doel instellingen
target_size = 40
target_color = GREEN
targets = []  # Lijst om alle doelen bij te houden
target_spawn_rate = 30  # Hoeveel frames tussen elk doel dat verschijnt

# Klok voor framerate
clock = pygame.time.Clock()
frame_count = 0

def spawn_target():
    x = random.randint(0, SCREEN_WIDTH - target_size)
    y = random.randint(0, SCREEN_HEIGHT // 2 - target_size)
    return [x, y]

# Hoofdloop van het spel
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Voeg een nieuwe kogel toe bij de positie van de speler
                bullet_x = player_x + player_size // 2 - bullet_size // 2
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])
    
    # Toetsenbord invoer
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Update kogels
    new_bullets = []
    for bullet in bullets:
        bullet[1] -= bullet_speed  # Beweeg kogel omhoog
        if bullet[1] > 0:  # Verwijder kogel als deze uit het scherm is
            new_bullets.append(bullet)
    bullets = new_bullets

    # Update doelen
    new_targets = []
    for target in targets:
        if target[1] < SCREEN_HEIGHT:
            target[1] += 3  # Beweeg doel omlaag
            new_targets.append(target)
    targets = new_targets

    # Kogels raken doelen
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
        for target in targets[:]:
            target_rect = pygame.Rect(target[0], target[1], target_size, target_size)
            if bullet_rect.colliderect(target_rect):
                bullets.remove(bullet)
                targets.remove(target)
                break

    # Spawn nieuwe doelen
    frame_count += 1
    if frame_count % target_spawn_rate == 0:
        targets.append(spawn_target())
    
    # Scherm opvullen met wit
    screen.fill(WHITE)

    # Tekenen van de speler
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Tekenen van de kogels
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_size, bullet_size))

    # Tekenen van de doelen
    for target in targets:
        pygame.draw.rect(screen, target_color, (target[0], target[1], target_size, target_size))

    # Bijwerken van het scherm
    pygame.display.flip()

    # Beperk framerate
    clock.tick(30)