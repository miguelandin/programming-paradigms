import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

rectH = pygame.Rect(250, 0, 250, 720)
rectW = pygame.Rect(0, 250, 1280, 250)


def isOnRect(rect: pygame.Rect, pos) -> bool:
    left, top, w, h = rect
    mx, my = pos
    return (mx >= left and mx <= w + left and my >= top and my <= h + top)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    pygame.draw.rect(screen, "blue", rectH)
    pygame.draw.rect(screen, "blue", rectW)
    pos = (pygame.mouse.get_pos())
    if (isOnRect(rectH, pos) or isOnRect(rectW, pos)):
        print("AZUL")
    else:
        print("BLANCO")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
