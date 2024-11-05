from Punto import Punto
"""
    Clase que representa una curva elíptica de la forma y^2 = x^3 + ax + b (mod p)
"""
class CurvaEliptica:
    
    def __init__(self, a, b, p):
        """
        Constructor de la clase CurvaEliptica
        Args:
            a (int): coeficiente a de la curva
            b (int): coeficiente b de la curva
            p (int): coeficiente p de la curva
        """
        self.a = a
        self.b = b
        self.p = p
        self.infinito = Punto(None, None)

    def __str__(self):
        return f"Curva Eliptica: y^2 = x^3 + {self.a}x + {self.b} (mod {self.p})"

    def tiene(self, punto):
        """
            Verifica si un punto está en la curva
        Args:
            punto (Punto): punto a evaluar
        Returns:
            bool : True si el punto está en la curva, False en otro caso 
        """
        if punto == self.infinito:
            return True  # El punto al infinito siempre está en la curva
        return (punto.y ** 2) % self.p == (punto.x ** 3 + self.a * punto.x + self.b) % self.p

    def puntos(self):
        """
            Devuelve una lista de todos los puntos en la curva
        Returns:
            list: lista de puntos en la curva
        """
        puntos = [self.infinito]
        for x in range(self.p):
            for y in range(self.p):
                punto = Punto(x, y)
                if self.tiene(punto):
                    puntos.append(punto)
        return puntos

    def orden(self, punto):
        """
            Calcula el orden de un punto en la curva
        Args:
            punto (Punto): punto a evaluar

        Returns:
            int : valor del orden del punto
        """
        k = 1
        while True:
            resultado = self.mult(k, punto)
            if resultado == self.infinito:
                return k
            k += 1

    def cofactor(self, punto):
        """
            Calcula el cofactor de un punto en la curva
        Args:
            punto (Punto): punto a evaluar

        Returns:
            int : valor del cofactor del punto
        """
        return len(self.puntos()) // self.orden(punto)

    def suma(self, p, q):
        """
            Realiza la suma de dos puntos en la curva
        Args:
            p (int): coeficiente p de la curva
            q (int): coeficiente q de la curva

        Returns:
            Punto : punto resultante de la suma
        """
        if p == self.infinito:
            return q
        if q == self.infinito:
            return p
        if p.x == q.x and (p.y != q.y or p.y == 0):
            return self.infinito
        if p != q:
            lam = ((q.y - p.y) * pow(q.x - p.x, self.p - 2, self.p)) % self.p
        else:
            lam = ((3 * p.x ** 2 + self.a) * pow(2 * p.y, self.p - 2, self.p)) % self.p
        x3 = (lam ** 2 - p.x - q.x) % self.p
        y3 = (lam * (p.x - x3) - p.y) % self.p
        return Punto(x3, y3)
    
    def resta(self, p, q):
        """
            Resta dos puntos en la curva
        Args:
            p (int): coeficiente p de la curva
            q (int): coeficiente q de la curva

        Returns:
            Punto : punto resultante de la resta
        """
        # Calcular el inverso aditivo de q
        q_inverso = self.inv(q)
        
        # Realizar la suma P + (-Q)
        resultado = self.suma(p, q_inverso)
        
        return resultado

    def mult(self, k, punto):
        """
            Realiza la multiplicación de un punto por un escalar
        Args:
            k (int): escalar
            punto (Punto): punto a multiplicar

        Returns:
            Punto : punto resultante de la multiplicación
        """
        if k == 0:
            return self.infinito
        resultado = self.infinito
        addend = punto
        while k:
            if k & 1:
                resultado = self.suma(resultado, addend)
            addend = self.suma(addend, addend)
            k >>= 1
        return resultado

    def inv(self, punto):
        """
            Calcula el inverso aditivo de un punto
        Args:
            punto (Punto): punto a evaluar

        Returns:
            Punto : punto resultante del inverso aditivo
        """
        return Punto(punto.x, -punto.y % self.p)
