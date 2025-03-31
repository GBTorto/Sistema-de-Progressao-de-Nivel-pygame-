import pygame
from teste_design import Menu
from upar_nivel import Combate

menu = Menu(5, 5, 5, 5, 5)
combate = Combate()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Loop do jogo
def game_loop():
    running = True
    while running:
        combate.movimentacao()
        combate.atualizar_xp()
        combate.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not combate.show_menu:
                    combate.attack(combate.dano)  # Ataca quando o espaço é pressionado

                if event.key == pygame.K_m:
                    combate.show_menu = not combate.show_menu

            if combate.show_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu.processar_eventos(event)
        # Atualiza o jogo se o menu NÃO estiver aberto
        if not combate.show_menu:
            combate.movimentacao()
            combate.atualizar_xp()
            combate.render()
        else:
            # Exibe o menu na tela
            screen.blit(menu.menu_img, (200, 50))  # Posição do menu
            menu.desenhar_valores(screen)


        pygame.display.flip()
        combate.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()