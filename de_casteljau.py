import pygame
import numpy as np
import sys


class DeCasteljau:
    def __init__(self):
        self._points = [
            [100.0, 300.0],
            [300.0, 100.0],
            [500.0, 300.0]
        ]
        self.selected_point = None
        self.t_value = 0.5

    def de_casteljau(self, t):

        points = np.array(self._points, dtype=float).copy()
        n = len(points)
        intermediate_steps = []

        for r in range(1, n):
            new_points = []
            for i in range(n - r):
                points[i] = (1 - t) * points[i] + t * points[i + 1]
                new_points.append(points[i].copy())
            intermediate_steps.append(new_points)
        return tuple(points[0]), intermediate_steps

    def find_point(self, x, y):
        for point in self._points:
            if ((point[0] - x) ** 2 + (point[1] - y) ** 2) ** 0.5 < 10:
                return point
        return None

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for point in self._points:
            pygame.draw.circle(screen, (0, 0, 255), (int(point[0]), int(point[1])), 5)

        curve_points = []
        all_intermediate_steps = []
        for t in np.linspace(0, 1, 101):
            bezier_point, intermediate_step = self.de_casteljau(self.t_value)
            bezier_point, intermediate_steps = self.de_casteljau(t)
            curve_points.append(bezier_point)
            all_intermediate_steps.append(intermediate_step)

        for i in range(len(curve_points) - 1):
            pygame.draw.line(screen, (255, 0, 0), curve_points[i], curve_points[i + 1], 2)

        for step in all_intermediate_steps:
            for line_points in step:
                for i in range(len(line_points) - 1):
                    pygame.draw.line(screen, (0, 255, 0), line_points[i], line_points[i + 1], 1)


        pygame.draw.rect(screen, (200, 200, 200), (100, 550, 600, 10))
        pygame.draw.circle(screen, (0, 0, 0), (int(100 + self.t_value * 600), 555), 8)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 100 <= event.pos[0] <= 700 and 545 <= event.pos[1] <= 565:
                        self.t_value = (event.pos[0] - 100) / 600
                    else:
                        self.selected_point = self.find_point(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.selected_point = None
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        if 100 <= event.pos[0] <= 700:
                            self.t_value = (event.pos[0] - 100) / 600
                        elif self.selected_point:
                            self.selected_point[0], self.selected_point[1] = float(event.pos[0]), float(event.pos[1])

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    interpolator = DeCasteljau()
    interpolator.run()