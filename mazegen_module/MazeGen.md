*Pequeña documentacion acerca de el modulo MazeGen para generar los laberintos*

# MazeGen

Para poder instanciar el generador tenemos que importar el modulo MazeGen, y con el las clases concretas del Parser y el Maze

```Python
from MazeGen import Parser, Maze
```

La clase Parser nos sirve para poder leer de un archivo con la funcion parse_line() la cual recibe las lineas de un fichero y genera un diccionario con los atributos que desea recibir el Maze. Ademas de parse_line(line, dictionary) tiene una funcion para checkear si los atributos obligatorios han sido insertados correctamente que es entry_checker(dictionary), y una ultima para generar el diccionario con el que poder generar directamente el laberinto

```txt
#Obligatorios
WIDTH=25
HEIGHT=25
ENTRY=0,0
EXIT=24,24
OUTPUT_FILE=maze.txt
PERFECT=True
#Opcionales
DISPLAY_MODE=Normal
ALGORITHM=prim
```

```Python
Parser.parse_line(line, dictionary)
Parser.entry_checker(dictionary)
dictionary_output = parser.complete_dictionary(dictionary)
maze = Maze(**dictionary_output)
```

Una vez que tenemos la estructura inicializada solo tenemos que llamar a la funcion create_maze(maze) de la clase Algorithms, la cual generara el laberinto basandose en el algoritmo recibido

```Python
from MazeGen import Algorithms

Algorithms.create_maze(maze)
```

Ademas, en caso de querer sacar la solucion mas corta del laberinto, tenemos la funcion solve_maze(maze), la cual recibira el laberinto generara una solucion y la guardara en la clase del laberinto y en el fichero de output proporcionado

```Python
from MazeGen import solve_maze

solve_maze(maze)
```

Por ultimo, en caso de querer verlo de manera grafica, pueden instanciar la clase Graphics la cual se ocupara de generar todo lo necesario

```Python
from MazeGen import Graphics

Graphics(maze)
```

## Ejecución del programa

para poder ejecutar este programa vamos a hacer uso de un Makefile, el cual se ocupara de instalar todas las dependencias y ejecutar el programa desde un entorno virtual que el mismo genera.

Para esto, lo mas basico es ejecutar el comando make o make run, el cual se ocupara de crear el entorno virtual, instalar las dependencias correspondientes sobre el, y ejecutar el archivo a_maze_ing.py

```bash
make run
```

por otro lado tenemos la regla de build, que se ocupa de buildear la carpeta MazeGen, para generar la libreria que luego se puede utilizar fuera del proyecto, y la regla install-module que se ocupa de instalar esta libreria en el environment creada anteriormente (MazeEnv)

```bash
make build
make install-module
```

Ademas de esto tenemos las reglas de clean y debug para limpiar el codigo de carpetas innecesarias de cache y para debugar el codigo con pbd

```bash
make clean
make debug
```

# Algoritmos empleados para la generación del laberinto

Para la generacion de algoritmos perfectos hemos hecho uso de dos algoritmos, el de prim y el de kruskal, los cuales generan laberintos perfectos, y en caso de necesitar un laberinto imperfecto hemos partido de estos dos algoritmos y hemos implementado un BFS (Breadth-first search), para destruir muros en base a un threshold

## Prim

El algoritmo de prim es un algoritmo sencillo que se basa en ir visitando casillas y levantando muros.

Este algoritmo empieza en una casilla cualquiera, en nuestro caso en la casilla de entry; levanta los cuatro muros sobre esta casilla, la marca como visitada y la añade a un stack, lo unico que tiene prohibido este algoritmo es moverse a una casilla que este puesta como visitada.

Una vez que tenemos este estado elige una casilla al azar de las diferentes casilla a las que puede moverse que le rodean (las posibles casillas son aquellas que no se salen de las dimensiones del laberinto y no han sido visitados anteiormente), y se mueve a ella poniendola en visited y levantando todos los muros menos el muro de la casilla de la que viene y a su vez destruyendo el muro correspondiente de la casilla anterior. Despues de esto añade la casilla al stack y vuelve a realizar la misma accion descrita en este parrafo.

Esta accion se ejecuta iterativamente hasta que la casilla actual en la que nos encontramos no tiene vecinos que poder visitar, cuando se da ese caso, se hace pop de la ultima posicion metida en el stack (que es la posicion actual), y se vuelve a mirar las casillas adyacentes con la nueva casilla actual, que sera la que ahora sea la ultima casilla en el stack

Este se seguira haciendo hasta que no queden casillas en el stack, y en ese momento habra terminado de generarse el laberinto.

## Kruskal

El algoritmo de kruskal se basa en levantar todos los muros de todas las casillas y establecer un grupo por casilla.

Se considera que dos casillas son de diferente grupo cuando estan separadas por muros

Una vez hecho esto ira rompiendo muros aleatorios de grupos diferentes para juntar grupos los grupos hasta tener un unico grupo

### BFS

Por ultimo, el algoritmo de BFS sirve para romper muros de estos laberintos perfectos y asi generar nuevas rutas hacia la salida.

Para esto, lo primero que hacemos es establecer un threshold, que sera el minimo entre la altura y la anchura del laberinto, y mediante la busqueda en profundidad calcularemos la distancia entre dos celdas, y en caso de que sea mayor que el threshold establecido destruira el muro entre ellos.

El algoritmo hara esto para todas las celdas con todos sus vecinos hasta que ya no le queden celdas