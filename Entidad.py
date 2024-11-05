import random
from config import ENTITY_LOGGS
"""
    Clase para representar una entidad que cifra y descifra mensajes
"""
class Entidad:
    def __init__(self, nombre, mensaje, curva, G, orden_G, llave_privada=None, punto_privado=None):
        """
        Constructor de la clase Entidad
        Args:
            nombre (str): nombre de la entidad
            mensaje (str): mensaje a cifrar
            curva (CurvaEliptica): curva elíptica
            G (Punto): punto generador
            orden_G (int): orden del punto generador
            llave_privada (Punto): llave privada de la entidad.
            punto_privado (Punto): punto privado de la entidad.
        """
        self.nombre = nombre
        self.mensaje = mensaje
        self.curva = curva
        self.G = G
        self.orden_G = orden_G
        self.llave_privada = llave_privada if llave_privada is not None else random.randint(1, orden_G)
        if punto_privado is None:
            self.punto_privado = self.curva.mult(self.llave_privada, G)  
        else:
            self.punto_privado = punto_privado
        self.pks= []
        self.llaves_recibidas = []

    def __str__(self):
      return f"Entidad: {self.nombre}, Mensaje: {self.mensaje}, Curva Eliptica: {str(self.curva)}, Punto Generador: {str(self.G)}, Orden de G: {self.orden_G}, Llave Privada: {self.llave_privada}, Punto Privado: {str(self.punto_privado)}, Llaves Publicas: {self.pks}, Llaves Recibidas: {self.llaves_recibidas}"
  
    def cifrar(self, mensaje, tabla):
        """
            Cifra un mensaje usando la curva elíptica
        Args:
            mensaje (str): mensaje a cifrar
            tabla (dict): tabla de caracteres

        Returns:
            str: mensaje cifrado
        """
        if ENTITY_LOGGS:
            print(f"CIFRADO DE MENSAJE {mensaje}")
        mensaje_cifrado = []
        for caracter in mensaje:
            r = random.randint(1, self.orden_G)
            if ENTITY_LOGGS:
                print(f"caracter '{caracter}' cifrado como:")
                print(f"random = {r}")
            # e1 = r(C)
            e1 = self.curva.mult(r, self.G)
            caracter_e1 =self.obtener_caracter(tabla,e1) 
            if ENTITY_LOGGS:
                print(f"{caracter} => {e1} = {caracter_e1}\n", end="")
            # e2 = M + (β + r)A1 − r(A2) + Ae
            M = tabla[caracter]
            beta_r_A1 = self.curva.mult(self.llave_privada+r, self.llaves_recibidas[0])
            r_A2 = self.curva.mult(r, self.llaves_recibidas[1])
            e2 = self.curva.suma(M, beta_r_A1)
            e2 = self.curva.resta(e2,r_A2)
            e2 = self.curva.suma(e2,self.llaves_recibidas[2])
            caracter_e2 = self.obtener_caracter(tabla,e2)
            if ENTITY_LOGGS:
                print(f"{caracter} => {e2} = {caracter_e2}\n", end="")

            # Agregar los puntos (e1, e2) al mensaje cifrado
            mensaje_cifrado.append((caracter_e1, caracter_e2))

        return mensaje_cifrado

    def descifrar(self, mensaje_cifrado, tabla):
        """
            Descifra un mensaje cifrado usando la curva elíptica
        Args:
            mensaje_cifrado (str): mensaje cifrado
            tabla (dict): tabla de caracteres 

        Returns:
            str: mensaje descifrado
        """
        mensaje_descifrado = []

        for tupla in mensaje_cifrado:
            caracter1 = tupla[0]
            caracter2 = tupla[1]
            
            # M = e2 - (alpha(e1) + alpha(B1) + Be)
            
            if caracter1 is None or caracter2 is None:
                mensaje_descifrado.append(None)
            else:
                #Punto e1
                e1 = tabla[caracter1]
                #Punto e2
                e2 = tabla[caracter2]

                alpha_e1 = self.curva.mult(self.llave_privada, e1)
                alpha_B1 = self.curva.mult(self.llave_privada, self.llaves_recibidas[0])

                a_e1_b1 = self.curva.suma(alpha_e1, alpha_B1)
                suma_be = self.curva.suma(a_e1_b1, self.llaves_recibidas[2])

                # M 
                punto_M = self.curva.resta(e2, suma_be)
                punto_descifrado = self.obtener_caracter(tabla, punto_M)
                if ENTITY_LOGGS:
                    print(f"e1: {e1} e2: {e2} B1: {self.llaves_recibidas[0]} Be: {self.llaves_recibidas[2]}")
                    print(f"El punto que corresponde es: {punto_M}")
                    print(f"El punto descifrado final es: {punto_descifrado}")
                mensaje_descifrado.append(punto_descifrado)


        return mensaje_descifrado


    def generaLlavesPublicas(self):
        """
            Genera las llaves públicas de la entidad
        """
        C_mas_A = self.curva.suma(self.G, self.punto_privado)
        A1 = self.curva.mult(self.llave_privada, C_mas_A)
        A2 = self.curva.mult(self.llave_privada, self.punto_privado)
        self.pks.append(A1)
        self.pks.append(A2)

    def recibeLlavesPublicas(self, pks):
        """
            Recibe las llaves públicas de otra entidad
        Args:
            pks (list): lista de llaves públicas
        Raises:
            ValueError: si no se proporcionan dos llaves públicas 
        """
        if isinstance(pks, list) and len(pks) >= 2:
            self.llaves_recibidas.extend(pks)  
        else:
            raise ValueError("Se deben proporcionar un par de llaves públicas.")

    def llavesFinales(self):
        """
            Genera la llave final de la entidad
        Raises:
            ValueError: si no se han recibido suficientes llaves públicas para generar la llave final
        Returns:
            list: lista con las llaves finales 
        """
        if len(self.llaves_recibidas) == 2:
            Pk2 = self.llaves_recibidas[1]
            Pke = self.curva.mult(self.llave_privada, Pk2)
            self.pks.append(Pke)
            print(f"Llave final de {self.nombre}: {Pke}")
            return self.pks
        else:
            raise ValueError("Error: No se han recibido suficientes llaves públicas para generar la llave final.")

    def obtener_caracter(self, diccionario, punto):
        """
            Obtiene el caracter que corresponde a un punto en la curva
        Args:
            diccionario (dict): diccionario de caracteres
            punto (Punto): punto en la curva

        Returns:
            char: caracter correspondiente al punto
        """
        for key, value in diccionario.items():
            if value == punto:
                return key
        return None
