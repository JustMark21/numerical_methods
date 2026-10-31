import math


class Methods():
    def bisection(self, f, a, b, tick = 100, tol = 1e-10):
        self.history = []
        first = f(a)
        if first == 0:
            return a
        second = f(b)
        if second == 0:
            return b
        mid = 0
        if first*second > 0:
            return None
        for i in range(tick):
            mid = (a + b) / 2
            self.history.append(mid)
            if (b - a) / 2 < tol:
                return mid
            fmid = f(mid)
            if fmid * first < 0:
                b = mid
            elif fmid * second < 0:
                a = mid
            else:
                return mid
        return mid

    def false_position(self, f, a, b, tick = 100, tol = 1e-10):
        # p_2 = p_1 - (f(p_1)(p_1 - p_0)) / (f(p_1) - f(p_0))
        self.history = []
        first = f(a)
        if first == 0:
            return a
        second = f(b)
        if second == 0:
            return b
        p = 0
        p_old = 0
        if first*second > 0:
            return None
        for i in range(tick):
            p_old = p
            p = b - (second * (b - a)) / (second - first)
            self.history.append(p)
            if i > 0 and abs(p - p_old) < tol:
                return p
            fp = f(p)
            if fp * first < 0:
                b = p
                second = fp
            elif fp * second < 0:
                a = p
                first = fp
            else:
                return p
        return p

    def newton_mthd(self, f, fprime, a, tick = 100, tol = 1e-10):
        # p_1 = p_0 - f(p_0)/f'(p_0)
        self.history = []
        self.history.append(a)
        def newton(f, fprime, a):
            return a - f(a)/fprime(a)
        if fprime(a) == 0:
            return None
        if a == newton(f, fprime, a):
            return a
        for i in range(tick):
            if fprime(a) == 0:
                return None
            if abs(a - newton(f, fprime, a)) < tol:
                self.history.append(newton(f, fprime, a))
                return newton(f, fprime, a)
            a = newton(f, fprime, a)
            self.history.append(a)
        return None

    def secant_mthd(self, f, p0, p1, tick=100, tol=1e-10):
        # p_2 = p_1 - (f(p_1)(p_1 - p_0)) / (f(p_1) - f(p_0))
        self.history = []
        self.history.append(p0)
        self.history.append(p1)
        def secant(f, p0, p1):
            return p1 - (f(p1)*(p1 - p0))/(f(p1) - f(p0))
        if f(p1) - f(p0) == 0:
            return None
        if p1 == secant(f, p0, p1):
            return p1
        for i in range(tick):
            if f(p1) - f(p0) == 0:
                break
            if abs(p1 - secant(f, p0, p1)) < tol:
                self.history.append(secant(f, p0, p1))
                return secant(f, p0, p1)
            p2 = secant(f, p0, p1)
            self.history.append(p2)
            p0 = p1
            p1 = p2
        if f(p1) == 0:
            return p1
        return None

    def muller_mthd(self, f, p0, p1, p2, tick=100, tol=1e-10):
        # p_3 = p_2 - 2f(p_2) / (b +- sqrt(b^2 - 4af(p_2)))
        self.history = []
        self.history.append(p0)
        self.history.append(p1)
        self.history.append(p2)
        def muller(f, p0, p1, p2):
            h1 = p1 - p0
            h2 = p2 - p1
            d1 = (f(p1) - f(p0))/h1
            d2 = (f(p2) - f(p1))/h2
            a = (d2 - d1)/(h2 + h1)
            b = d2 + h2*a
            D = (b*b - 4*f(p2)*a)**0.5
            if abs(b - D) < abs(b + D):
                E = b + D
            else:
                E = b - D
            return p2 - 2*f(p2)/E
        if p0 == p1 or p1 == p2 or p0 == p2:
            return None
        for i in range(tick):
            if f(p2) == 0:
                break
            if p0 == p1 or p1 == p2 or p0 == p2:
                break
            try:
                if abs(p2 - muller(f, p0, p1, p2)) < tol:
                    self.history.append(muller(f, p0, p1, p2))
                    return muller(f, p0, p1, p2)
                p3 = muller(f, p0, p1, p2)
                self.history.append(p3)
                p0 = p1
                p1 = p2
                p2 = p3
            except ZeroDivisionError:
                break
        if f(p2) == 0:
            return p2
        return None


def print_results(name, f, r, p, alpha, history):
    print(name, r)
    print("k  p_n  f(p_n)  e_n  e_n/e_(n-1)^alpha")
    for k in range(len(history)):
        e_n = abs(history[k] - p)
        if k == 0:
            print(k, history[k], f(history[k]), e_n)
        else:
            e_old = abs(history[k-1] - p)
            ratio = e_n / e_old**alpha
            print(k, history[k], f(history[k]), e_n, ratio)
    print()


def print_bound(history, p, a, b):
    # e_n <= (b - a) / 2^n
    print("bisection error bound check")
    print("k  e_n  (b-a)/2^(k+1)  e_n<=bound")
    for k in range(len(history)):
        e_n = abs(history[k] - p)
        bound = (b - a) / 2**(k+1)
        print(k, e_n, bound, e_n <= bound)
    print()
  

m = Methods()

# Problem 1: beam deflection, f(x) = y'(x)
w0 = 2.5
E = 2e8
I = 3e-4
L = 5
def f1(x):
    return w0/(120*E*I*L) * (-5*x**4 + 6*L**2*x**2 - L**4)
def f1prime(x):
    return w0/(120*E*I*L) * (-20*x**3 + 12*L**2*x)
p1 = m.newton_mthd(f1, f1prime, 2, tol=1e-15)
print("Problem 1")
r = m.bisection(f1, 0, 4)
print_results("bisection", f1, r, p1, 1, m.history)
print_bound(m.history, p1, 0, 4)
r = m.false_position(f1, 0, 4)
print_results("false position", f1, r, p1, 1, m.history)
r = m.newton_mthd(f1, f1prime, 2)
print_results("newton", f1, r, p1, 2, m.history)
r = m.secant_mthd(f1, 1, 3)
print_results("secant", f1, r, p1, 1.618, m.history)
r = m.muller_mthd(f1, 1, 2, 3)
print_results("muller", f1, r, p1, 1.84, m.history)

# Problem 2: Kepler's equation
e = 0.65
M = 1.25
def f2(x):
    return x - e*math.sin(x) - M
def f2prime(x):
    return 1 - e*math.cos(x)
p2 = m.newton_mthd(f2, f2prime, M, tol=1e-15)
print("Problem 2")
r = m.bisection(f2, 0, math.pi)
print_results("bisection", f2, r, p2, 1, m.history)
print_bound(m.history, p2, 0, math.pi)
r = m.false_position(f2, 0, math.pi)
print_results("false position", f2, r, p2, 1, m.history)
r = m.newton_mthd(f2, f2prime, M)
print_results("newton", f2, r, p2, 2, m.history)
r = m.secant_mthd(f2, 0, math.pi)
print_results("secant", f2, r, p2, 1.618, m.history)
r = m.muller_mthd(f2, 0, 1, 2)
print_results("muller", f2, r, p2, 1.84, m.history)
