*Este proyecto ha sido creado como parte del currículo de 42 por iarrien- y aeiros-t*

# A-maze-ing — Proyecto 42

El objetivo de este proyecto es implementar un generador de laberintos en Python que reciba un archivo de configuración, genere un laberinto, posiblemente perfecto(con un único camino entre la entrada(entry) y la salida(exit)), y escriba dicho laberinto a un archivo usando hexadecimales para representar muros. También se deberá proveer una reprentación visual del laberinto generdo.

---

## Índice

1. [Descripción](#descripción)  
1.1. [Descripción General](#descripción-general)
2. [Instrucciones](#instrucciones)  
2.1. [Ejecución del Programa](#ejecución-del-programa)  
2.2. [Estructura del Proyecto](#estructura-del-proyecto)  
2.2.1 [Reutilización del código](#reutilización-del-código)  
3. [Algoritmos empleados para la generación del laberinto](#algoritmos-empleados-para-la-generación-del-laberinto)  
4. [Contribuciones](#contribuciones)   
4.1. [Roles del equipo](#roles-del-equipo)  
4.2. [Planificación del proyecto](#planificación-del-proyecto)  
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

Una vez generado el laberinto, éste se debe escribir en un archivo de salida, usando un digito hexadecimal para representar cada celda. El hexadecimal representa los muros basado en la siguiente tabla:


| Bit | Dirección |
|----------|-------------|
| **0**(LSB) | Norte |
| **1** | Este |
| **2** | Sur |
| **3** | Oeste |

Si hay un muro, se representa con un 1, y si no hay muro se representa con 0.  
Ejemplos: 
 - 3 (binario 0011) significa que hay muros al **Norte** y al **Este**.  
 - A(binario 1010) significa que hay muros al **Este** y al **Oeste**.

Las celdas se escriben fila a fila, escribiendo una fila en cada linea. Al terminar de escribir el laberinto, se ha de dejar un salto de linea y después se han de insertar tres datos, uno en cada linea: punto de entrada al laberinto, punto de salida del laberinto y el camino valido más corto desde la entrada hasta la salida.

Siguiendo el ejemplo del config.txt descrito antes, a continuación se muestra un ejemplo de un output de salida(maze.txt en el ejemplo de arriba):

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

## Ejecución del programa

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
`W` = como lo supiste, va a tener valor 1 o 0, dependiendo de si hay muro en la dirección oeste o no.  


### `Maze`

La clase Maze sirve para representar el laberinto, así como ciertos atributos asociados para la ejecución del programa.

```Python
class Maze:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    animation: boolean
    algorithm: str
    seed: int
    maze_map: list[list[Cell]]
```

`width` = la anchura del laberinto, recibida desde el archivo config.txt.  
`height` = la altura del laberinto, recibida desde el archivo config.txt.  
`entry` = el punto de entrada del laberinto, recibido desde el archivo config.txt. Partiremos desde este punto para encontrar la solución.  
`exit` = el punto de salida del laberinto, recibido desde el archivo config.txt. Este será el destino para encontrar la solución.  
`output_file` = el nombre o la ruta del archivo de salida que se va a generar, recibido desde el archivo config.txt.  
`perfect` = un booleano que dictamina si el laberinto es perfecto(tiene una única solución) o no, recibido desde el archivo config.txt.  
`animation` = un booleano que indica si se debe mostrar animación al generar el laberinto o no, recibido desde el archivo config.txt.  
`algorithm` = el algoritmo específico que se va a utilizar para la generación del laberinto. Si no se especifica en el config.txt, por defecto se usa el Prim.  
`seed` = la semilla para generar el laberinto.  
`maze_map` = la matriz con la representación del laberinto.  

### `Graphics`

La clase Graphics sirve para crear la representación gráfica del laberinto.

```Python
class Graphics:
    m: Mlx
    mlx_ptr: void puntero de una libreria de c
    win_height: int
    win_width: int
    win_ptr: void puntero de una libreria de c
    maze_img_ptr: void puntero de una libreria de c
    maze_buffer: tuple[memoryview[int], int, int, int]
    route_img_ptr: void puntero de una libreria de c
    route_buffer: tuple[memoryview[int], int, int, int]
    wall_multiplier: int
    colors: deque[dict[int]]
```

`m` = la clase principal de la minilibx.  
`mlx_ptr` = un puntero a la mlx.  
`win_heighty` = la anchura de la ventana gráfica basada en el monitor.  
`win_width` = la altura de la ventana gráfica basada en el monitor.  
`win_ptr` = un puntero a la ventana gráfica que vamos a mostrar.  
`maze_img_ptr` = un puntero a la imagen que contiene el laberinto creado.  
`maze_buffer` = el buffer de la imagen del laberinto.  
`route_img_ptr` = un puntero a la imagen que contiene la ruta desde el punto de entrada hasta el punto de salida.  
`route_buffer` = el buffer de la imagen de la ruta.  
`wall_multiplier` = un valor para aumentar la anchura de los muros en la imagen.  
`colors` = los diferentes colores del laberinto.  

### `Algorithms`

La clase Algorithms es una clase que representa el objeto para la creación del laberinto. Como tal, esta clase no tiene ningún atributo, solo metodos. Los más importantes son los siguientes:

```Python
class Algorithms:
    create_map(self, maze: Maze) -> None:
    create_seed(self, maze: Maze) -> None:
    create_map_kruskal(self, maze: Maze) -> None:
    create_map_prim(self, maze: Maze) -> None:
```

`create_map` = este método crea una semilla o utiliza la del config.txt si hay alguna y crea un laberinto basando en el algoritmo especificado en el atributo algorithm de la clase Maze.  
`create_seed` = este método crea una semilla aleatoria para el laberinto.  
`create_map_kruskal` = este método crea un laberinto utilizando el algoritmo kruskal, el cual se explicará más adelante.  
`create_map_prim` = este método crea un laberinto utilizando el algoritmo prim, el cual se explicará más adelante.  

### Reutilización del código

# Algoritmos empleados para la generación del laberinto

# Contribuciones

## Roles del equipo

El rol principal de Iker durante este proyecto ha sido el de graphic designer(creador de la rumba). Se ha encargado sobretodo de la integración de la minilib(🫡). También se ha encargado de la implementación de los algoritmos de creación del laberinto.

El rol prinicpal de Ander durante este proyecto ha sido el de software engeneer(creador del pos=0). Se ha encargado principalmente de la implementación del algoritmo flood fill, lo cual puede no parecer demasiado mirando el código, ya que más de la mitad del trabajo se fué a la basura por querer complicar las cosas de más(facilmente 30 horas de trabajo tiradas 😭).

## Planificación del proyecto

Para la planificación del proyecto nos basamos en la metodología Agile. Planificamos 4 sprints, de una semana cada uno. En el primer sprint, identificamos y dividimos las tareas principales del proyecto. Una vez divididas las tareas, cada miembro del equipo se dispuso a buscar la información pertoinente.

En el segundo sprint, lo primero que hicimos fue una reunión para compartir la información recabada y terminar de decidir los últimos detalles sobre el reparto de tareas. Después de ello, el objetivo de este sprint fué tener listo el parseo de los datos de entrada y la generación del laberinto, de momento independientes uno del otro.

En el tercer sprint, lo primero que hicimos fue juntar el parseo de los datos de entrada con la generación del laberinto creados en el sprint anterior. Una vez hecho, el objetivo de este sprint fue generar la interfaz para la representación gráfica del laberinto e implementar el algoritmo para la resolución del laberinto.

En el cuarto y último sprint, lo primero que hicimos fue una reunión para comprobar el estado del proyecto. Una vez aclarado el estado del proyecto y las tareas pendientes, el objetivo de este sprint fue limpiar y pulir el código, así como crear la documentación del proyecto.

En la siguiente tabla se puede ver como se desarrolló la planificación:


| Sprint | Objetivo | Se cumplió el objetivo | Razón por la que no |
|:----------:|:----------:|:----------:|:----------:|
| **1** | División de tareas y busqueda de información | Si | - |
| **2** | Crear el parseo de los datos de entrada y la generación del laberinto | Si | - |
| **3** | Generar la interfaz gráfica e implementar el algoritmo para la resolución del laberinto | No | Sobrecomplicación al querer hacer la implementación de la solución |
| **4** | Pulir y limpiar el código y crear la documentación | No | Los retrasos acarreados del sprint anterior y motivos personales |

Como se puede ver en la tabla, a partir del tercer sprint hubo problemas que provocaron retrasos en el proyecto. Por un lado, quisimos implementar la resolución del algoritmo utilizando la idea de un robot que se encuentra en un laberinto y tiene que buscar la salida, identificando y actualizando los muros según los iba encontrando. Conseguimos implementarlo para los laberintos perfectos pero a la hora de resolver laberintos imperfectos hubo demasiados problemas y al final decidimos simplificar la solución.

Por otro lado, por motivos personales de uno de los miembros del grupo, el sprint 4 se tuvo que posponer durante una semana, ya que este miembro no iba a poder trabajar en el proyecto durante ese tiempo.

Otro fallo en la planificación fue el dejar la limpieza de codigo y la documentación para el final, ya que hubo que resolver algunos conflictos y refactorizar bastante código el cual se podría haber ahorrado si se hubiera hecho al momento.

Debido a estos problemas, hubo que añadir un sprint más entre el tercero y el cuarto, para terminar con la implementación de la solución y empezar con la limpieza del código.

# Recursos

- **Rayan Bouhal and Niko Paraskevopoulos** — *Maze Solving using Flood Fill Algorithm*.  
- **Oscar Gonzalez** — *Cómo construir un robot micromouse que resuelve un laberinto* 
- **Microsiervos** — *Un algoritmo para crear laberintos «interesantes»*
- **Universitat Politècnica de València** — *algoritmo de Kruskal*
- **Claude, Copilot y ChatGPT** — *Conceptos clave. Edición del README.*  