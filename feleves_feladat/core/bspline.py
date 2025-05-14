import pygame
import numpy as np
from .bspline_calculator import BSplineCalculator
from .bspline_approximator import BSplineApproximator

class BSplineInterpolation:
    def __init__(self):
        self._points = [{'x': 100 + i * 100, 'y': 300 if i % 2 == 0 else 100} for i in range(8)]
        self.k = 4
        self.approximation_k = 3
        self.min_k = 2
        self.max_k = 10
        self.k = max(self.min_k, min(self.max_k, self.k, len(self._points)))
        self.approximation_k = max(self.min_k, min(self.max_k, self.approximation_k, len(self._points), self.k))
        self.show_global_approx = False
        self.show_lower_order = False
        self.selected_point = None
        self.calculator = BSplineCalculator()
        self.approximator = BSplineApproximator(self.calculator)
        self.slider_k_rect = pygame.Rect(20, 540, 200, 10)
        self.slider_k_handle = pygame.Rect(0, 0, 10, 20)
        self.slider_approx_rect = pygame.Rect(20, 570, 200, 10)
        self.slider_approx_handle = pygame.Rect(0, 0, 10, 20)
        self.dragging_k = False
        self.dragging_approx = False
        self.update_slider_positions()

    def update_slider_positions(self):
        slider_width = self.slider_k_rect.width
        handle_width = self.slider_k_handle.width
        usable_width = slider_width - handle_width
        k_range = self.max_k - self.min_k
        clamped_k = max(self.min_k, min(self.max_k, self.k))
        ratio_k = (clamped_k - self.min_k) / k_range if k_range > 0 else 0
        self.slider_k_handle.left = self.slider_k_rect.left + int(ratio_k * usable_width)
        self.slider_k_handle.centery = self.slider_k_rect.centery
        clamped_approx_k = max(self.min_k, min(self.max_k, self.approximation_k))
        ratio_approx = (clamped_approx_k - self.min_k) / k_range if k_range > 0 else 0
        self.slider_approx_handle.left = self.slider_approx_rect.left + int(ratio_approx * usable_width)
        self.slider_approx_handle.centery = self.slider_approx_rect.centery

    def find_point(self, x, y):
        for point in self._points:
            if ((point['x'] - x) ** 2 + (point['y'] - y) ** 2) ** 0.5 < 10:
                return point
        return None

    def add_point(self, x, y):
        self._points.append({'x': x, 'y': y})
        self._points.sort(key=lambda p: p['x'])
        self.k = max(self.min_k, min(self.k, len(self._points)))
        self.approximation_k = max(self.min_k, min(self.approximation_k, len(self._points), self.k))
        self.update_slider_positions()

    def remove_point(self, point):
        if point in self._points:
            self._points.remove(point)
            self.selected_point = None
            self.k = max(self.min_k, min(self.k, len(self._points)))
            self.approximation_k = max(self.min_k, min(self.approximation_k, len(self._points), self.k))
            self.update_slider_positions()

    def handle_sliders(self, event):
        slider_width = self.slider_k_rect.width
        handle_width = self.slider_k_handle.width
        usable_width = slider_width - handle_width
        slider_value_range = self.max_k - self.min_k
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_k_handle.collidepoint(event.pos):
                self.dragging_k = True
            elif self.slider_approx_handle.collidepoint(event.pos):
                self.dragging_approx = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_k = False
            self.dragging_approx = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_k and slider_value_range > 0 and usable_width > 0:
                mouse_x_in_track = max(0, min(event.pos[0] - self.slider_k_rect.left, usable_width))
                ratio = mouse_x_in_track / usable_width
                raw_k = int(round(ratio * slider_value_range + self.min_k))
                self.k = max(self.min_k, min(self.max_k, raw_k, len(self._points)))
                self.approximation_k = min(self.approximation_k, self.k)
                self.update_slider_positions()
            if self.dragging_approx and slider_value_range > 0 and usable_width > 0:
                mouse_x_in_track = max(0, min(event.pos[0] - self.slider_approx_rect.left, usable_width))
                ratio = mouse_x_in_track / usable_width
                raw_approx_k = int(round(ratio * slider_value_range + self.min_k))
                self.approximation_k = max(self.min_k, min(self.max_k, raw_approx_k, len(self._points), self.k))
                self.update_slider_positions()

    def draw(self, screen, font):
        screen.fill((255, 255, 255))
        text_y = 10
        line_height = font.get_linesize() + 5
        for point in self._points:
            color = (0, 0, 255)
            if self.selected_point is point:
                color = (255, 165, 0)
            pygame.draw.circle(screen, color, (int(point['x']), int(point['y'])), 5)
        if len(self._points) >= self.k and self.k >= self.min_k:
            curve_points = self.calculator.compute_bspline(self._points, self.k)
            if curve_points and len(curve_points) > 1:
                for i in range(len(curve_points) - 1):
                    pygame.draw.line(screen, (255, 0, 0),
                                     (int(curve_points[i]['x']), int(curve_points[i]['y'])),
                                     (int(curve_points[i + 1]['x']), int(curve_points[i + 1]['y'])), 2)
            elif not curve_points and len(self._points) >= self.min_k:
                warning_text = f"Original spline computation failed (k={self.k}, points={len(self._points)})."
                screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
                text_y += line_height
        elif len(self._points) < self.k and len(self._points) >= self.min_k:
            warning_text = f"Need at least {self.k} points for original spline (current: {len(self._points)})."
            screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
            text_y += line_height
        elif len(self._points) < self.min_k:
            warning_text = f"Need at least {self.min_k} points for any spline (current: {len(self._points)})."
            screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
            text_y += line_height
        if self.show_global_approx:
            if len(self._points) >= self.approximation_k and self.approximation_k >= self.min_k:
                new_ctrl, max_error_lsq, rms_error_lsq = self.approximator.least_squares_approximation(
                    self._points, self.k, self.approximation_k, num_target_ctrl_points=len(self._points))
                if new_ctrl:
                    approx_curve_lsq = self.calculator.compute_bspline(new_ctrl, self.approximation_k)
                    if approx_curve_lsq and len(approx_curve_lsq) > 1:
                        for i in range(len(approx_curve_lsq) - 1):
                            pygame.draw.line(screen, (0, 200, 0),
                                             (int(approx_curve_lsq[i]['x']), int(approx_curve_lsq[i]['y'])),
                                             (int(approx_curve_lsq[i + 1]['x']), int(approx_curve_lsq[i + 1]['y'])), 2)
                        for point in new_ctrl:
                            pygame.draw.circle(screen, (0, 100, 0), (int(point['x']), int(point['y'])), 5)
                        error_text_lsq = f"[LSQ] Approx k={self.approximation_k}, Max error: {max_error_lsq:.2f}, RMS error: {rms_error_lsq:.2f}"
                        screen.blit(font.render(error_text_lsq, True, (0, 0, 0)), (10, text_y))
                        text_y += line_height
                    elif not approx_curve_lsq:
                        warning_text = f"[LSQ] Cannot compute approx curve for drawing (k={self.approximation_k}, ctrl pts={len(new_ctrl)})."
                        screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
                        text_y += line_height
                else:
                    warning_text = "[LSQ] Approximation failed (check console for errors)."
                    screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
                    text_y += line_height
            elif len(self._points) < self.approximation_k and len(self._points) >= self.min_k:
                warning_text = f"[LSQ] Need at least {self.approximation_k} points for approx order {self.approximation_k} (current: {len(self._points)})."
                screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
                text_y += line_height
        if self.show_lower_order:
            if len(self._points) >= self.approximation_k and self.approximation_k >= self.min_k:
                approx_points_lo, max_error_lo, rms_error_lo, errors_list_lo = self.approximator.compute_approximation_by_order(
                    self._points, self.k, self.approximation_k)
                if approx_points_lo and len(approx_points_lo) > 1:
                    max_e = max(errors_list_lo) if errors_list_lo else 1.0
                    if max_e == 0: max_e = 1.0
                    norm_errors = [e / max_e for e in errors_list_lo]
                    def get_color(value):
                        clamped_value = max(0.0, min(1.0, value))
                        r = int(255 * clamped_value)
                        g = int(255 * (1 - clamped_value))
                        b = 0
                        return (r, g, b)
                    for i in range(len(approx_points_lo) - 1):
                        color = get_color(norm_errors[i])
                        pygame.draw.line(screen, color,
                                         (int(approx_points_lo[i]['x']), int(approx_points_lo[i]['y'])),
                                         (int(approx_points_lo[i + 1]['x']), int(approx_points_lo[i + 1]['y'])), 4)
                    error_text_lo = f"[Orig Pts] Approx k={self.approximation_k}, Max error: {max_error_lo:.2f}, RMS error: {rms_error_lo:.2f}"
                    screen.blit(font.render(error_text_lo, True, (0, 0, 0)), (10, text_y))
                    text_y += line_height
                elif not approx_points_lo:
                    warning_text = f"[Orig Pts] Cannot compute approx curve (k={self.approximation_k}, points={len(self._points)})."
                    screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
                    text_y += line_height
            elif len(self._points) < self.approximation_k and len(self._points) >= self.min_k:
                warning_text = f"[Orig Pts] Need at least {self.approximation_k} points for approx order {self.approximation_k} (current: {len(self._points)})."
                screen.blit(font.render(warning_text, True, (255, 0, 0)), (10, text_y))
                text_y += line_height
        pygame.draw.rect(screen, (180, 180, 180), self.slider_k_rect)
        pygame.draw.rect(screen, (50, 50, 200), self.slider_k_handle)
        k_label = f"Original k = {self.k}"
        screen.blit(font.render(k_label, True, (0, 0, 0)), (self.slider_k_rect.left, self.slider_k_rect.top - 20))
        pygame.draw.rect(screen, (180, 180, 180), self.slider_approx_rect)
        pygame.draw.rect(screen, (200, 100, 50), self.slider_approx_handle)
        approx_k_label = f"Approx k = {self.approximation_k}"
        screen.blit(font.render(approx_k_label, True, (0, 0, 0)),
                     (self.slider_approx_rect.left, self.slider_approx_rect.top - 20))
        instructions = "Left Click: Select/Drag Pt | Right Click: Add Pt | Del/Backspace: Remove Selected Pt | G: Toggle LSQ Approx | A: Toggle Orig Pts Approx"
        screen.blit(font.render(instructions, True, (0, 0, 0)), (10, text_y))
        pygame.display.flip()
