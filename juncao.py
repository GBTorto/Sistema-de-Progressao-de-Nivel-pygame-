import pygame
from teste_design import Menu
from upar_nivel import Combate

tamanho_menu_img_x = 0
tamanho_menu_img_y = 0

menu = Menu(5, 5, 5, 5, 5, 1, 1, 1, 1, 1)
combate = Combate()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Loop do jogo
def game_loop():
    running = True
    while running:
        combate.movimentacao()
        combate.atualizar_xp(screen, WIDTH, HEIGHT)
        combate.render(screen)

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

            if combate.show_menu and menu.tamanho_menu_img_x == 600 and menu.tamanho_menu_img_y == 400:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for atributo, botoes in menu.botoes.items():
                        # Botão de diminuir
                        if botoes["diminuir"]["rect"].collidepoint(event.pos) and combate.pontos_disponiveis < combate.pontos_disponiveis_copy:
                            if menu.valores[atributo] > menu.valores_copy[atributo]:  # Impede de reduzir abaixo do inicial
                                menu.valores[atributo] -= 1
                                botoes["diminuir"]["pressionado"] = True
                                combate.pontos_disponiveis += 1  # Devolve um ponto

                                if atributo == "ataque":
                                    menu.atributos[atributo] -= 1.25
                                    combate.dano -= 10
                                if atributo == "defesa":
                                    menu.atributos[atributo] -= 1
                                if atributo == "vida":
                                    menu.atributos[atributo] -= 0.5
                                if atributo == "stamina":
                                    menu.atributos[atributo] -= 1.25
                                if atributo == "velocidade":
                                    menu.atributos[atributo] -= 2
                                    combate.player_speed -= 1

                                print(menu.atributos[atributo])

                        # Botão de aumentar
                        if botoes["aumentar"]["rect"].collidepoint(event.pos) and combate.pontos_disponiveis > 0:
                            menu.valores[atributo] += 1
                            botoes["aumentar"]["pressionado"] = True
                            combate.pontos_disponiveis -= 1  # Gasta um ponto

                            if atributo == "ataque":
                                menu.atributos[atributo] += 1.25
                                combate.dano += 10
                            if atributo == "defesa":
                                menu.atributos[atributo] += 1
                            if atributo == "vida":
                                menu.atributos[atributo] += 0.5
                            if atributo == "stamina":
                                menu.atributos[atributo] += 1.25
                            if atributo == "velocidade":
                                menu.atributos[atributo] += 2
                                combate.player_speed += 1
                            
                            print(menu.atributos[atributo])

                    # Confirma os valores ao pressionar ENTER
                    if event.type == pygame.K_KP_ENTER:
                        menu.valores_copy = menu.valores.copy()

        if combate.show_menu and menu.tamanho_menu_img_x < 600 and menu.tamanho_menu_img_y < 400:
            menu.tamanho_menu_img_x += 30  # Ajuste a velocidade do zoom
            menu.tamanho_menu_img_y += 20
            menu.menu_img = pygame.transform.scale(menu.menu_img_original, (menu.tamanho_menu_img_x, menu.tamanho_menu_img_y))
        elif not combate.show_menu and menu.tamanho_menu_img_x > 0 and menu.tamanho_menu_img_y > 0:
            menu.tamanho_menu_img_x = max(0, menu.tamanho_menu_img_x - 30)
            menu.tamanho_menu_img_y = max(0, menu.tamanho_menu_img_y - 20)

            if menu.tamanho_menu_img_x > 0 and menu.tamanho_menu_img_y > 0:
                menu.menu_img = pygame.transform.scale(menu.menu_img_original, (menu.tamanho_menu_img_x, menu.tamanho_menu_img_y))


                
        # Atualiza o jogo se o menu NÃO estiver aberto
        if not combate.show_menu:
            combate.movimentacao()
            combate.render(screen)
            combate.atualizar_xp(screen, WIDTH, HEIGHT)
        else:
            # Exibe o menu na tela 
            screen.blit(menu.menu_img,((WIDTH // 2) - (menu.tamanho_menu_img_x // 2),(HEIGHT // 2) - (menu.tamanho_menu_img_y // 2)))
            if menu.tamanho_menu_img_x > 500 and menu.tamanho_menu_img_y > 333:
                # Posição do menu
                menu.desenhar_valores(screen, combate.font_nivel, combate.text_nivel, combate.nivel, combate.pontos_disponiveis)
                menu.atualizar_sprites()
                menu.desenhar_botoes(screen)
                menu.resetar_botoes()   

        pygame.display.flip()
        combate.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()