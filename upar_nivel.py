import pygame

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
xp_limitador = 0
xp_max = 100
nivel = 1
nivel_anterior = nivel
dano = 15
multiplicador_xp = 1.1
temporizador_mensagem = None

# Variáveis xp
xp_width = 200
xp_height = 20
pos_xp_x = (WIDTH // 2) - (xp_width // 2)
pos_xp_y = HEIGHT - (xp_height * 2)
xp_ratio = 0
temporizador_xp = None
ganhando_xp = False

# Distribuição de pontos
pontos_disponiveis = 0

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

    # Desenha a barra de xp
    barra_xp = pygame.draw.rect(screen, WHITE, (pos_xp_x, pos_xp_y, xp_width, xp_height))
    barra_xp_preenchida = pygame.draw.rect(screen, GREEN, (pos_xp_x, pos_xp_y, 0 + xp_ratio, xp_height))

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_d] and player.x < WIDTH - player_size:
        player.x += player_speed
    if keys[pygame.K_w] and player.y > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.y < HEIGHT - player_size:
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
    if enemy_health == 0 and not ganhando_xp:
        temporizador_xp = pygame.time.get_ticks()
        ganhando_xp = True
        xp_limitador += 50

    if ganhando_xp:
        if xp <= xp_limitador and pygame.time.get_ticks() - temporizador_xp > 30: 
            xp += 5
            xp_ratio = (xp / xp_max) * 200
            temporizador_xp = pygame.time.get_ticks()
        elif xp > xp_limitador - 5:
            ganhando_xp = False


        # print(xp_ratio)
        # print(xp)
        enemy_health = 100

    if  xp >= xp_max and temporizador_mensagem is None:
        temporizador_mensagem = pygame.time.get_ticks()

        nivel += 1
        pontos_disponiveis += 5
        pontos_disponiveis_copy = pontos_disponiveis
        print(nivel)

        xp_excedente = xp_limitador - xp_max
        xp_max *= multiplicador_xp
        print(xp_max)
        print(xp_excedente)
        xp = 0
        xp_limitador = xp_excedente
        xp_ratio = (xp / xp_max) * 200
        
        # print(f"{xp_max:.2f}")

    if nivel_anterior < nivel:
        nivel_anterior = nivel
        dano += 10
    
    if temporizador_mensagem is not None:
        font = pygame.font.SysFont(None, 55)
        text = font.render("Você upou de nível", True, GREEN)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
        if pygame.time.get_ticks() - temporizador_mensagem > 1500:
            temporizador_mensagem = None

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                attack(dano)
                # print(dano)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()