from CurvaEliptica import CurvaEliptica
from Entidad import Entidad
from Punto import Punto
from config import TABLE 


def prueba_curva():
    # Ejemplo de uso
    a = 2
    b = 2
    p = 17
    G = Punto(5, 1)
    curva = CurvaEliptica(a, b, p)

    print("k | kG | kG en EC?")
    print("------------------")
    for k in range(1, 20):
        kG = curva.mult(k, G)
        on_curve = curva.tiene(kG)
        print(f"{k} | {kG} | {on_curve}")
    print(f"\norden(G) = {curva.orden(G)}")
    print(f"cofactor(G) = {curva.cofactor(G)}")
    

def main():
    # Curva y punto G
    curva = CurvaEliptica(2, 9, 37)
    G = Punto(9, 4)
    # Puntos fijos de ejemplo
    punto_allice = Punto(10,20)
    punto_bob = Punto(11,20)

    # Creamos a Allice y Bob
    allice = Entidad("Allice", "Mensaje secreto de Allice", curva, G, curva.orden(G),5,punto_allice)
    bob = Entidad("Bob", "Mensaje secreto de Bob", curva, G, curva.orden(G),7,punto_bob)
    #print(f"Orden de G = {curva.orden(G)}")

    # Generamos y compartir llaves publicas de Allice y Bob
    allice.generaLlavesPublicas()
    #print(f"\nLlaves publicas de Allice {allice.pks}")
    bob.generaLlavesPublicas()
    #print(f"\nLlaves publicas de Bob {bob.pks}")
    # Allice recibe las llaves publicas de Bob
    allice.recibeLlavesPublicas(bob.pks)
    #print(f"\nAllice recibe las llaves de BOB y son: {allice.llaves_recibidas}")
    bob.recibeLlavesPublicas(allice.pks)
    #print(f"\nBob recibe las llaves de Allice y son: {bob.llaves_recibidas}")

    allice.llavesFinales()
    #print(f"\nLlaves finales de Allice {allice.pks}")
    #print("\nLlaves Publicas de Allice:", allice.pks)
    bob.llavesFinales()
    #print(f"\nLlaves finales de Bob{bob.pks}")
    #print(f"\nllaves Publicas de Bob:{ bob.pks}")
    #print("Intercambio de llaves públicas")
    # Intercambiamos la última clave de cada uno
    #allice.pks[2], bob.pks[2] = bob.pks[2] ,allice.pks[2] 
    # Allice recibe la ultima llave de Bob
    allice.llaves_recibidas.append(bob.pks[2])
    #allice.recibeLlavesPublicas(bob.pks)
    # Bob recibe la ultima llave de Allice
    bob.llaves_recibidas.append(allice.pks[2])
    #print("\nLlaves Públicas FINALES de Allice:", allice.pks)
    #print("\n Llaves recibidas de allice: ",allice.llaves_recibidas)
    #print("\nLlaves Públicas FINALES de BOB:", bob.pks)
    #print("\n Llaves recibidas de bob: ",bob.llaves_recibidas)
    
    # Bob cifra el mensaje 'Attack'
    mensaje_cifrado_bob = bob.cifrar('yaquierovacaciones',TABLE)
    print(f"Mensaje cifrado por BOB: {mensaje_cifrado_bob}")

    mensaje_descifrado = allice.descifrar(mensaje_cifrado_bob, TABLE)
    print(f"Mensaje descifrado : {mensaje_descifrado}")
    
    
if __name__ == "__main__":
    main()
