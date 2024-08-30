import pygame
import random
import time
from variable import FOLDER_SOUND, FOLDER_ASSETS, FOLDER_FONTS, WHITE, BLACK, RED, GREEN, BLUE, volume, volume_texts

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Code Defender")

# FPS settings
clock = pygame.time.Clock()
FPS = 60

# Load and resize images
enemy_sprite = pygame.image.load(FOLDER_ASSETS / 'inimigo.png')
enemy_sprite = pygame.transform.scale(enemy_sprite, (50, 50))  # Resize to 50x50 pixels

player_image = pygame.image.load(FOLDER_ASSETS / 'player.png')
player_image = pygame.transform.scale(player_image, (50, 50))  # Resize to 50x50 pixels

background_game = pygame.image.load(FOLDER_ASSETS / 'game_background.jpg')
background_game = pygame.transform.scale(background_game, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_main = pygame.image.load(FOLDER_ASSETS / 'main_background.jpg')
background_main = pygame.transform.scale(background_main, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the bullet sprite
bullet_sprite = pygame.image.load(FOLDER_ASSETS / 'shoot.png')
bullet_sprite = pygame.transform.scale(bullet_sprite, (30, 40))  # Adjust the size as needed

# Fonts
font = pygame.font.SysFont(None, 55)
font_menu_game = pygame.font.SysFont(None, 5)
button_font = pygame.font.Font(FOLDER_FONTS / 'Blank Place.otf', 30)
font_titulo = pygame.font.Font(FOLDER_FONTS / 'BADABB__.TTF', 75)
text_volume_font = pygame.font.SysFont(None, 25)
text_pontuation_font = pygame.font.Font(FOLDER_FONTS / 'Blank Place.otf', 30)

# Enemy Class
class Enemy:
    def __init__(self):
        self.image = enemy_sprite
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH - 50), random.randint(-50, -10)))
        self.speed = random.uniform(1, 3)  # Lower speed range for enemies

    def move(self):
        self.rect.y += self.speed  # Move the enemy down

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Draw the enemy on the screen

    def is_off_screen(self):
        return self.rect.y > SCREEN_HEIGHT  # Check if the enemy has moved off-screen

# Bullet Class
class Bullet:
    def __init__(self, x, y):
        self.image = bullet_sprite
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = -10  # Bullet speed upwards

    def move(self):
        self.rect.y += self.speed  # Move the bullet up

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Draw the bullet on the screen

    def is_off_screen(self):
        return self.rect.y < 0  # Check if the bullet has moved off-screen

# Custom Functions
volume_levels = [0.0, 0.5, 1.0]  # Mute, Medium, High volume levels
current_volume_index = 1  # Start with medium volume
pygame.mixer.music.set_volume(volume_levels[current_volume_index])

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Function for Main Menu
def main_menu():
    global current_volume_index
    global volume

    main_menu_music = pygame.mixer.Sound(FOLDER_SOUND / 'main_menu.mp3')
    main_menu_music.play(-1)

    start_button = pygame.Rect(300, 200, 200, 50)
    volume_button = pygame.Rect(300, 300, 200, 50)
    quit_button = pygame.Rect(300, 400, 200, 50)
    menu_running = True

    while menu_running:
        screen.blit(background_main, (0, 0))
        
        # Add menu text
        menu_text = font_titulo.render('Code Defender', True, GREEN)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 80))

        # Draw buttons
        pygame.draw.rect(screen, GREEN, start_button, border_radius=20)
        pygame.draw.rect(screen, GREEN, volume_button, border_radius=20)
        pygame.draw.rect(screen, RED, quit_button, border_radius=20)
        draw_text('Start Game', button_font, BLACK, screen, 400, 225)
        draw_text('Music Volume', button_font, BLACK, screen, 400, 325)
        draw_text('Exit', button_font, BLACK, screen, 400, 425)

        # Display the current volume
        draw_text(f"Volume: {volume_texts[current_volume_index]}", text_volume_font, WHITE, screen,
                   SCREEN_WIDTH - 70, SCREEN_HEIGHT - 20)

        pygame.display.flip()

        # Handle menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main_menu_music.stop()
                    game_loop()  # Start the game loop
                if volume_button.collidepoint(event.pos):
                    # Toggle volume level
                    current_volume_index = (current_volume_index + 1) % len(volume_levels)
                    main_menu_music.set_volume(volume_levels[current_volume_index])
                    volume = volume_levels[current_volume_index]
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def spawn_enemy(enemies):
    """Create a new enemy and add it to the list."""
    enemy = Enemy()
    enemies.append(enemy)

def player_shoot(bullets, x, y):
    """Create a new player bullet."""
    bullet = Bullet(x + 22, y)  # Adjust bullet position to the player's center
    bullets.append(bullet)
    pygame.mixer.Sound(FOLDER_SOUND / 'shoot.mp3').play(0).set_volume(0.4)

def check_collision(bullets, enemies):
    """Check for collisions between bullets and enemies and remove both upon collision."""
    collision_occurred = False
    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)  # Remove the bullet
                enemies.remove(enemy)  # Remove the enemy
                collision_occurred = True
                break  # Exit loop after removing bullet to avoid iteration errors
    return collision_occurred

def check_collision_player(enemies, player_rect):
    """Check for collisions between the player and enemies."""
    for enemy in enemies:
        if player_rect.colliderect(enemy.rect):
            enemies.remove(enemy)  # Remove the enemy that collided with the player
            return True  # Collision occurred
    return False  # No collision

def game_over():
    """Handle game over state."""
    screen.fill(BLUE)
    font = pygame.font.SysFont(None, 55)
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.mixer.Sound(FOLDER_SOUND / 'game_over.mp3').play()
    time.sleep(2)
    main_menu()  # Return to the main menu after "Game Over"

def game_loop():
    """Main game loop."""
    ambient_music = pygame.mixer.Sound(FOLDER_SOUND / 'game_music.mp3')
    ambient_music.play(loops=-1).set_volume(volume)
    player_rect = player_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))  # Player's sprite
    player_speed = 8

    enemies = []  # List to store enemies
    bullets = []  # List to store bullets
    spawn_timer = 0  # Timer to control enemy spawn
    score = 20  # Player's score

    running = True

    while running:
        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot when the spacebar is pressed
                    player_shoot(bullets, player_rect.x, player_rect.y)
                    score -= 5

        if score < 0:
            ambient_music.stop()
            game_over()
            return  # Return to the main menu after game over
                        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # Screen boundaries
        player_rect.x = max(0, min(SCREEN_WIDTH - player_rect.width, player_rect.x))  # Prevent the player from going off-screen

        # Enemy spawn
        spawn_timer += 1
        if spawn_timer >= 70:  # Every 70 frames
            spawn_enemy(enemies)  # Add an enemy to the list
            spawn_timer = 0  # Reset the spawn timer

        screen.blit(background_game, (0, 0))  # Draw game background

        # Move and draw enemies
        for enemy in enemies:
            enemy.move()
            enemy.draw()
            if enemy.rect.y > SCREEN_HEIGHT:  # If the enemy moves off-screen
                score -= 2  # Penalize the player
                pygame.mixer.Sound(FOLDER_SOUND / 'unpoint.mp3').play()

        # Move and draw bullets
        for bullet in bullets:
            bullet.move()
            bullet.draw()

        # Remove off-screen enemies and bullets
        enemies = [enemy for enemy in enemies if not enemy.is_off_screen()]
        bullets = [bullet for bullet in bullets if not bullet.is_off_screen()]

        # Check for collisions
        if check_collision(bullets, enemies):
            score += 10  # Award points for hitting an enemy
            pygame.mixer.Sound(FOLDER_SOUND / 'point.mp3').play()

        if check_collision_player(enemies, player_rect):
            score -= 10  # Penalize the player for getting hit
            pygame.mixer.Sound(FOLDER_SOUND / 'unpoint.mp3').play()

        # Draw the player
        screen.blit(player_image, player_rect.topleft)

        # Draw the score
        draw_text(f"Score: {score}", text_pontuation_font, WHITE, screen, SCREEN_WIDTH // 2, 50)

        pygame.display.update()

        # Quit the game when the window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Maintain the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main_menu()  # Start the game from the main menu
