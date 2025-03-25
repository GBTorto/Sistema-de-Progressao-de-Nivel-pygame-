import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema de Combate Simples")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Parâmetros do jogador e inimigo
player_size = 50
player_speed = 5
player = pygame.Rect(WIDTH // 4, HEIGHT // 2, player_size, player_size)

enemy_size = 50
enemy = pygame.Rect(WIDTH * 3 // 4, HEIGHT // 2, enemy_size, enemy_size)

# Barra de vida do inimigo
enemy_health = 100
max_health = 100

# Sistema de xp
xp = 0
xp_max = 100
nivel = 1
nivel_anterior = nivel
dano = 15
multiplicador_xp = 1.1

# Função para desenhar a barra de vida
def draw_health_bar(x, y, health, max_health):
    health_width = 200
    health_height = 20
    health_ratio = health / max_health
    pygame.draw.rect(screen, RED, (x, y, health_width, health_height))
    pygame.draw.rect(screen, GREEN, (x, y, health_width * health_ratio, health_height))

# Função para atacar
def attack(dano):
    global enemy_health
    damage = dano
    enemy_health -= damage
    if enemy_health < 0:
        enemy_health = 0

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLUE)  # Cor de fundo

    # Desenha o jogador (quadrado azul)
    pygame.draw.rect(screen, WHITE, player)

    # Desenha o inimigo (quadrado vermelho)
    pygame.draw.rect(screen, RED, enemy)

    # Desenha a barra de vida do inimigo
    draw_health_bar(enemy.x, enemy.y - 30, enemy_health, max_health)

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
        player.x += player_speed
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.y < HEIGHT - player_size:
        player.y += player_speed

    # Inimigo se move automaticamente
    if enemy.x > player.x:
        enemy.x -= 1
    elif enemy.x < player.x:
        enemy.x += 1

    if enemy.y > player.y:
        enemy.y -= 1
    elif enemy.y < player.y:
        enemy.y += 1

    # Verifica se o inimigo morreu
    while enemy_health == 0:
        xp += 100
        print(xp)
        enemy_health = 100

    if  xp >= xp_max:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Você upou de nível", True, GREEN)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))

        nivel += 1
        print(nivel)

        xp_max *= multiplicador_xp
        xp = xp - xp_max
        print(f"{xp_max:.2f}")

    if nivel_anterior < nivel:
        nivel_anterior = nivel
        print(nivel_anterior)
        dano += 10

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                attack(dano)
                print(dano)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()