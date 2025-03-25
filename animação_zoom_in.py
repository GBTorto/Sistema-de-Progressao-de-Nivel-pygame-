import pygame

pygame.init()

# Configuração da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animação de Zoom-in")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
font_size = 10  # Começa pequeno

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Aumenta o tamanho da fonte até um limite
    if font_size < 55:
        font_size += 2  # Aumenta gradualmente o tamanho

    # Renderiza o texto com o novo tamanho
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render("Você upou de nível!", True, GREEN)

    # Desenha no centro da tela
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)  # Controla a velocidade da animação

pygame.quit()
