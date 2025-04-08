import numpy as np
from .matrix_utils import MatrixUtils
import pygame

class BSplineInterpolation:
    def __init__(self):
        self._points = [{'x': 100 + i * 100, 'y': 300 if i % 2 == 0 else 100} for i in range(8)]
        self.k = 4
        self.approximation_k = 3
        self.show_global_approx = False
        self.selected_point = None
        self.show_lower_order = False

        # Csúszka setup
        self.slider_k_rect = pygame.Rect(20, 540, 200, 10)
        self.slider_k_handle = pygame.Rect(20, 535, 10, 20)

        self.slider_approx_rect = pygame.Rect(20, 570, 200, 10)
        self.slider_approx_handle = pygame.Rect(20, 565, 10, 20)

        self.dragging_k = False
        self.dragging_approx = False

        # Handle pozíciók beállítása
        self.update_slider_positions()

    def update_slider_positions(self):
        ratio_k = (self.k - 1) / 9
        self.slider_k_handle.x = self.slider_k_rect.left + int(ratio_k * self.slider_k_rect.width)

        ratio_approx = (self.approximation_k - 1) / 9
        self.slider_approx_handle.x = self.slider_approx_rect.left + int(ratio_approx * self.slider_approx_rect.width)

    def basis_function(self, i, k, t, knots):
        if k == 1:
            return 1.0 if knots[i] <= t < knots[i + 1] else 0.0
        else:
            denom1 = knots[i + k - 1] - knots[i]
            term1 = 0.0 if denom1 == 0 else (t - knots[i]) / denom1 * self.basis_function(i, k - 1, t, knots)
            denom2 = knots[i + k] - knots[i + 1]
            term2 = 0.0 if denom2 == 0 else (knots[i + k] - t) / denom2 * self.basis_function(i + 1, k - 1, t, knots)
            return term1 + term2

    def compute_bspline(self, points, num_points=200):
        n = len(points)
        knots = np.linspace(0, 1, n + self.k)
        t_values = np.linspace(knots[self.k - 1], knots[n], num_points)
        spline_x, spline_y = [], []

        for t in t_values:
            x, y = 0.0, 0.0
            for i in range(n):
                basis = self.basis_function(i, self.k, t, knots)
                x += basis * points[i]['x']
                y += basis * points[i]['y']
            spline_x.append(x)
            spline_y.append(y)

        return [{'x': spline_x[i], 'y': spline_y[i]} for i in range(len(spline_x))]

    def compute_lower_order_approximation(self, num_points=200):
        original_curve = self.compute_bspline(self._points)
        x_orig = np.array([p['x'] for p in original_curve])
        y_orig = np.array([p['y'] for p in original_curve])

        n = len(self._points)
        knots = np.linspace(0, 1, n + self.approximation_k)
        t_values = np.linspace(knots[self.approximation_k - 1], knots[n], num_points)

        spline_x, spline_y = [], []

        for t in t_values:
            x, y = 0.0, 0.0
            for i in range(n):
                basis = self.basis_function(i, self.approximation_k, t, knots)
                x += basis * self._points[i]['x']
                y += basis * self._points[i]['y']
            spline_x.append(x)
            spline_y.append(y)

        errors = np.sqrt((x_orig - np.array(spline_x)) ** 2 + (y_orig - np.array(spline_y)) ** 2)
        max_error = np.max(errors)
        rms_error = np.sqrt(np.mean(errors ** 2))

        approx_points = [{'x': spline_x[i], 'y': spline_y[i]} for i in range(len(spline_x))]
        return approx_points, max_error, rms_error

    def least_squares_approximation(self):
        original_curve = self.compute_bspline(self._points)
        num_approx_points = len(self._points)
        knots = np.linspace(0, 1, num_approx_points + self.approximation_k)
        t_values = np.linspace(knots[self.approximation_k - 1], knots[num_approx_points], len(original_curve))

        B = np.array([
            [self.basis_function(col, self.approximation_k, t, knots) for col in range(num_approx_points)]
            for t in t_values
        ])

        x_target = np.array([p['x'] for p in original_curve])
        y_target = np.array([p['y'] for p in original_curve])

        pinv = MatrixUtils.pseudo_inverse(B.tolist())
        if pinv is None:
            return self._points, None, None

        pinv = np.array(pinv)
        ctrl_x = pinv @ x_target
        ctrl_y = pinv @ y_target

        new_ctrl_pts = [{'x': ctrl_x[i], 'y': ctrl_y[i]} for i in range(num_approx_points)]
        approx_curve = self.compute_bspline(new_ctrl_pts)

        x_approx = np.array([p['x'] for p in approx_curve])
        y_approx = np.array([p['y'] for p in approx_curve])

        errors = np.sqrt((x_target - x_approx) ** 2 + (y_target - y_approx) ** 2)
        max_error = np.max(errors)
        rms_error = np.sqrt(np.mean(errors ** 2))

        return new_ctrl_pts, max_error, rms_error

    def find_point(self, x, y):
        for point in self._points:
            if ((point['x'] - x) ** 2 + (point['y'] - y) ** 2) ** 0.5 < 10:
                return point
        return None

    def add_point(self, x, y):
        self._points.append({'x': x, 'y': y})
        self._points.sort(key=lambda p: p['x'])

    def handle_sliders(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_k_handle.collidepoint(event.pos):
                self.dragging_k = True
            elif self.slider_approx_handle.collidepoint(event.pos):
                self.dragging_approx = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_k = False
            self.dragging_approx = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_k:
                x = max(self.slider_k_rect.left, min(event.pos[0], self.slider_k_rect.right))
                self.slider_k_handle.x = x
                ratio = (x - self.slider_k_rect.left) / self.slider_k_rect.width
                self.k = max(2, min(10, int(ratio * 9 + 1)))

            if self.dragging_approx:
                x = max(self.slider_approx_rect.left, min(event.pos[0], self.slider_approx_rect.right))
                self.slider_approx_handle.x = x
                ratio = (x - self.slider_approx_rect.left) / self.slider_approx_rect.width
                self.approximation_k = max(2, min(10, int(ratio * 9 + 1)))

    def draw(self, screen, font):
        screen.fill((255, 255, 255))

        for point in self._points:
            pygame.draw.circle(screen, (0, 0, 255), (int(point['x']), int(point['y'])), 5)

        curve_points = self.compute_bspline(self._points)
        for i in range(len(curve_points) - 1):
            pygame.draw.line(screen, (255, 0, 0),
                             (int(curve_points[i]['x']), int(curve_points[i]['y'])),
                             (int(curve_points[i + 1]['x']), int(curve_points[i + 1]['y'])), 2)

        if self.show_global_approx:
            new_ctrl, max_error, rms_error = self.least_squares_approximation()
            approx_curve = self.compute_bspline(new_ctrl)
            for i in range(len(approx_curve) - 1):
                pygame.draw.line(screen, (0, 200, 0),
                                 (int(approx_curve[i]['x']), int(approx_curve[i]['y'])),
                                 (int(approx_curve[i + 1]['x']), int(approx_curve[i + 1]['y'])), 2)
            for point in new_ctrl:
                pygame.draw.circle(screen, (0, 100, 0), (int(point['x']), int(point['y'])), 5)
            error_text = f"[LSQ] Max error: {max_error:.2f}, RMS error: {rms_error:.2f}"
            screen.blit(font.render(error_text, True, (0, 0, 0)), (10, 30))

        # Slider rajzok
        pygame.draw.rect(screen, (180, 180, 180), self.slider_k_rect)
        pygame.draw.rect(screen, (50, 50, 200), self.slider_k_handle)
        screen.blit(font.render(f"k = {self.k}", True, (0, 0, 0)), (self.slider_k_rect.left, self.slider_k_rect.top - 20))

        pygame.draw.rect(screen, (180, 180, 180), self.slider_approx_rect)
        pygame.draw.rect(screen, (200, 100, 50), self.slider_approx_handle)
        screen.blit(font.render(f"approx_k = {self.approximation_k}", True, (0, 0, 0)),
                    (self.slider_approx_rect.left, self.slider_approx_rect.top - 20))

        if self.show_lower_order:
            approx_points, max_error, rms_error = self.compute_lower_order_approximation()
            if approx_points:
                original_curve = self.compute_bspline(self._points)

                errors = [((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5
                          for p1, p2 in zip(original_curve, approx_points)]

                max_e = max(errors) if max(errors) != 0 else 1
                norm_errors = [e / max_e for e in errors]

                def get_color(value):
                    r = int(255 * value)
                    g = 0
                    b = int(255 * (1 - value))
                    return (r, g, b)

                for i in range(len(approx_points) - 1):
                    color = get_color(norm_errors[i])
                    pygame.draw.line(screen, color,
                                     (int(approx_points[i]['x']), int(approx_points[i]['y'])),
                                     (int(approx_points[i + 1]['x']), int(approx_points[i + 1]['y'])), 4)

                error_text = f"Max error: {max_error:.2f}, RMS error: {rms_error:.2f}"
                text_surface = font.render(error_text, True, (0, 0, 0))
                screen.blit(text_surface, (10, 10))