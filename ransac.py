import math
import random
import numpy as np

class LinearFit:
    min_count = 2

    def __init__(self, points):
        self.points = points.copy()

        # linear model:
        #
        #    x = self.p[0] * y + self.p[1]
        #
        y = [p[0] for p in points]
        x = [p[1] for p in points]
        self.p, self.residuals, _, _, _ = np.polyfit(y, x, 1, full=True)

    def fit_err(self, point):
        # The distance from a point (x0, y0) to a line: ax + by + c = 0 is:
        #
        #        | a*x0 + b*y0 + c |
        #    d = -------------------
        #         sqrt(a^2 + b^2)
        #
        err = abs(point[1] - self.p[0] * point[0] - self.p[1])
        err = err / math.sqrt(1 + self.p[0]**2)
        return err

    def err(self):
        return self.residuals[0]

def choose_random(points, n, weights):
    chosen = set()
    points = points[:]
    weights = weights[:]

    while len(chosen) < n:
        point = random.choices(points, weights=weights)[0]
        chosen.add(point)

        i = points.index(point)
        del points[i]
        del weights[i]

    return chosen

def ransac(points, weights, model_class, max_iters, max_fit_err, fit_ratio):
    best_model = None

    min_count = model_class.min_count
    fit_count = len(points) * fit_ratio

    for _ in range(max_iters):
        inliers = choose_random(points, min_count, weights)
        model = model_class(inliers)

        for point in points:
            if point in model.points:
                continue
            if  model.fit_err(point) < max_fit_err:
                inliers.add(point)

        if len(inliers) >= fit_count:
            if best_model is not None and best_model.points == inliers:
                continue

            model = model_class(inliers)
            if best_model is None or best_model.err() > model.err():
                best_model = model

    if best_model is None:
        return None

    best_points = best_model.points.copy()
    for point in points:
        if point in best_model.points:
            continue
        if best_model.fit_err(point) < max_fit_err:
            best_points.add(point)

    if best_model.points != best_points:
        best_model = model_class(best_points)

    return best_model

def test_linear_fit():
    points = [(0,1), (1,0)]
    line = LinearFit(points)
    err = line.fit_err((0,0))
    assert abs(err - 1/math.sqrt(2)) < 0.001

def test_ransac():
    points = [
        (128, 93), (221, 33), (254, 33), (287, 34), (321, 34), (389, 35),
        (424, 35), (459, 35), (494, 36), (530, 36), (602, 37), (639, 93),
    ]
    weights = [1] * len(points)

    model = ransac(points, weights, LinearFit, 10, 3, 0.6)
    assert model is not None
    assert (128, 93) not in model.points
    assert (639, 93) not in model.points
    assert len(model.points) == 10
    print(model.p)

def test():
    test_linear_fit()
    test_ransac()

if __name__ == "__main__":
    test()
