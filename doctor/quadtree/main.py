class Quadtree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
    
    def insert(self, x, y, id=None):
        if self.boundary.contains(x, y):
            if len(self.points) < self.capacity:
                p = Point(x, y, id)
                self.points.append(p)
            else:
                if not self.divided:
                    self.subdivide()
                self.northEast.insert(x, y, id)
                self.northWest.insert(x, y, id)
                self.southEast.insert(x, y, id)
                self.southWest.insert(x, y, id)


    def subdivide(self):
        x, y, w, h = self.boundary.point.x, self.boundary.point.y, self.boundary.w, self.boundary.h
        ne = Rectangle(x+w/2, y+h/2, w-w/2, h-h/2)
        nw = Rectangle(x, y+h/2, w/2, h-h/2)
        sw = Rectangle(x, y, w/2, h/2)
        se = Rectangle(x+w/2, y, (w-w/2), h/2)
        
        self.northEast = Quadtree(ne)
        self.northWest = Quadtree(nw)
        self.southEast = Quadtree(se)
        self.southWest = Quadtree(sw)
        self.divided = True
    
    def nearby(self, range, points):
        if self.boundary.isIntersect(range):
            for pts in self.points:
                if range.contains(pts.x, pts.y):
                    points.append(pts)
            
            if self.divided:
                self.northEast.nearby(range, points)
                self.northWest.nearby(range, points)
                self.southEast.nearby(range, points)
                self.southWest.nearby(range, points)


class Point:
    def __init__(self, x, y, id=None):
        self.id = id
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.point = Point(x, y)
        self.w = w
        self.h = h
    
    def contains(self, x, y):
        f = ( x>=(self.point.x) \
             and x<=(self.point.x + self.w) and \
                  y>=(self.point.y) and \
                       y<=(self.point.y + self.h) )
        return f
    
    def isIntersect(self, rect):
        f = ((self.point.x + self.w) <= rect.point.x ) or ((rect.point.x + rect.w) <= self.point.x ) or ((self.point.y + self.h) <= rect.point.y ) or ((rect.point.y + rect.h) <= self.point.y )
        return not f