import math

class Vector2(object): # vector class
    def _init_(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh =0.000001

    def _add_(self, other): # arithmetic methods 
        return Vector2(self.x + other.x, self.y + other.y)
    
    def _sub_(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def _neg_(self):
        return Vector2(-self.x, -self.y)

    def _mul_(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def _div_(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None
    
    def _truediv_(self, scalar):
        return self._div_(scalar)

    def _eq_(self, other): # equality check between 2 vectors, using threshold value
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
            return False

    def magnitudSquared(self): # more optmizied for comparision of length between 2 vectors
        return self.x**2 + self.y**2

    def magnitude(self): # returns actual length of vector
        return math.sqrt(self.magnitudSquared())

    def copy(self): # copy method to create new instance of a vector
        return Vector2(self.x, self.y)

    def asTuple(self): # converts vector to tuple
        return self.x, self.y

    def asInt(self): # converts vetor to int tuple
        return int(self.x), int(self.y)

    def _str_(self): # print out vector 
        return "<"+str(self.x)+", "+str(self.y)+">"