import pygame

pygame.init()

# Configuração da tela
width, height = 1000, 800
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption("Redimensionar Imagem")

# Carregar imagem
menu_img = pygame.image.load("Imagem menu/menu.png")
menu_img = pygame.transform.scale(menu_img, (400, 600))

# Fonte
tamanho_fonte = 100

class Menu():
    def __init__(self, valor_ataque, valor_defesa, valor_vida, valor_stamina, valor_velocidade):
        self.valores = {
            "ataque": valor_ataque,
            "defesa": valor_defesa,
            "vida": valor_vida,
            "stamina": valor_stamina,
            "velocidade": valor_velocidade
        }

        # Carregar imagens dos botões
        # self.botao_mais = pygame.image.load('Spritesheet/SpriteSheet_mais.png')
        self.botao_menos = pygame.image.load('Spritesheet/spritesheet_menos.png')

        # Criar dicionário para armazenar botões e suas posições
        self.botoes = {}
        for i, atributo in enumerate(self.valores.keys()):
            x, y = 600, 100 + i * 80  # Posiciona os botões verticalmente
            
            self.botoes[atributo] = {
                # "aumentar": {"imagem": self.botao_mais, "rect": pygame.Rect(x + 50, y, 30, 30)},
                "diminuir": {"imagem": self.botao_menos, "rect": pygame.Rect(x, y, 30, 30)}
            }

menu = Menu(10, 5, 20, 8, 15)

# Loop principal
running = True
while running:
    tela.fill((255, 255, 255))  # Limpar tela

    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for atributo, botoes in menu.botoes.items():
                # if botoes["aumentar"]["rect"].collidepoint(event.pos):
                #     menu.valores[atributo] += 1  # Aumenta o valor do atributo
                if botoes["diminuir"]["rect"].collidepoint(event.pos):
                    menu.valores[atributo] -= 1  # Diminui o valor do atributo
                    print(menu.valores[atributo])


    # Desenhar a imagem redimensionada
    tela.blit(menu_img, (200, 00))  # Posição na tela
    # Desenhar os botões
    for atributo, botoes in menu.botoes.items():
        # tela.blit(botoes["aumentar"]["imagem"], botoes["aumentar"]["rect"].topleft)
        tela.blit(botoes["diminuir"]["imagem"], botoes["diminuir"]["rect"].topleft)

    # Atributos
    fonte = pygame.font.SysFont(None, tamanho_fonte)

    pygame.display.update()  # Atualiza a tela

pygame.quit()
