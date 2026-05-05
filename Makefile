MAP=MazeProgram/config.txt
DEBUGGER= -m pdb

VIRTUALENV= MazeEnv
PYTHON=$(VIRTUALENV)/bin/python3
PIP=$(VIRTUALENV)/bin/pip

MINILIBX=mlx_CLXV
MLX=$(VIRTUALENV)/lib/python3.13/site-packages/mlx
DEPENDENCIES=MazeProgram/requirements.txt

MAIN=MazeProgram/a_maze_ing.py

TOCLEAN=.mypy_cache

MYPYFLAGS=--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all: install run

install:
	$(PIP) install -r $(DEPENDENCIES)

$(MLX): install
	$(MAKE) -C $(MINILIBX)

run: $(VIRTUALENV)
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(PYTHON) $(DEBUGGER) $(MAIN)

$(VIRTUALENV):
	python3 -m venv $(VIRTUALENV)


clean:
	py3clean .
	rm -rf $(TOCLEAN)

lint:
	flake8 MazeProgram
	mypy MazeProgram  $(MYPYFLAGS)

lint-strict:
	flake8 MazeProgram
	mypy MazeProgram --strict

SILENT: all install run debug env clean lint lint-strict