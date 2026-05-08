*Este proyecto ha sido creado como parte del currículo de 42 por iarrien- y aeiros-t*

# A-maze-ing — Proyecto 42

El objetivo de este proyecto es implementar un generador de laberintos en Python que reciba un archivo de configuración, gener un laberinto, posiblemente perfecto(con un único camino entre la entrada(entry) y la salida(exit)), y escriba dicho laberinto a un archivo usando hexadecimales para representar muros. También se deberá proveer una reprentación visual del laberinto generdo.

---

## Índice

1. [Descripción](#descripción)  
1.1. [Descripción General](#descripción-general)
2. [Instrucciones](#instrucciones)  
2.1. [Estructura del Proyecto](#ejecución-del-programa)  
2.1.1 [Reutilización del código](#reutilización-del-código)  
2.2. [Ejecución del Programa](#selectores-de-estrategia)  
3. [Algoritmos empleados para la generación del laberinto](#algoritmos-implementados)  
4. [Contribuciones](#contribuciones)   
5. [Recursos](#recursos)
---

# Descripción

## Descripción General

La generación del laberinto parte de los parametros incluidos en el archivo config.txt. En este archivo se describirán los parametros del laberinto. La estructura del archivo config.txt es la siguiente:

| Key | Descripton |
|----------|-------------|
| **WIDTH** | La anchura del laberinto(numero de columnas). |
| **HEIGHT** | La altura del laberinto(numero de filas). |
| **ENTRY** | El punto de entrada del laberinto (x,y). |
| **EXIT** | El punto de salida del laberinto (x,y). |
| **OUTPUT_FILE** | El nombre del archivo de salida donde se van a guardar los datos. |
| **PERFECT** | Una flag para determinar si el laberinto a crear es perfecto o no (True o False). |
| **DISPLAY_MODE** | Campo opcional para elegir entre los dos modos de visualización disponibles (Normal o Animado). |
| **SEED** | Campo opcional para incluir una semilla para poder regenerar el mismo laberinto. |
| **ALGORITHM** | Campo opcional para decidir entre los dos algoritmos de creacion implementados (Prim o Kruskal). |

A continuación se muestra un ejemplo de un archivo config.txt válido:

```txt
WIDTH=25
HEIGHT=25
ENTRY=0,0
EXIT=24,24
OUTPUT_FILE=maze.txt
DISPLAY_MODE=Normal
PERFECT=True
ALGORITHM=prim
```

Una vez generado el laberinto, se debe escribir en un archivo de salida, usando un digito hexadecimal para representar cada celda. El hexadecimal representa los muros basado en la siguiente tabla:


| Bit | Dirección |
|----------|-------------|
| **0**(LSB) | Norte |
| **1** | Este |
| **2** | Sur |
| **3** | Oeste |

Si hay un muro, se representa con un 1, y si no hay muro se representa con 0.
Ejemplo:  3 (binario 0011) significa que hay muros al **Norte** y al **Este**. A
(binario 1010) significa que hay muros al **Este** y al **Oeste**.

Las celdas se escriben fila a fila, escribiendo una fila en cada linea. Al terminar de escribir el laberinto, se ha de dejar un salto de linea y después se han de insertar tres datos, uno en cada linea: punto de entrada al laberinto, punto de salida del laberinto y el camino valido más corto desde la entrada hasta la salida.

Siguiendo el ejemplo del config.txt descrito antes, a continuación se describe un ejemplo de un output de salida(maze.txt en el ejemplo de arriba):

```txt
BD5391553B95517955179153B
A93C6A95686D3C5697C52ABAA
C6C556C3969543D52953EAC2A
9539117AAD293C516ABC3C3AA
AD6AAE96C3C2C3969683C56C2
853AA9693C3C7AA96BAC55556
A92AC6D287C516EA96C155793
AAEC553AC553A956C13A953AA
AA95556AD13C6A953E86C3C6A
AAA93D5296A93C47C3AD3A952
EAC6C53AAFC6AFFF96C56AC3A
941557AC2FD5057F853956BAE
83E955696FFFAFFFC7AC516C3
AC3A93BAD13FAFD5156956952
C3C6AA8456EFAFFFC53A956BA
BC53AAE9553BA95393C6A9786
853C6C5695686A96AC3BAA96B
C7815795693C56A9296AA86D2
956E93AD16AD17AEAA96AC552
A9556AC56BC385696A83C5396
AAD13C551296C3D296EC13AC7
AC3AC5396EC53C56A9556EC53
83AC53AC55556939469395552
AEA956AD55153EC4796AA917A
C546D545556D455556D46EC56

0,0
24,24
SSENESEEENNEEESWWSESSWSWSWNNNWSSSSEEESWWWWSSENESEESSWWWSSWNWNWSSESEESENNNESSSEENEEESWWSWWSSEENENESSESWSEESWWWWWNENWWWNNWSWWWSSESSSENEENWWNNESEESSSEEEENEESEEEEENENESSENNEEEESS
```

# Instrucciones

## Estructura del proyecto

El programa muestra en una interfaz gráfica el laberinto generado, mientras que por la terminal se muestra el menú para poder interactuar con el programa. A continuación se van a desribir las clases más importantes del código.

### `Parser`

La clase Parser se encarga de verificar los datos introducidos en el archivo de configuración. En caso de error, lanza una excepción para que luego el programa principal la reciba, imprima el error y termine la ejecución.
Tiene el siguiente TypeDict con todos los parametros de entrada del archivo de configuración:

```Python
class Config(TypedDict):

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    ANIMATION: bool
    ALGORITHM: str
    SEED: int
```

### `Player`

La clase Player guarda tanto su posición actual en el laberinto como el camino que ha recorrido desde la casilla de inicio hasta la celda en la que actualmente se encuentra. Se usa para encontrar el camino más corto entre la casilla de entrada y la de salida.

```Python
class Player:

    x: int
    y: int
    movements: list[str]
```

`x` = la posicion x del player en el laberinto.  
`y` = la posicion y del player en el laberinto.  
`movements` = la lista de movimientos realizados por el player hasta el momento.  

### `Cell`

La clase Cell sirve para guardar los muros de cada celda, a parte de tener algunos parámetros para la implementación del programa.

```Python
class Cell:
    visited: bool
    block_42: bool
    routed: bool
    weight: int
    N: int
    S: int
    E: int
    W: int
```

`visited` = un booleano que se utiliza para la generación del laberinto.  
`block_42` = un booleano para saber si la celda pertenece al 42 que hay que incrustar en el laberinto.  
`routed` = un booleano que se utiliza para aplicar el algoritmo flood fill.  
`weight` = un número entero con la distancia hasta la casilla de salida que se utiliza en el algoritmo flood fill.  
`N` = va a tener valor 1 o 0, dependiendo de si hay muro en la dirección norte o no.  
`S` = va a tener valor 1 o 0, dependiendo de si hay muro en la dirección sur o no.  
`E` = va a tener valor 1 o 0, dependiendo de si hay muro en la dirección este o no.  
`W` = va a tener valor 1 o 0, dependiendo de si hay muro en la dirección oeste o no.  

### Reutilización del código

## Ejecución del programa

# Algoritmos empleados para la generación del laberinto

# Contribuciones

# Recursos