import numpy as np

class BSplineCalculator:
    @staticmethod
    def basis_function(i, k, t, knots):
        if k == 1:
            return 1.0 if (knots[i] <= t < knots[i + 1]) else 0.0
        else:
            denom1 = knots[i + k - 1] - knots[i]
            term1 = 0.0 if denom1 == 0 else (t - knots[i]) / denom1 * BSplineCalculator.basis_function(i, k - 1, t, knots)

            denom2 = knots[i + k] - knots[i + 1]
            term2 = 0.0 if denom2 == 0 else (knots[i + k] - t) / denom2 * BSplineCalculator.basis_function(i + 1, k - 1, t, knots)

            return term1 + term2

    @staticmethod
    def compute_bspline(points, k, num_points=200):
        n = len(points)
        if n < k:
            return []

        knots = np.linspace(0, 1, n + k)

        start_t = knots[k - 1]
        end_t = knots[n]
        if start_t >= end_t:
            return []

        t_values = np.linspace(start_t, end_t, num_points)

        spline_points = []
        for t in t_values:
            x, y = 0.0, 0.0
            for i in range(n):
                basis = BSplineCalculator.basis_function(i, k, t, knots)
                x += basis * points[i]['x']
                y += basis * points[i]['y']
            spline_points.append({'x': x, 'y': y})

        return spline_points
