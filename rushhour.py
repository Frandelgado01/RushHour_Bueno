import sys

# QUE: Funcion que recibe la posicion de la cadena(0-35) y calcula la fila y la columna
# PORQUE: El nivel llega como una cadena y hay que traducirlo a filas y columnas 
def calculo_casilla(posicion):
    fila = posicion // 6
    columna = posicion % 6
    return fila, columna

# QUE: Funcion que recibe fila y columna y devuelve la posicion de la cadena
# PORQUE: necesitamos hacer este calculo para la pregunta --what
def calculo_posicion(fila, columna):
    posicion = fila * 6 + columna
    return posicion

def vehiculoHorizontal (lista):
    filas = []
    for posicion in filas:
        filas.append(calculo_casilla(posicion))
    for i in range(1, len(lista)):
        if lista[i] != lista [i] - 1:
            return False
        
    return True

def vehiculoVertical (lista):
    for i in range(1, len(lista)):
        if lista[i] != lista[i + 6]:
            return False
        
    return True
    

# QUE: Comprueba si el nivel es valido y devuelve el codigo de error o 0 si es correcto
# PORQUE: Accion verify de T1
def verify(nivel):
    # Een caso de incumplirse dos casos de error, no se garantiza que se de el error de menor número primero, es decir, si se incumplen 6 y 7, puede saltar cualquiera, el orden depende de la ordenación interna de python de dict
    if len(nivel) != 36:  
        return 1
    
    for caracter in nivel:

        if (caracter < "A" or caracter > "Z") and caracter != "o":
            return 2
        
    if "A" not in nivel: 
        return 3

    coche_rojo = []

    for posicion, caracter in enumerate (nivel):
        if caracter == "A":
            fila, columna = calculo_casilla (posicion) 
            
            coche_rojo.append((fila, columna))

    # En el enunciado no se marca si el coche rojo es de 2 o de 3 de tamaño, asumimos que al ser un coche, es de 2, en caso de no ser cierto, se considera erróneo, caso 6
    if len(coche_rojo) != 2:
        # Este resultado se puede obtener en otros puntos, se en unas líneas más adelante, pero ponemos la comprobación del coche rojo para que sea una invariante
        return 6

    # Comprueba que alguna de las filas del coche rojo sea la de salida
    if not (coche_rojo[0][0] == 2 or coche_rojo[1][0] == 2):
        return 4

    if coche_rojo[0][0] != coche_rojo[1][0]:
        return 5

    # Comprobamos que el coche rojo esté conexo/junto
    if coche_rojo[0][1] != coche_rojo[1][1] -1:
        # Es caso 6 porque si no están juntas, siginifica que son dos letras A separadas, y sólo dos por la invariante de len(coche_rojo) == 2
        return 6

    # resto de comprobaciones del caso 6
    vehiculos = {}
    for posicion, caracter in enumerate (nivel):
        if caracter != "o":
            if caracter not in vehiculos:
                vehiculos[caracter] = []
            vehiculos[caracter].append(calculo_casilla(posicion))

    for vehiculo, posiciones in vehiculos.items():
        if len(posiciones) < 2:
            return 6

        # como se recorre en orden, las posiciones también van a estar ordenadas, es decir, primero tendremos la posición de más arriba a la izquierda
        
        # si es un coche horizontal, de 2 de tamaño, sus columnas tienen que estar contiguas
        if len(posiciones) == 2 and posiciones[0][0] == posiciones[1][0] and not posiciones[0][1] == posiciones[1][1] -1:
            return 7
        # si es un coche vertical, de 2 de tamaño, sus filas tienen que estar contiguas
        elif len(posiciones) == 2 and posiciones[0][1] == posiciones[1][1] and not posiciones[0][0] == posiciones[1][0] -1:
            return 7
        # si es un coche horizontal, de 3 de tamaño, sus columnas tienen que estar contiguas
        elif len(posiciones) >= 3 and posiciones[0][0] == posiciones[1][0] and not (posiciones[0][0] == posiciones[2][0] and posiciones[0][1] == posiciones[1][1] -1 and posiciones[0][1] == posiciones[2][1] -2):
            return 7
        # si es un coche vertical, de 3 de tamaño, sus filas tienen que estar contiguas
        elif len(posiciones) >= 3 and posiciones[0][1] == posiciones[1][1] and not (posiciones[0][1] == posiciones[2][1] and posiciones[0][0] == posiciones[1][0] -1 and posiciones[0][0] == posiciones[2][0] -2):
            return 7
        # si las dos primeras posiciones, no están en la misma fila o misma columna
        elif posiciones[0][0] != posiciones[1][0] and posiciones[0][1] != posiciones[1][1]:
            return 7

        if len(posiciones) > 3:
            return 6

    return 0      

# QUE: Calcula las posiciones de un vehiculo
# PORQUE: Accion question whereis de T1
def question_whereis(nivel, vehiculo):
    posiciones = []
    for posicion, caracter in enumerate (nivel):
        if caracter == vehiculo:
            posiciones.append(calculo_casilla(posicion))
    return posiciones

# QUE: Calcula que hay en una posicion del nivel
# PORQUE: Acción de question what de T1
def question_what(nivel, celda):
    return nivel[calculo_posicion(celda[0], celda[1])]

# QUE: Calcula el tamaño del vehiculo especificado
# PORQUE: Accion de question size de T1
def question_size(nivel, vehiculo):
    cuenta = 0
    for caracter in nivel:
        if caracter == vehiculo:
            cuenta += 1
    return cuenta

# QUE: Calcula el numero de vehiculos en el nivel
# PORQUE: Accón de question howmany de T1
def question_howmany(nivel):
    vehiculos = set()
    for caracter in nivel:
        if caracter != "o":
            if caracter not in vehiculos:
                vehiculos.add(caracter)
    return len(vehiculos)





accion = sys.argv[1]
nivel = sys.argv[3]


if accion == "question":
    pregunta = sys.argv[4]
    if pregunta == "--howmany":
        print(question_howmany(nivel))
    elif pregunta == "--size":
        vehiculo = sys.argv[5]
        print(question_size(nivel, vehiculo))
    elif pregunta == "--what":
        celda_str = sys.argv[5]
        celda = (int(celda_str[0]), int(celda_str[2]))
        print(question_what(nivel, celda))
    elif pregunta == "--whereis":
        vehiculo = sys.argv[5]
        posiciones = question_whereis(nivel, vehiculo)
        for posicion in posiciones:
            print(f"({posicion[0]},{posicion[1]})", end = "")
        print()
    else:
        print("Pregunta desconocida")
        
elif accion == "verify":
    print(verify(nivel))
else : 
    print("Acción desconocida")





