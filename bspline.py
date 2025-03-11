import pygame
import sys
import scipy.interpolate as si
import numpy as np


class BSplineInterpolation:
    def __init__(self):
        self._points = [
            {'x': 100 + i * 100, 'y': 300 if i % 2 == 0 else 100} for i in range(8)
        ]
        self.selected_point = None
        self.k = 4

    def basis_function(self, i, k, t, knots):
        if k == 1:
            return 1.0 if knots[i] <= t < knots[i + 1] else 0.0
        else:
            denom1 = knots[i + k - 1] - knots[i]
            term1 = 0.0 if denom1 == 0 else (t - knots[i]) / denom1 * self.basis_function(i, k - 1, t, knots)
            denom2 = knots[i + k] - knots[i + 1]
            term2 = 0.0 if denom2 == 0 else (knots[i + k] - t) / denom2 * self.basis_function(i + 1, k - 1, t, knots)
            return term1 + term2

    def compute_bspline(self, num_points=100):
        n = len(self._points)
        knots = np.linspace(0, 1, n + self.k)
        t_values = np.linspace(knots[self.k - 1], knots[n], num_points)
        spline_x, spline_y = [], []

        for t in t_values:
            x, y = 0.0, 0.0
            for i in range(n):
                basis = self.basis_function(i, self.k, t, knots)
                x += basis * self._points[i]['x']
                y += basis * self._points[i]['y']
            spline_x.append(x)
            spline_y.append(y)

        return [{'x': spline_x[i], 'y': spline_y[i]} for i in range(len(spline_x))]

    def find_point(self, x, y):
        for point in self._points:
            if ((point['x'] - x) ** 2 + (point['y'] - y) ** 2) ** 0.5 < 10:
                return point
        return None

    def add_point(self, x, y):
        self._points.append({'x': x, 'y': y})
        self._points.sort(key=lambda p: p['x'])

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for point in self._points:
            pygame.draw.circle(screen, (0, 0, 255), (int(point['x']), int(point['y'])), 5)

        curve_points = self.compute_bspline()
        if curve_points:
            for i in range(len(curve_points) - 1):
                pygame.draw.line(screen, (255, 0, 0),
                                 (int(curve_points[i]['x']), int(curve_points[i]['y'])),
                                 (int(curve_points[i + 1]['x']), int(curve_points[i + 1]['y'])), 2)

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
                    if event.button == 1:
                        self.selected_point = self.find_point(*event.pos)
                    elif event.button == 3:  # Jobb klikk
                        self.add_point(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.selected_point = None
                elif event.type == pygame.MOUSEMOTION and self.selected_point:
                    self.selected_point['x'], self.selected_point['y'] = event.pos

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    interpolator = BSplineInterpolation()
    interpolator.run()