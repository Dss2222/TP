import copy

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''

    grilla = []
    for fila in desc:
        lista = []
        for caracter in fila:
            lista += caracter
        grilla += [lista]
    return grilla


def dimensiones(grilla): 
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    return (len(grilla[0]) ,len(grilla))


def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == '#'


def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] in ('.', '*', '+')


def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] in ('$', '*')


def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] in ('@', '+')


def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for fila in grilla:
        if ('$' in fila or '.' in fila):
            return False
    return True


def obtener_posicion_del_jugador(grilla):
    for i in range(len(grilla)):
        for j in range(len(grilla[0])):
            if (hay_jugador(grilla, j, i)):
                return (j, i)


def obtener_posicion_adyacente(coord, direccion):
    return (coord[0] + direccion[0], coord[1] + direccion[1])


def mover_jugador(grilla, pos_inicial, pos_final):
    if hay_objetivo(grilla, pos_inicial[0], pos_inicial[1]):
        grilla[pos_inicial[1]][pos_inicial[0]] = '.'
    else:
        grilla[pos_inicial[1]][pos_inicial[0]] = ' '
    
    if hay_objetivo(grilla, pos_final[0], pos_final[1]):
        grilla[pos_final[1]][pos_final[0]] = '+'
    else:
        grilla[pos_final[1]][pos_final[0]] = '@'


def mover_caja(grilla, pos_final):
    if hay_objetivo(grilla, pos_final[0], pos_final[1]):
        grilla[pos_final[1]][pos_final[0]] = '*'
    else:
        grilla[pos_final[1]][pos_final[0]] = '$'


def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''

    # 1er paso: determinar adonde esta el jugador
    # 2do paso: determinar que hay al lado del jugador en la direccion indicada
    #   - si no hay nada, mover al jugador
    #   - si hay pared, no se modifica la grilla
    #   - si hay caja y luego pared, no se modifica la grilla
    #   - si hay caja y luego nada
    #   - si hay caja y luego objetivo
    pos_jugador = obtener_posicion_del_jugador(grilla) # (1, 2)
    pos_al_lado_jugador = (pos_jugador[0] + direccion[0], pos_jugador[1] + direccion[1]) # (c: 2, f: 2)

    nueva_grilla = copy.deepcopy(grilla)
    if hay_pared(grilla, pos_al_lado_jugador[0], pos_al_lado_jugador[1]):
        return nueva_grilla
    
    if hay_caja(grilla, pos_al_lado_jugador[0], pos_al_lado_jugador[1]):
        # A partir de aca, si que hay una caja en la pos_al_lado
        pos_caja = pos_al_lado_jugador
        pos_al_lado_caja = (pos_caja[0] + direccion[0], pos_caja[1] + direccion[1])
        if hay_pared(grilla, pos_al_lado_caja[0], pos_al_lado_caja[1]) or hay_caja(grilla, pos_al_lado_caja[0], pos_al_lado_caja[1]):
            return nueva_grilla
            
        # a partir de aca, del otro lado de la caja, no hay nada.
        mover_jugador(nueva_grilla, pos_jugador, pos_caja)
        mover_caja(nueva_grilla, pos_al_lado_caja)
        return nueva_grilla
    
    # Caso remanente: no hay ni caja ni pared enfrente al jugador
    mover_jugador(nueva_grilla, pos_jugador, pos_al_lado_jugador)
    return nueva_grilla


def mostrar_grilla(grilla):
    for lista in grilla:
        print(lista)
    print("-------------")


def main():
    grilla = crear_grilla([
        '##########',
        '#.$      #',
        '#@     . #',
        '#      $ #',
        '#        #',
        '##########',
    ])
    
    while not juego_ganado(grilla):
        mostrar_grilla(grilla)
        c = input("Ingrese a,w,s,d para mover al jugador: ")
        match c:
            case 'w':
                grilla = mover(grilla, (0, -1))
            case 'd':
                grilla = mover(grilla, (1, 0))
            case 's':
                grilla = mover(grilla, (0, 1))
            case 'a':
                grilla = mover(grilla, (-1, 0))
            case _:
                print("Valor invalido...")

    mostrar_grilla(grilla)

    print("Ganase el juegooOoOOOO!!!")

main()
