import pygame
import sys
from core.bspline import BSplineInterpolation

def run():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    interpolator = BSplineInterpolation()

    running = True
    while running:
        for event in pygame.event.get():
            interpolator.handle_sliders(event) 

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    interpolator.selected_point = interpolator.find_point(*event.pos)
                elif event.button == 3:
                    interpolator.add_point(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                interpolator.selected_point = None
            elif event.type == pygame.MOUSEMOTION and interpolator.selected_point:
                interpolator.selected_point['x'], interpolator.selected_point['y'] = event.pos
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    interpolator.show_global_approx = not interpolator.show_global_approx
                elif event.key == pygame.K_a:
                    interpolator.show_lower_order = not interpolator.show_lower_order

        interpolator.draw(screen, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
