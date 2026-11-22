import sys
from bisect import insort
from timeit import timeit

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
# PORQUE: Acción de question howmany de T1
def question_howmany(nivel):
    vehiculos = set()
    for caracter in nivel:
        if caracter != "o":
            if caracter not in vehiculos:
                vehiculos.add(caracter)
    return len(vehiculos)


# QUE: Calcula si el nivel es objetivo, es decir, si el coche rojo esta en la salida
# PORQUE: Accón de question goal de T1
def question_goal(nivel):
    return question_what(nivel, (2, 5)) == "A"


# QUE: Genera los sucesores de un nivel
# PORQUE: Acción de sucesor goal T2
def succesors(nivel):
    # obtenemos los diferentes identificadores de vehiculos que exiten, quitamos los huecos ("o"), ordenamos alfabéticamente
    vehiculos = sorted(set(nivel) - {"o"})

    sucesores = []

    for vehiculo in vehiculos:
        posiciones = question_whereis(nivel, vehiculo)

        # es un vehiculo horizontal?
        if posiciones[0][0] == posiciones[1][0]:
            
            # nos quedamos con la posición más a la derecha del vehiculo
            inicio = posiciones[2][1] if len(posiciones) == 3 else posiciones[1][1]

            for desplazamiento, nueva_pos in enumerate(range(inicio+1, 6), 1):
                if nivel[calculo_posicion(posiciones[0][0], nueva_pos)] == "o":
                    nuevo_nivel_lista = list(nivel)
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(posiciones[0][0], posiciones[0][1]+i)] = "o"
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(posiciones[0][0], nueva_pos-i       )] = vehiculo

                    sucesores.append((f"{vehiculo}+{desplazamiento}", "".join(nuevo_nivel_lista), 6-desplazamiento))
                else:
                    break


            for desplazamiento, nueva_pos in enumerate(range(posiciones[0][1]-1, -1, -1), 1):
                if nivel[calculo_posicion(posiciones[0][0], nueva_pos)] == "o":
                    nuevo_nivel_lista = list(nivel)
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(posiciones[0][0], posiciones[0][1]+i)] = "o"
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(posiciones[0][0], nueva_pos+i       )] = vehiculo

                    sucesores.append((f"{vehiculo}-{desplazamiento}", "".join(nuevo_nivel_lista), 6-desplazamiento))
                else:
                    break
        else:
            for desplazamiento, nueva_pos in enumerate(range(posiciones[0][0]-1, -1, -1), 1):
                if nivel[calculo_posicion(nueva_pos, posiciones[0][1])] == "o":
                    nuevo_nivel_lista = list(nivel)
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(posiciones[0][0]+i, posiciones[0][1])] = "o"
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(nueva_pos+i,        posiciones[0][1])] = vehiculo

                    sucesores.append((f"{vehiculo}+{desplazamiento}", "".join(nuevo_nivel_lista), 6-desplazamiento))
                else:
                    break

            inicio = posiciones[2][0] if len(posiciones) == 3 else posiciones[1][0]

            for desplazamiento, nueva_pos in enumerate(range(inicio+1, 6), 1):
                if nivel[calculo_posicion(nueva_pos, posiciones[0][1])] == "o":
                    nuevo_nivel_lista = list(nivel)
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(posiciones[0][0]+i, posiciones[0][1])] = "o"
                    for i in range(len(posiciones)):
                        nuevo_nivel_lista[calculo_posicion(nueva_pos-i,        posiciones[0][1])] = vehiculo

                    sucesores.append((f"{vehiculo}-{desplazamiento}", "".join(nuevo_nivel_lista), 6-desplazamiento))
                else:
                    break

    return sucesores


# QUE: Aplica los cambios consecutivamente de la lista de acciones al nivel
# PORQUE: Question move T2
def move(nivel, lista_acciones):
    # Asume que la lista de acciones son válidas, es decir, que el coche no se sale, y que no pisa otros coches
    nuevo_nivel_lista = list(nivel)

    for accion in lista_acciones:
        vehiculo = accion[0]
        direccion = accion[1]
        desplazamiento = int(accion[2])
        
        posiciones = question_whereis("".join(nuevo_nivel_lista), vehiculo)

        if posiciones[0][0] == posiciones[1][0]:
            if direccion == "+":
                nueva_pos = posiciones[2][1] if len(posiciones) == 3 else posiciones[1][1] + desplazamiento
                for i in range(len(posiciones)):
                    nuevo_nivel_lista[calculo_posicion(posiciones[0][0], posiciones[0][1]+i)] = "o"
                    nuevo_nivel_lista[calculo_posicion(posiciones[0][0], nueva_pos-i       )] = vehiculo
            else:
                nueva_pos = posiciones[0][1] - desplazamiento
                for i in range(len(posiciones)):
                    nuevo_nivel_lista[calculo_posicion(posiciones[0][0], posiciones[0][1]+i)] = "o"
                    nuevo_nivel_lista[calculo_posicion(posiciones[0][0], nueva_pos+i       )] = vehiculo
        else:
            if direccion == "+":
                nueva_pos = posiciones[0][0] - desplazamiento
                for i in range(len(posiciones)):
                    nuevo_nivel_lista[calculo_posicion(posiciones[0][0]+i, posiciones[0][1])] = "o"
                    nuevo_nivel_lista[calculo_posicion(nueva_pos+i,        posiciones[0][1])] = vehiculo
            else:
                nueva_pos = posiciones[2][0] if len(posiciones) == 3 else posiciones[1][0] + desplazamiento
                for i in range(len(posiciones)):
                    nuevo_nivel_lista[calculo_posicion(posiciones[0][0]+i, posiciones[0][1])] = "o"
                    nuevo_nivel_lista[calculo_posicion(nueva_pos-i,        posiciones[0][1])] = vehiculo

    return "".join(nuevo_nivel_lista)


# QUE: Funcion recursiva que devuelve lista de nodos ordenados de raíz a solucion
# PORQUE: funcion camino T3
def construir_camino(nodo):
    if nodo is None:
        return []
    else:
        camino = construir_camino(nodo[1])
        camino.append(nodo)
        return camino


# QUE: ejecuta el algoritmo de búsqueda
# PORQUE: algoritmo busqueda t3
def algoritmo_busqueda(estado_inicial, estrategia_str, profundidad_max):
    # nodo_inicial: ( 0,  None,  "___", estado_inicial,     0,           0,          0,     0)
    # nodo:         (id, padre, accion,         estado, coste, profundidad, heuristica, valor)
    #                 0      1       2               3      4            5           6      7
   
    frontera = []
    nodo_inicial = (0, None, "___", estado_inicial, 0, 0, 0, 0)
    insort(frontera, nodo_inicial, key=lambda nodo: (nodo[7], nodo[0]))
    visitados = {}
    solucion = False
    visitados[estado_inicial] = nodo_inicial[7]

    tn = 1 # nodos generados
    cn = 0 # nodos podados
    en = 0 # nodos expandidos
    df = 0 # profundidad máxima
    tiempo_inicio = timeit() # para el tiempo

    while not solucion and len(frontera) != 0:
        nodo = frontera.pop(0)
        if question_goal(nodo[3]):
            solucion = True
        else:
            if nodo[5] >= profundidad_max or (nodo[3] in visitados and visitados[nodo[3]] < abs(nodo[7])):
                cn += 1
            else:
                visitados[nodo[3]] = abs(nodo[7])
                sucesores = succesors(nodo[3])
                for sucesor in sucesores:
                    nuevo_nodo = (tn, nodo, sucesor[0], sucesor[1], sucesor[2], nodo[5]+1, 0, 0)
                    nuevo_nodo = (tn, nodo, sucesor[0], sucesor[1], sucesor[2], nodo[5]+1, 0, selector_estrategia(estrategia_str, nuevo_nodo))
                    insort(frontera, nuevo_nodo, key=lambda nodol: (nodol[7], nodol[0]))
                    tn += 1
                if nodo[5] > df:
                    df = nodo[5]
                en += 1

    et = timeit() - tiempo_inicio # tiempo ejecucion

    camino = []
    if solucion:
        camino = construir_camino(nodo)

    return camino, et, tn, cn, en, df


# QUE: Devuelve el valor de la estrategia dado el nombre de esta
# PORQUE: Usar el parámetro de strategy de T3
def selector_estrategia(estrategia_str, nodo):
    if estrategia_str == "DFS":
        return -nodo[5]
    elif estrategia_str == "BFS":
        return nodo[5]
    elif estrategia_str == "UCS":
        return nodo[4]

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
    elif pregunta == "--goal":
        finalizado = question_goal(nivel)
        print("TRUE" if finalizado else "FALSE")
    elif pregunta == "--move":
        lista_acciones_str = sys.argv[5]
        lista_acciones = []
        for accion_str in lista_acciones_str.split(","):
            lista_acciones.append(accion_str)
        print(move(nivel, lista_acciones))
    else:
        print("Pregunta desconocida")
        
elif accion == "verify":
    print(verify(nivel))

elif accion == "successors":
    sucesores = succesors(nivel)

    for sucesor in sucesores:
        print(f"[{sucesor[0]},{sucesor[1]},{sucesor[2]}]")

elif accion == "solver":
    estrategia_str = sys.argv[5]
    profundidad_max = int(sys.argv[7])

    camino, et, tn, cn, en, df = algoritmo_busqueda(nivel, estrategia_str, profundidad_max)

    for nodo in camino:
        print(f"[{nodo[0]},{nodo[1][0] if nodo[1] is not None else None},{nodo[2]},{nodo[3]},{nodo[4]},{nodo[5]},{nodo[6]},{nodo[7]}]")

    if len(sys.argv) > 8 and sys.argv[8] == "--stats":
        print()
        print("ET:", et)
        print("TN:", tn)
        print("EN:", en)
        print("CN:", cn)
        print("DF:", df)

else: 
    print("Acción desconocida")



# coger en selector estrategia añadir A* y voraz de tal manera qeu la primera devuelva la suma de el coste + esuristica y voraz solo heuristica
# para calcular euristica, hay que crear una funion que a partir de un numero (0, 1, 2) nos de un valor para esa heuristica.
# 0 numero de casillas a la derecha del coche rojo; 1 numero de coches a la derecha del coche rojo; 2 suma de heuristica 0 + 1 

