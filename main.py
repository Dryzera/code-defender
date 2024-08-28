import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Code Defender")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Taxa de FPS
clock = pygame.time.Clock()
FPS = 60

# Classe Inimigo
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(-50, -10), 50, 50)
        self.speed = random.uniform(1, 3)  # Reduzido para uma faixa menor

    def move(self):
        self.rect.y += self.speed  # Move o inimigo para baixo

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)  # Desenha o inimigo

    def is_off_screen(self):
        return self.rect.y > SCREEN_HEIGHT  # Verifica se o inimigo saiu da tela

# Classe Tiro
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = -10  # Velocidade do tiro para cima

    def move(self):
        self.rect.y += self.speed  # Move o tiro para cima

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)  # Desenha o tiro

    def is_off_screen(self):
        return self.rect.y < 0  # Verifica se o tiro saiu da tela

# Funções Personalizadas
def main_menu():
    """Exibe o menu principal do jogo."""
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 55)
        text = font.render("Pressione ESPAÇO para Iniciar", True, WHITE)
        screen.blit(text, (100, 250))
        pygame.display.flip()

        # Eventos do Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False  # Inicia o jogo

def spawn_enemy(enemies):
    """Cria um novo inimigo e o adiciona à lista."""
    enemy = Enemy()
    enemies.append(enemy)

def player_shoot(bullets, x, y):
    """Cria um novo tiro do jogador."""
    bullet = Bullet(x + 22, y)  # Ajuste a posição do tiro para o centro do jogador
    bullets.append(bullet)

def check_collision(bullets, enemies):
    """Verifica colisões entre tiros e inimigos e remove ambos em caso de colisão."""
    for bullet in bullets[:]:  # Itera sobre uma cópia da lista para evitar problemas durante a remoção
        for enemy in enemies[:]:  # Itera sobre uma cópia da lista para evitar problemas durante a remoção
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                return True  # Retorna True para indicar que uma colisão ocorreu
    return False

def check_collision_player(enemies, player_rect):
    """Verifica colisões entre o jogador e os inimigos."""
    for enemy in enemies[:]:  # Itera sobre uma cópia da lista para evitar problemas durante a remoção
        if enemy.rect.colliderect(player_rect):
            enemies.remove(enemy)
            return True  # Retorna True para indicar que uma colisão ocorreu
    return False

def game_loop():
    """Loop principal do jogo."""
    player_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 50, 50)  # Representação do jogador
    player_speed = 8

    enemies = []  # Lista para armazenar os inimigos
    bullets = []  # Lista para armazenar os tiros
    spawn_timer = 0  # Temporizador para controlar o spawn de inimigos
    score = 0  # Pontuação do jogador

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

        # Movimento do Jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # Limites da Tela
        player_rect.x = max(0, min(SCREEN_WIDTH - player_rect.width, player_rect.x))  # Impede que o jogador saia da tela

        # Spawn de Inimigos
        if spawn_timer >= 60:  # A cada 60 quadros (1 segundo)
            spawn_enemy(enemies)
            spawn_timer = 0
        else:
            spawn_timer += 1

        # Movimento e Desenho dos Inimigos
        screen.fill(BLACK)  # Limpa a tela
        for enemy in enemies:
            enemy.move()
            enemy.draw()

        # Movimento e Desenho dos Tiros
        for bullet in bullets:
            bullet.move()
            bullet.draw()

        # Remover Inimigos Fora da Tela
        enemies = [enemy for enemy in enemies if not enemy.is_off_screen()]

        # Remover Tiros Fora da Tela
        bullets = [bullet for bullet in bullets if not bullet.is_off_screen()]

        # Verificação de Colisão
        if check_collision(bullets, enemies):
            score += 10  # Incrementa a pontuação em 10 para cada inimigo destruído

        # Verificação de Colisão com o Jogador
        if check_collision_player(enemies, player_rect):
            score -= 10  # Diminui a pontuação em 10 para cada colisão com o jogador
            if score < 0:
                screen.fill(BLUE)
                font = pygame.font.SysFont(None, 55)
                text = font.render("GAME OVER", True, WHITE)
                screen.blit(text, (100, 250))
                pygame.display.update()
                time.sleep(2)
                break
                
        # Desenha o Jogador
        pygame.draw.rect(screen, RED, player_rect)  # Desenha o jogador

        # Exibe a Pontuação
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()  # Atualiza a tela

        # Controle de FPS
        clock.tick(FPS)

    pygame.quit()

# Execução do Jogo
if __name__ == "__main__":
    main_menu()  # Exibe o menu principal
    game_loop()  # Inicia o loop principal do jogo
