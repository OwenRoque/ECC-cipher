"""
Clase que representa un punto en el plano cartesiano
"""
class Punto:
    
    #Punto al infinito
    infinite_point = None
    
    def __init__(self, x = 0, y = 0):
        """
        Constructor de la clase Punto
        Args:
            x (int, 0): coordenada x. Defaults to 0.
            y (int, 0): coordenada y. Defaults to 0.
        """
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, another_point):
        if not another_point:
            return False
        # Verifica si ambos puntos son infinitos, hay que revisarla para descifrar
        if self is self.infinite_point and another_point is another_point.infinite_point:
            return True
        # Comparar los atributos x e y
        return self.x == another_point.x and self.y == another_point.y

    def set(self, x, y):
        '''Define los valores de x y y a este punto'''
        self.x = x
        self.y = y

