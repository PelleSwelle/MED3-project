import random
#https://lvngd.com/blog/convex-hull-graham-scan-algorithm-python/

"""
Computes the Convex Hull with the Graham Scan algorithm
Use:
	h = ConvexHull()
	print(h.hull)
"""


class ConvexHull:
    def __init__(self, points):
        if not points:
            self.points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(50)]
        else:
            self.points = points
        self.hull = self.compute_convex_hull()

    def get_cross_product(self, p1, p2, p3):
        return ((p2[0] - p1[0]) * (p3[1] - p1[1])) - ((p2[1] - p1[1]) * (p3[0] - p1[0]))

    def get_slope(self, p1, p2):
        if p1[0] == p2[0]:
            return float('inf')
        else:
            return 1.0 * (p1[1] - p2[1]) / (p1[0] - p2[0])

    def compute_convex_hull(self):
        hull = []
        self.points.sort(key=lambda x: [x[0], x[1]]) #If more than one point has the smallest x value, take the one with the smallest y value.
        start = self.points.pop(0)

        hull.append(start)
        self.points.sort(key=lambda p: (self.get_slope(p, start), -p[1], p[0]))
        for pt in self.points:
            hull.append(pt)
            while len(hull) > 2 and self.get_cross_product(hull[-3], hull[-2], hull[-1]) < 0:
                hull.pop(-2)
        return hull