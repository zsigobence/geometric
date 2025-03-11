from math import comb


import pygame
import sys



def bernstein(n, k, x):
    return comb(n, k) * (x ** k) * ((1 - x) ** (n - k))

class BezierCurve:
    def __init__(self):
        self._points = [
            {'x': 100, 'y': 300},
            {'x': 300, 'y': 100},
            {'x': 500, 'y': 300},
            {'x': 700, 'y': 100},
        ]
        self.weights = [1, 2, 2, 1]
        self.selected_point = None

    def denominator(self,t):
        n = len(self._points)
        sum = 0
        for j in range(n):
            sum +=  self.weights[j] * bernstein(n, j, t)

        return sum

    def bezier(self,t):
        n = len(self._points)
        x = 0
        y = 0

        for i in range(n):
            x += ((self.weights[i] * bernstein(n, i, t)) / ( self.denominator(t) )) * self._points[i]["x"]
            y += ((self.weights[i] * bernstein(n, i, t))  / ( self.denominator(t) ) )* self._points[i]["y"]


        return {'x': x, 'y': y}

    def find_point(self, x, y):
        for point in self._points:
            if ((point['x'] - x) ** 2 + (point['y'] - y) ** 2) ** 0.5 < 10:
                return point
        return None

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for point in self._points:
            pygame.draw.circle(screen, (0, 0, 255), (int(point['x']), int(point['y'])), 5)

        curve_points = [self.bezier(t / 100) for t in range(0,101) if t != 100]
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
                    self.selected_point = self.find_point(*event.pos)
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
    interpolator = BezierCurve()
    interpolator.run()
