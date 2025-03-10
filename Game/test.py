import pygame

pygame.init()
display_win = pygame.display.set_mode((1000, 1000), flags=pygame.OPENGL | pygame.DOUBLEBUF)
win = pygame.Surface((250, 250))

font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

text = font.render("Text", True, (255, 255, 0))

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window_center = win.get_rect().center

    win.fill(0)
    pygame.draw.circle(win, (255, 0, 0), window_center, 100)
    win.blit(text, text.get_rect(center = window_center))

    scaled_win = pygame.transform.smoothscale(win, display_win.get_size())
    display_win.blit(scaled_win, (0, 0))
    pygame.display.flip()

pygame.quit()
exit()