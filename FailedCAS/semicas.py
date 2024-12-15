import math
from typing import Any
import random
import utils

def group(array):
    resarr = []
    for i in array:
        state = True
        for j, k in resarr:
            state = state and j != i
        
        if state:
            resarr.append([i, array.count(i)])
    
    return resarr

def singular(array):
    state = True
    for i, j in array:
        state = state and j == 1
    return state

class const:
    def __init__(self, val):
        self.val = val
    
    def __call__(self, x):
        return self.val
    
    def __str__(self):
        return str(self.val)
    
    def diff(self):
        return 0
    
class multiset:
    def __init__(self, array):
        self.array = array[:]
    
    def __eq__(self, other):
        if isinstance(other, multiset):
            statement = True
            for i in self.array:
                statement = statement and other.array.count(i) == self.array.count(i)
            for i in other.array:
                statement = statement and other.array.count(i) == self.array.count(i)
            
            return statement
        else:
            if isinstance(other, list):
                return self == multiset(other)
            else:
                return False

                  

class identity:
    def __init__(self, string):
        self.str = string
    
    def __call__(self, x):
        return x
    def __str__(self) -> str:
        return str(self.str)
    
    def __eq__(self, other):
        if isinstance(other, identity):
            return self.str == other.str
        
        return False
    
    def diff(self):
        return 1
        

class add(object):
    '''
    def __init__(self, elems):
        self.elems = list(filter(lambda a : a != 0, elems))
        s = 0
        for i in self.elems:
            if isinstance(i, (int, float)):
                s += i
        q = list(filter(lambda a : not isinstance(a, (int, float)), self.elems[:]))
        self.elems = q + [s] if (s != 0 or len(q) == 0) else q
    '''
    def __new__(cls, elems):
        if len(elems) == 1:
            return elems[0]
        if len(elems) == 0:
            return 0
        arr = []
        for i in elems:
            if isinstance(i, add):
                arr += i.elems
        new_elems = list(filter(lambda x : not isinstance(x, add), elems)) + arr
        allbasic = True
        for i in new_elems:
            allbasic = allbasic and isinstance(i, (int, float))
        
        if allbasic:
            return sum(new_elems)
        
        else:
            '''
            h = list(filter(lambda a : a != 0, new_elems))
            s = 0
            for i in h:
                if isinstance(i, (int, float)):
                    s += i
            q = list(filter(lambda a : not isinstance(a, (int, float)), h))
            obj = object().__new__(cls)
            object.__setattr__(obj, 'elems', q + [s] if (s != 0 or len(q) == 0) else q)
            return obj
            '''
            h = list(filter(lambda a : a != 0, new_elems))
            hcounter = group(h)
            new_arr = [mul([i, j]) for i, j in hcounter]
            s = 0
            for i in new_arr:
                if isinstance(i, (int, float)):
                    s += i
            
            h = new_arr[:]
            hcounter = group(h)
            
            while not singular(hcounter):
                
                new_arr = [mul([i, j]) for i, j in hcounter]
                s = 0
                for i in new_arr:
                    if isinstance(i, (int, float)):
                        s += i
                
                h = new_arr[:]
                hcounter = group(h)
                
            q = list(filter(lambda a : not isinstance(a, (int, float)), h))
            obj = object().__new__(cls)
            object.__setattr__(obj, 'elems', q + [s] if (s != 0 or len(q) == 0) else q)
            return obj
            
            
        
    
    def __call__(self, x):
        s = 0
        for i in self.elems:
            if callable(i):
                s += i(x)
            
            else:
                s += i
        
        return s
    def __str__(self):
        return " + ".join([str(i) for i in self.elems])
    
    def __add__(self, other):
        if isinstance(other, add):
            return add(self.elems[:] + other.elems[:])
        else:
            return add(self.elems[:] + [other])
    
    def __neg__(self):
        return add([mul([-1, i]) for i in self.elems])
    
    def __sub__(self, other):
        return self + mul([-1, other])
    
    def __mul__(self, other):
        if isinstance(other, add):
            arr1 = self.elems[:]
            arr2 = other.elems[:]
            new_arr = []
            for i in self.elems:
                for j in other.elems:
                    new_arr.append(mul([i, j]))
            
            return add(new_arr)
        
        else:
            return add([i * other for i in self.elems])

    def __eq__(self, other):
        if isinstance(other, add):
            return multiset(self.elems[:]) == multiset(other.elems[:])
        
        return False

    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        array = []
        for i in self.elems:
            if hasattr(i, 'diff') and callable(i.diff):
                array.append(i.diff())

        return add(array)
    
class mul(object):
    
    def __new__(cls, elems):
        if len(elems) == 1:
            return elems[0]
        if len(elems) == 0:
            return 0
        arr = []
        for i in elems:
            if isinstance(i, mul):
                arr += i.elems
        new_elems = list(filter(lambda x : not isinstance(x, mul), elems)) + arr
        for i in new_elems:
            if i == 0:
                return 0
        allbasic = True
        for i in new_elems:
            allbasic = allbasic and isinstance(i, (int, float))
        if allbasic:
            p = 1
            for i in new_elems:
                p *= i
            return p
        
        q = list(filter(lambda a : a != 1, new_elems))
        qcounter = group(q)
        new_arr = [pow([i, j]) for i, j in qcounter]
        p = 1
        for i in q :
            if isinstance(i, (int, float)):
                p *= i
        
        q = new_arr[:]
        qcounter = group(q)
        while not singular(qcounter):
            
            new_arr = [pow([i, j]) for i, j in qcounter]
            p = 1
            for i in q :
                if isinstance(i, (int, float)):
                    p *= i
            
            q = new_arr[:]
            qcounter = group(q)
            
        q = list(filter(lambda a : not isinstance(a, (int, float)), q))
        z = q + [p] if (p != 1 or len(q) == 0) else q
        array = []
        for i in range(len(z)):
            item = z[i]
            if isinstance(item, add):
                exc_q = mul(z[:i] + z[i+1:])
                for j in item.elems:
                    array.append(mul([j, exc_q]))
                
                return add(array[:])
               
        obj = object().__new__(cls)
        object.__setattr__(obj, 'elems', z)
        return obj
    
    def __call__(self, x):
        s = 1
        for i in self.elems:
            if callable(i):
                s *= i(x)
            
            else:
                s *= i
        
        return s
    def __str__(self) -> str:
        new_array = [str(self.elems[-1])]
        narr = [str(i) for i in list(filter(lambda x : not isinstance(x, (add, mul, div, pow, int, float)), self.elems[:]))]
        narr2 = ["(%s)"%str(i) for i in list(filter(lambda x : isinstance(x, (add, mul, pow, div)), self.elems[:]))]
        return "".join(new_array + narr + narr2)
        #return " * ".join(["(%s)"%str(i) for i in self.elems])
    
    def __mul__(self, other):
        if isinstance(other, mul):
            return mul(self.elems[:] + other.elems[:])
        else:
            narr = self.elems[:] + [other]
            return mul(narr[:])
        
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        narr = self.elems[:]
        narr[0] = mul([-1, narr[0]])
        return mul(narr[:])
    
    def __sub__(self, other):
        return self + mul([-1, other])

    def __eq__(self, other):
        if isinstance(other, mul):
            return multiset(self.elems[:]) == multiset(other.elems[:])
        
        return False

    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        array = []
        for i in range(len(self.elems)):
            if hasattr(self.elems[i], 'diff') and callable(self.elems[i].diff):
                mularray = self.elems[:]
                mularray.pop(i)
                mularray.append(self.elems[i].diff())
                mulobj = mul(mularray)
                array.append(mulobj)

        return add(array)

class div:
    def __init__(self, elems):
        self.elems = elems
        
    
    def __call__(self, x):
        s = self.elems[0](x) if callable(self.elems[0]) else self.elems[0]
        s /= self.elems[1](x) if callable(self.elems[1]) else self.elems[1]
        return s
    def __str__(self):
        return "((%s)"%str(self.elems[0]) + " / " + "(%s))"%str(self.elems[1])
    
    def inv(self):
        return div([self.elems[1], self.elems[0]])
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return div([mul([-1, self.elems[0]]), self.elems[1]])
    
    def __mul__(self, other):
        if isinstance(other, div):
            return div([mul([self.elems[0] , other.elems[0]]), mul([self.elems[1] , other.elems[1]])])
        
        narr1 = mul([self.elems[0], other]) 
        return div([narr1, self.elems[1]])
    
    def __truediv__(self, other):
        if isinstance(other, div):
            return mul([self, other.inv()])
        
        return div([self.elems[0], mul([self.elems[1] , other])])
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        f = self.elems[0] if hasattr(self.elems[0], 'diff') and callable(self.elems[0].diff()) else self.elems[0]
        g = self.elems[1] if hasattr(self.elems[1], 'diff') and callable(self.elems[1].diff()) else self.elems[1]
        
        return div([add([mul([f.diff(), g]), -mul([g.diff(), f])]), pow([g, 2])])
    
class pow(object):
    '''
    def __init__(self, elems):
        self.elems = elems[:]
    '''
    
    def __new__(cls, elems):
        if elems[1] == 0:
            return 1
        elif elems[1] == 1:
            return elems[0]
        elif elems[0] in [0, 1]:
            return elems[0]
        elif isinstance(elems[0], (int, float)) and isinstance(elems[1], (int, float)):
            return elems[0] ** elems[1]
        else:
            obj = object().__new__(cls)
            object.__setattr__(obj, 'elems', elems[:] if not isinstance(elems[0], pow) else [elems[0].elems[0], mul([elems[0].elems[1], elems[1]])])
            return obj
        
        
    
    def __call__(self, x):
        a = self.elems[0](x) if callable(self.elems[0]) else self.elems[0]
        
        return a ** (self.elems[1](x)) if callable(self.elems[1]) else a ** self.elems[1]
    
    def __str__(self):
        if not isinstance(self.elems[0], (add, mul, div)):
            string = str(self.elems[0])
            if not isinstance(self.elems[1], (add, mul, div)):
                string += "^%s"%str(self.elems[1])
        
        else:
            string = "(%s)^%s"%(str(self.elems[0]), str(self.elems[1]) if not isinstance(self.elems[1], (add, mul, div)) else "(%s)"%str(self.elems[1]))
            
        return string #"(%s) ^ (%s)"%(str(self.elems[0]), str(self.elems[1]))
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return self + mul([-1, other])
    
    def __mul__(self, other):
        if isinstance(other, pow):
            if other.elems[0] == self.elems[0]:
                return pow([self.elems[0], add([self.elems[1], other.elems[1]])])
            if other.elems[1] == self.elems[1]:
                return pow([mul([self.elems[0], other.elems[0]]), other.elems[1]])
        if isinstance(other, mul):
            inds = []
            curr_pow = self.elems[1]
            new_arr = other.elems[:]
            for i in range(len(other.elems)):
                if other.elems[i] == self.elems[0]:
                    inds.append[i]
            for j in inds:
                curr_pow = add([curr_pow, 1])
                new_arr.pop(j)
            
            new_arr.append(pow([self.elems[0], curr_pow]))
            return mul(new_arr[:])
                
        return mul([self, other])
    def __truediv__(self, other):
        if isinstance(other, pow):
            if other.elems[0] == self.elems[0]:
                return pow([self.elems[0], add([self.elems[1], mul([-1, other.elems[1]])])])
            if other.elems[1] == self.elems[1]:
                return pow([div([self.elems[0], other.elems[0]]), other.elems[1]])
            
        return div([self, other])
    
    def __eq__(self, other):
        if isinstance(other, pow):
            return self.elems[:] == other.elems[:]
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        if callable(self.elems[1]):
            return mul([self, mul([log(self.elems[0]), self.elems[1]]).diff()])
        
        else:
            return mul([self.elems[1], self.elems[0].diff(), pow([self.elems[0], add([self.elems[1], -1])])])

class sub(object):
    def __new__(cls, elems):
        return add([elems[0], mul([-1, elems[1]])])   

class log:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.log(self.input(x)) if callable(self.input) else math.log(self.input)
    
    def __str__(self) -> str:
        return "log(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), self.input]) if callable(self.input) else 0

class exp:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.exp(self.input(x)) if callable(self.input) else math.exp(self.input)
    
    def __str__(self) -> str:
        return "exp(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return mul([self.input.diff(), self]) if callable(self.input) else 0

class sin:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.sin(self.input(x)) if callable(self.input) else math.sin(self.input)
    
    def __str__(self) -> str:
        return "sin(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return mul([self.input.diff(), cos(self.input)]) if callable(self.input) else 0
class cos:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.cos(self.input(x)) if callable(self.input) else math.cos(self.input)
    
    def __str__(self) -> str:
        return "cos(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return mul([mul([-1, self.input.diff()]), sin(self.input)]) if callable(self.input) else 0

class tan:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.tan(self.input(x)) if callable(self.input) else math.tan(self.input)
    
    def __str__(self) -> str:
        return "tan(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), pow([cos(self.input), 2])]) if callable(self.input) else 0

class cot:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return 1/math.tan(self.input(x)) if callable(self.input) else 1/math.tan(self.input)
    
    def __str__(self) -> str:
        return "cot(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([mul([-1, self.input.diff()]), pow([sin(self.input), 2])]) if callable(self.input) else 0

class atan:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.atan(self.input(x)) if callable(self.input) else math.atan(self.input)
    
    def __str__(self) -> str:
        return "atan(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), add([1, pow([self.input, 2])])]) if callable(self.input) else 0

class asin:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.asin(self.input(x)) if callable(self.input) else math.asin(self.input)
    
    def __str__(self) -> str:
        return "asin(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), pow([add([1, -pow([self.input, 2])]), 0.5])]) if callable(self.input) else 0

class acos:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.acos(self.input(x)) if callable(self.input) else math.acos(self.input)
    
    def __str__(self) -> str:
        return "acos(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([mul([-1, self.input.diff()]), pow([add([1, -pow([self.input, 2])]), 0.5])]) if callable(self.input) else 0

class sinh:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.sinh(self.input(x)) if callable(self.input) else math.sinh(self.input)
    
    def __str__(self) -> str:
        return "sinh(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return mul([self.input.diff(), cosh(self.input)]) if callable(self.input) else 0
class cosh:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.cosh(self.input(x)) if callable(self.input) else math.cosh(self.input)
    
    def __str__(self) -> str:
        return "cosh(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return mul([self.input.diff(), sinh(self.input)]) if callable(self.input) else 0

class tanh:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.tanh(self.input(x)) if callable(self.input) else math.tan(self.input)
    
    def __str__(self) -> str:
        return "tanh(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), pow([cosh(self.input), 2])]) if callable(self.input) else 0

class atanh:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.atanh(self.input(x)) if callable(self.input) else math.atanh(self.input)
    
    def __str__(self) -> str:
        return "atanh(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), add([1, -pow([self.input, 2])])]) if callable(self.input) else 0

class asinh:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.asinh(self.input(x)) if callable(self.input) else math.asinh(self.input)
    
    def __str__(self) -> str:
        return "asinh(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), pow([add([1, pow([self.input, 2])]), 0.5])]) if callable(self.input) else 0

class acosh:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.acosh(self.input(x)) if callable(self.input) else math.acosh(self.input)
    
    def __str__(self) -> str:
        return "acos(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), pow([add([-1, pow([self.input, 2])]), 0.5])]) if callable(self.input) else 0

class atan:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.atan(self.input(x)) if callable(self.input) else math.atan(self.input)
    
    def __str__(self) -> str:
        return "atan(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), add([1, pow([self.input, 2])])]) if callable(self.input) else 0

class asin:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.asin(self.input(x)) if callable(self.input) else math.asin(self.input)
    
    def __str__(self) -> str:
        return "asin(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), pow([add([1, -pow([self.input, 2])]), 0.5])]) if callable(self.input) else 0

class sqrt:
    def __init__(self, inp):
        self.input = inp
    
    def __call__(self, x):
        return math.sqrt(self.input(x)) if callable(self.input) else math.sqrt(self.input)
    
    def __str__(self) -> str:
        return "sqrt(%s)"%str(self.input)
    
    def __add__(self, other):
        return add([self, other])
    
    def __neg__(self):
        return mul([-1, self])
    
    def __sub__(self, other):
        return add([self, mul([-1, other])])
    
    def __mul__(self, other):
        return mul([self, other])
    
    def __truediv__(self, other):
        return div([self, other])
    
    def __eq__(self, other) :
        if isinstance(other, type(self)):
            return self.input == other.input
        
        return False
    
    __rmul__ = __mul__
    __radd__ = __add__
    
    def diff(self):
        return div([self.input.diff(), mul([2, pow([self.input, 0.5])])]) if callable(self.input) else 0



    
FUNCTIONS = [identity, log, exp, sin, cos, tan, cot, asin, acos, atan, sinh, tanh, cosh, atanh, asinh, acosh, sqrt]
FUNCTIONS += 12 * [identity]


def generate_random_pow_hard():
    x = identity("x")
    y, z = random.choice(FUNCTIONS)(x), random.choice(FUNCTIONS)(x)
    return mul([random.randint(1, 10), pow([y, z])])

def generate_random_mul_hard(num=None):
    arr = [generate_random_pow_hard() for i in range(random.randint(1, 3) if num is None else num)]
    return mul(arr)

def generate_random_add_hard(num=None):
    arr = [generate_random_mul_hard() for i in range(random.randint(1, 3) if num is None else num)]
    return add(arr)

def generate_random_div_hard():
    a, b = generate_random_add_hard(), generate_random_add_hard()
    return div([a, b])


def generate_random_poly(deg=3):
    x = identity("x")
    return add([mul([random.randint(1, 10), pow([x, i])]) for i in range(deg + 1)])

def generate_random_divpoly(deg1, deg2):
    return div([generate_random_poly(deg1), generate_random_poly(deg2)])

def generate_random_pow(ranges=[1, 3]):
    x = identity("x")
    return pow([random.choice(FUNCTIONS)(x), random.randint(ranges[0], ranges[1])])
    
def generate_random_mul(num=None):
    arr = [generate_random_pow() for i in range(random.randint(1, 3) if num is None else num)]
    return mul(arr)
def generate_random_function(depth = 2):
    NEW_FUNCTIONS = [identity, log, exp, sin, cos, tan, cot, asin, acos, atan, sinh, tanh, cosh, atanh, asinh, acosh, sqrt]
    NEW_FUNCTIONS += 2 * [atan] + 2 * [asin] + 2*[acos]
    x = identity("x")
    new_func = random.choice(NEW_FUNCTIONS)(x)
    for i in range(depth - 1):
        new_func = random.choice(NEW_FUNCTIONS)(new_func)
    
    return new_func
y = generate_random_function(depth=2)
print(y)
print("#################################################")
print(y.diff())
print(y.diff()(1/2))
