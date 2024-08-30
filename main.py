import pygame
import random
import time
from variable import FOLDER_SOUND, FOLDER_ASSETS, WHITE, BLACK, RED, GREEN, BLUE, volume

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Code Defender")

# Taxa de FPS
clock = pygame.time.Clock()
FPS = 60

# Carregar e redimensionar imagens
enemy_sprite = pygame.image.load(FOLDER_ASSETS / 'inimigo.png')
enemy_sprite = pygame.transform.scale(enemy_sprite, (50, 50))  # Redimensiona para 50x50 pixels

player_image = pygame.image.load(FOLDER_ASSETS / 'player.png')
player_image = pygame.transform.scale(player_image, (50, 50))  # Redimensiona para 50x50 pixels

background_game = pygame.image.load(FOLDER_ASSETS / 'game_background.jpg')
background_game = pygame.transform.scale(background_game, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_main = pygame.image.load(FOLDER_ASSETS / 'main_background.jpg')
background_main = pygame.transform.scale(background_main, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar o sprite do tiro
bullet_sprite = pygame.image.load(FOLDER_ASSETS / 'shoot.png')
bullet_sprite = pygame.transform.scale(bullet_sprite, (30, 40))  # Ajuste o tamanho conforme necessário

font = pygame.font.SysFont(None, 55)
button_font = pygame.font.SysFont(None, 45)

# Classe Inimigo
class Enemy:
    def __init__(self):
        self.image = enemy_sprite
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH - 50), random.randint(-50, -10)))
        self.speed = random.uniform(1, 3)  # Reduzido para uma faixa menor

    def move(self):
        self.rect.y += self.speed  # Move o inimigo para baixo

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Desenha o inimigo

    def is_off_screen(self):
        return self.rect.y > SCREEN_HEIGHT  # Verifica se o inimigo saiu da tela

# Classe Tiro
class Bullet:
    def __init__(self, x, y):
        self.image = bullet_sprite
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = -10  # Velocidade do tiro para cima

    def move(self):
        self.rect.y += self.speed  # Move o tiro para cima

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Desenha o tiro usando o sprite

    def is_off_screen(self):
        return self.rect.y < 0  # Verifica se o tiro saiu da tela

# Funções Personalizadas
volume_levels = [0.0, 0.5, 1.0]  # Mudo, Médio, Alto
current_volume_index = 1  # Começar com volume médio
pygame.mixer.music.set_volume(volume_levels[current_volume_index])

# Função para desenhar o texto na tela
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Função para o Menu Principal
def main_menu():
    main_menu_music = pygame.mixer.Sound(FOLDER_SOUND / 'main_menu.mp3')
    main_menu_music.play(-1)
    
    start_button = pygame.Rect(300, 200, 200, 50)
    volume_button = pygame.Rect(300, 300, 200, 50)
    quit_button = pygame.Rect(300, 400, 200, 50)
    menu_running = True

    while menu_running:
        screen.blit(background_main, (0, 0))
        
        # Adiciona o texto do menu
        menu_text = font.render('Code Defender', True, GREEN)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 80))  # Ajusta a posição do texto do menu

        # Desenhar botões
        pygame.draw.rect(screen, GREEN, start_button, border_radius=20)
        pygame.draw.rect(screen, GREEN, volume_button, border_radius=20)
        pygame.draw.rect(screen, RED, quit_button, border_radius=20)
        draw_text('Iniciar Jogo', button_font, BLACK, screen, 400, 225)
        draw_text('Volume', button_font, BLACK, screen, 400, 325)
        draw_text('Sair do Jogo', button_font, BLACK, screen, 400, 425)

        pygame.display.flip()

        # Eventos do Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    main_menu_music.stop()
                    game_loop()  # Inicia o loop do jogo
                if volume_button.collidepoint(event.pos):
                    # Alterna o nível de volume
                    global current_volume_index
                    current_volume_index = (current_volume_index + 1) % len(volume_levels)
                    main_menu_music.set_volume(volume_levels[current_volume_index])
                    global volume
                    volume = volume_levels[current_volume_index]
                    print(f"Volume: {volume_levels[current_volume_index] * 100}%")
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def spawn_enemy(enemies):
    """Cria um novo inimigo e o adiciona à lista."""
    enemy = Enemy()
    enemies.append(enemy)

def player_shoot(bullets, x, y):
    """Cria um novo tiro do jogador."""
    bullet = Bullet(x + 22, y)  # Ajuste a posição do tiro para o centro do jogador
    bullets.append(bullet)
    pygame.mixer.Sound(FOLDER_SOUND / 'shoot.mp3').play(0).set_volume(0.4)

def check_collision(bullets, enemies):
    """Verifica colisões entre tiros e inimigos e remove ambos em caso de colisão."""
    collision_occurred = False
    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)  # Remove o tiro
                enemies.remove(enemy)  # Remove o inimigo
                collision_occurred = True
                break  # Sai do loop após remover o tiro para evitar erros de iteração
    return collision_occurred

def check_collision_player(enemies, player_rect):
    """Verifica colisões entre o jogador e inimigos."""
    for enemy in enemies:
        if player_rect.colliderect(enemy.rect):
            enemies.remove(enemy)  # Remove o inimigo que colidiu com o jogador
            return True  # Colisão ocorreu
    return False  # Sem colisão

def game_over():
    screen.fill(BLUE)
    font = pygame.font.SysFont(None, 55)
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.mixer.Sound(FOLDER_SOUND / 'game_over.mp3').play()
    time.sleep(2)
    main_menu()  # Retorna ao menu principal após o "Game Over"

def game_loop():
    """Loop principal do jogo."""
    ambient_music = pygame.mixer.Sound(FOLDER_SOUND / 'game_music.mp3')
    ambient_music.play(loops=-1).set_volume(volume)
    player_rect = player_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))  # Usa o sprite do jogador
    player_speed = 8

    enemies = []  # Lista para armazenar os inimigos
    bullets = []  # Lista para armazenar os tiros
    spawn_timer = 0  # Temporizador para controlar o spawn de inimigos
    score = 20  # Pontuação do jogador

    # Variável de execução do jogo
    running = True

    while running:
        # Eventos de Jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Atira quando a barra de espaço é pressionada
                    player_shoot(bullets, player_rect.x, player_rect.y)
                    score -= 5

        if score < 0:
            ambient_music.stop()
            game_over()
            return  # Retorna para o menu principal após o game over
                        
        # Movimento do Jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # Limites da Tela
        player_rect.x = max(0, min(SCREEN_WIDTH - player_rect.width, player_rect.x))  # Impede que o jogador saia da tela

        # Spawn de Inimigos
        spawn_timer += 1
        if spawn_timer >= 90:  # A cada 90 frames
            spawn_enemy(enemies)  # Adiciona um inimigo à lista
            spawn_timer = 0  # Reseta o temporizador

        # Desenhar o Fundo
        screen.blit(background_game, (0, 0))  # Fundo estático

        # Atualizar e Desenhar Inimigos
        for enemy in enemies:
            enemy.move()  # Mover o inimigo para baixo
            enemy.draw()  # Desenha o inimigo na tela

        # Atualizar e Desenhar Tiros
        for bullet in bullets:
            bullet.move()  # Move o tiro para cima
            bullet.draw()  # Desenha o tiro na tela

        # Remover Inimigos Fora da Tela
        enemies = [enemy for enemy in enemies if not enemy.is_off_screen()]

        # Remover Tiros Fora da Tela
        bullets = [bullet for bullet in bullets if not bullet.is_off_screen()]

        # Verificar Colisões
        if check_collision(bullets, enemies):
            score += 10  # Incrementa a pontuação para cada inimigo destruído
            pygame.mixer.Sound(FOLDER_SOUND / 'point.mp3').play()

        # Verificar Colisões com o Jogador
        if check_collision_player(enemies, player_rect):
            score -= 10  # Diminui a pontuação para cada colisão com o jogador
            pygame.mixer.Sound(FOLDER_SOUND / 'unpoint.mp3').play()

        # Desenhar o Jogador
        screen.blit(player_image, player_rect.topleft)  # Usa o sprite do jogador

        # Mostrar Pontuação
        draw_text(f"Pontuação: {score}", font, WHITE, screen, SCREEN_WIDTH // 2, 50)

        # Adicionar Botão de Menu
        menu_button = pygame.Rect(SCREEN_WIDTH - 80, 20, 60, 30)
        pygame.draw.rect(screen, GREEN, menu_button, border_radius=10)
        draw_text('Menu', button_font, BLACK, screen, SCREEN_WIDTH - 50, 35)

        pygame.display.update()

        # Eventos do Botão de Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('cheg')
                if menu_button.collidepoint(event.pos):
                    ambient_music.stop()
                    main_menu()  # Volta para o menu principal

        # Controlar o FPS
        clock.tick(FPS)

    pygame.quit()

# Inicializar o Menu Principal

if __name__ == '__main__':
    main_menu()
