import numpy as np
from .bspline_calculator import BSplineCalculator

class BSplineApproximator:
    def __init__(self, calculator: BSplineCalculator):
        self.calculator = calculator

    def compute_approximation_by_order(self, original_points, original_k, approx_k, num_eval_points=200):
        n = len(original_points)
        if n < original_k or n < approx_k or original_k < 2 or approx_k < 2:
            return [], 0.0, 0.0, []

        knots_orig = np.linspace(0, 1, n + original_k)
        start_t_orig = knots_orig[original_k - 1]
        end_t_orig = knots_orig[n]
        if start_t_orig >= end_t_orig:
            return [], 0.0, 0.0, []

        t_values = np.linspace(start_t_orig, end_t_orig, num_eval_points)

        original_curve_points = []
        knots_orig_eval = np.linspace(0, 1, n + original_k)
        for t in t_values:
            x, y = 0.0, 0.0
            for i in range(n):
                basis = self.calculator.basis_function(i, original_k, t, knots_orig_eval)
                x += basis * original_points[i]['x']
                y += basis * original_points[i]['y']
            original_curve_points.append({'x': x, 'y': y})

        approx_curve_points = []
        knots_approx_eval = np.linspace(0, 1, n + approx_k)
        for t in t_values:
            x, y = 0.0, 0.0
            for i in range(n):
                basis = self.calculator.basis_function(i, approx_k, t, knots_approx_eval)
                x += basis * original_points[i]['x']
                y += basis * original_points[i]['y']
            approx_curve_points.append({'x': x, 'y': y})

        if not original_curve_points or not approx_curve_points or len(original_curve_points) != len(approx_curve_points):
            return [], 0.0, 0.0, []

        errors = []
        for p1, p2 in zip(original_curve_points, approx_curve_points):
            error = ((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5
            errors.append(error)

        errors_np = np.array(errors)
        max_error = np.max(errors_np) if errors_np.size > 0 else 0.0
        rms_error = np.sqrt(np.mean(errors_np ** 2)) if errors_np.size > 0 else 0.0

        return approx_curve_points, max_error, rms_error, errors

    def least_squares_approximation(self, original_points, original_k, target_k, num_target_ctrl_points=None, num_sample_points=400):
        n_orig = len(original_points)
        if num_target_ctrl_points is None:
            num_target_ctrl_points = n_orig

        if n_orig < original_k or num_target_ctrl_points < target_k or original_k < 2 or target_k < 2:
            return [], 0.0, 0.0

        knots_orig = np.linspace(0, 1, n_orig + original_k)
        start_t_orig = knots_orig[original_k - 1]
        end_t_orig = knots_orig[n_orig]
        if start_t_orig >= end_t_orig:
            return [], 0.0, 0.0

        t_values_sample = np.linspace(start_t_orig, end_t_orig, num_sample_points)

        original_curve_samples = []
        knots_orig_eval = np.linspace(0, 1, n_orig + original_k)
        for t in t_values_sample:
            x, y = 0.0, 0.0
            for i in range(n_orig):
                basis = self.calculator.basis_function(i, original_k, t, knots_orig_eval)
                x += basis * original_points[i]['x']
                y += basis * original_points[i]['y']
            original_curve_samples.append({'x': x, 'y': y})

        if not original_curve_samples:
            return [], 0.0, 0.0

        x_target = np.array([p['x'] for p in original_curve_samples])
        y_target = np.array([p['y'] for p in original_curve_samples])

        n_approx_ctrl = num_target_ctrl_points
        k_approx = target_k
        knots_approx_basis = np.linspace(0, 1, n_approx_ctrl + k_approx)

        B = np.zeros((len(t_values_sample), n_approx_ctrl))
        for i, t in enumerate(t_values_sample):
            for j in range(n_approx_ctrl):
                B[i, j] = self.calculator.basis_function(j, k_approx, t, knots_approx_basis)

        pinv_B = np.linalg.pinv(B)
        ctrl_x = pinv_B @ x_target
        ctrl_y = pinv_B @ y_target
        new_ctrl_pts = [{'x': ctrl_x[i], 'y': ctrl_y[i]} for i in range(n_approx_ctrl)]

        approx_curve_evaluated = []
        knots_approx_eval = np.linspace(0, 1, n_approx_ctrl + k_approx)
        for t in t_values_sample:
            x, y = 0.0, 0.0
            for i in range(n_approx_ctrl):
                basis = self.calculator.basis_function(i, k_approx, t, knots_approx_eval)
                x += basis * new_ctrl_pts[i]['x']
                y += basis * new_ctrl_pts[i]['y']
            approx_curve_evaluated.append({'x': x, 'y': y})

        if not approx_curve_evaluated or len(approx_curve_evaluated) != len(original_curve_samples):
            return new_ctrl_pts, 0.0, 0.0

        errors = []
        for p_orig, p_approx in zip(original_curve_samples, approx_curve_evaluated):
            error = ((p_orig['x'] - p_approx['x']) ** 2 + (p_orig['y'] - p_approx['y']) ** 2) ** 0.5
            errors.append(error)

        errors_np = np.array(errors)
        max_error = np.max(errors_np) if errors_np.size > 0 else 0.0
        rms_error = np.sqrt(np.mean(errors_np ** 2)) if errors_np.size > 0 else 0.0

        return new_ctrl_pts, max_error, rms_error
