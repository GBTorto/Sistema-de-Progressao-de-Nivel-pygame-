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
        combate.atualizar_xp(screen, WIDTH, HEIGHT)
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
                        menu.valores_copy = menu.valores.copy()  # Salva os valores antes de editar

            if combate.show_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for atributo, botoes in menu.botoes.items():
                        # Botão de diminuir
                        if botoes["diminuir"]["rect"].collidepoint(event.pos) and combate.pontos_disponiveis < combate.pontos_disponiveis_copy:
                            if menu.valores[atributo] > menu.valores_copy[atributo]:  # Impede de reduzir abaixo do inicial
                                menu.valores[atributo] -= 1
                                botoes["diminuir"]["pressionado"] = True
                                combate.pontos_disponiveis += 1  # Devolve um ponto

                        # Botão de aumentar
                        if botoes["aumentar"]["rect"].collidepoint(event.pos) and combate.pontos_disponiveis > 0:
                            menu.valores[atributo] += 1
                            botoes["aumentar"]["pressionado"] = True
                            combate.pontos_disponiveis -= 1  # Gasta um ponto

                    # Confirma os valores ao pressionar ENTER
                    if event.type == pygame.K_KP_ENTER:
                        menu.valores_copy = menu.valores.copy()

        # Atualiza o jogo se o menu NÃO estiver aberto
        if not combate.show_menu:
            combate.movimentacao()
            combate.render()
            combate.atualizar_xp(screen, WIDTH, HEIGHT)
        else:
            # Exibe o menu na tela 
            screen.blit(menu.menu_img, (200, 50))  # Posição do menu
            menu.desenhar_valores(screen)
            menu.atualizar_sprites()
            menu.desenhar_botoes(screen)
            menu.resetar_botoes()

        pygame.display.flip()
        combate.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
