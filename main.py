import pygame

pygame.init()

# Screen
WIDTH = 300
win = pygame.display.set_mode((WIDTH, WIDTH))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def render():
    win.fill(WHITE)
    pygame.display.update()


def main():
    run = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        render()


if __name__ == '__main__':
    main()
