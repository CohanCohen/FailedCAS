import math
import random

class poly:
    def __init__(self, coeffs):
        self.coeffs = coeffs[:]
        self.deg = len(coeffs) - 1
    
    def __call__(self, x):
        s = 0
        for i in range(self.deg + 1):
            s += self.coeffs[i] * x ** i
        
        return s
    
    def __str__(self):
        string = []
        for i in range(self.deg + 1):
            if i < self.deg:
                if i > 1:
                    if self.coeffs[i] == 0:
                        continue;
                    elif self.coeffs[i] == 1 or self.coeffs[i] == -1:
                        string += ["%s%s^%d"%("+" if self.coeffs[i] == 1 else "-", "x", i)]
                    else:
                        string += ["%s%s%s^%d"%("+" if math.copysign(1, self.coeffs[i])==1 else "" , str(self.coeffs[i]), "x", i)]
                elif i == 1:
                    if self.coeffs[i] == 0:
                        continue;
                    elif self.coeffs[i] in [1, -1]:
                        string += ["%s%s"%("+" if math.copysign(1, self.coeffs[i])==1 else "-" , "x")]
                    else:
                        string += ["%s%s%s"%("+" if math.copysign(1, self.coeffs[i])==1 else "" ,str(self.coeffs[i]), "x")]
                elif i == 0:
                    if self.coeffs[i] == 0:
                        continue;
                    string += ["%s%s"%("+" if math.copysign(1, self.coeffs[i])==1 else "" , str(self.coeffs[i]))]
            
            else:
                if i > 1:
                    if self.coeffs[i] == 0:
                        continue;
                    elif self.coeffs[i] in [1, -1]:
                        string += ["%s%s^%d"%("+" if math.copysign(1, self.coeffs[i])==1 else "-" , "x", i)]
                    else:
                        string += ["%s%s%s^%d"%("+" if math.copysign(1, self.coeffs[i])==1 else "", str(self.coeffs[i]), "x", i)]
                elif i == 1:
                    if self.coeffs[i] == 0:
                        continue;
                    elif self.coeffs[i] in [1, -1]:
                        string += ["%s%s"%("+" if math.copysign(1, self.coeffs[i])==1 else "-" , "x")]
                    else:
                        string += ["%s%s%s"%("+" if math.copysign(1, self.coeffs[i])==1 else "" ,str(self.coeffs[i]), "x")]
                elif i == 0:
                    if self.coeffs[i] == 0:
                        continue;
                    string += ["%s"%(str(self.coeffs[i]))]

        string.reverse()
        return "".join(string)
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            x = self.coeffs[:]
            x[0] += other
            return poly(x[:])
        
        elif isinstance(other, poly):
            large_poly = self if self.deg >= other.deg else other
            small_poly = self if self.deg < other.deg else other
            
            res_arr = small_poly.coeffs[:] + [0 for i in range(large_poly.deg - small_poly.deg)]
            for i in range(len(large_poly.coeffs)):
                res_arr[i] += large_poly.coeffs[i]
            
            return poly(res_arr[:])
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            x = [other * i for i in self.coeffs[:]]
            return poly(x)
        
        elif isinstance(other, poly):
            arr = [0 for i in range(self.deg + other.deg + 1)]
            for i in range(len(self.coeffs)):
                for j in range(len(other.coeffs)):
                    arr[i + j] += self.coeffs[i] * other.coeffs[j]
            
            return poly(arr[:])
    
    def __neg__(self):
        return -1 * self
    
    def __sub__(self, other):
        return self + (-other)
    
    def __pow__(self, other):
        if isinstance(other, int):
            p = poly([1])
            for i in range(other):
                p *= self
            return p
    def __eq__(self, other):
        return self.coeffs[:] == other.coeffs[:]
    
    def diff(self):
        new_arr = []
        for i in range(1, self.deg + 1):
            new_arr.append(self.coeffs[i] * i)
        
        return poly(new_arr)
    
    __rmul__ = __mul__
    __radd__ = __add__
    @staticmethod
    def rand(deg, coeff_range = [0, 10]):
        coeffs = [random.randint(coeff_range[0], coeff_range[1]) for i in range(deg + 1)]
        return poly(coeffs)

class RationalExpr:
    def __init__(self, elems):
        self.elems = elems
    
    def __call__(self, x):
        return self.elems[0](x) / self.elems[1](x)
    def __str__(self):
        str1 = str(self.elems[0])
        str2 = str(self.elems[1])
        string = str1 + "\n" + "".join(["-" for i in range(max(len(str1), len(str2)))]) + "\n" + str2
        return string
    def __add__(self, other):
        if isinstance(other, RationalExpr):
            return RationalExpr([self.elems[0] * other.elems[1] + self.elems[1] * other.elems[0], self.elems[1] * other.elems[1]])
        
        elif isinstance(other, poly):
            return RationalExpr([self.elems[0] + self.elems[1] * other, self.elems[1]])
        
        elif isinstance(other, (int, float)):
            return RationalExpr([self.elems[0] + self.elems[1] * other, self.elems[1]])
    
    def __neg__(self):
        return RationalExpr([-self.elems[0], self.elems[1]])
    
    def __sub__(self, other):
        return self + (-other)
    
    def __mul__(self, other):
        if isinstance(other, RationalExpr):
            return RationalExpr([self.elems[0] * other.elems[0], self.elems[1] * other.elems[1]])
        
        elif isinstance(other, poly):
            return RationalExpr([self.elems[0] * other, self.elems[1]])
        
        elif isinstance(other, (int, float)):
            return RationalExpr([self.elems[0] * other, self.elems[1]])
    
    def __truediv__(self, other):
        if isinstance(other, RationalExpr):
            return RationalExpr([self.elems[0] * other.elems[1], self.elems[1] * other.elems[0]])
        
        elif isinstance(other, poly):
            return RationalExpr([self.elems[0] , self.elems[1] * other])
        
        elif isinstance(other, (int, float)):
            return RationalExpr([self.elems[0], self.elems[1] * other])
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            pass
    
    __radd__ = __add__
    __rmul__ = __mul__
    
    def diff(self):
        return RationalExpr([self.elems[0].diff() * self.elems[1] - self.elems[1].diff() * self.elems[0], self.elems[1] ** 2])
    
    @staticmethod
    def rand(deg, coeff_range = [0, 10]):
        return RationalExpr([poly.rand(deg, coeff_range=coeff_range), poly.rand(deg, coeff_range=coeff_range)])

class Root:
    def __init__(self, p, n):
        self.poly = p
        self.root = n
    
    def __call__(self, x):
        return (self.poly(x)) ** self.root
    
    def __str__(self):
        poly_str = str(self.poly)
        string = "   " + "".join(["_" for i in range(len(poly_str))]) + "\n"+" %d/\n"%self.root
        string += "\\/%s"%poly_str
        return string

    def __add__(self, other):
        pass
