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