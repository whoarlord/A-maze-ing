MAP=config.txt
DEBUGGER= -m pdb

VIRTUALENV= MazeEnv
PYTHON=$(VIRTUALENV)/bin/python3
PIP=$(VIRTUALENV)/bin/pip

MLX=$(VIRTUALENV)/lib/python3.13/site-packages/mlx
DEPENDENCIES=requirements.txt
MAZEVERSION=0.7
MAZEPROGRAM=mazegen-$(MAZEVERSION)-py3-none-any.whl

MAIN=a_maze_ing.py

TOCLEAN=.mypy_cache

MYPYFLAGS=--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all: install run

install:
	$(PIP) install -r $(DEPENDENCIES)

run: $(VIRTUALENV) install
	$(PYTHON) $(MAIN) $(MAP)

debug: $(VIRTUALENV)
	$(PYTHON) $(DEBUGGER) $(MAIN) $(MAP) </dev/tty

$(VIRTUALENV):
	python3 -m venv $(VIRTUALENV)

build: 
	$(PYTHON) -m build
	cp dist/$(MAZEPROGRAM) mazegen_module/

install-module: build
	$(PIP) install mazegen_module/$(MAZEPROGRAM)

clean:
	py3clean .
	rm -rf $(TOCLEAN)

lint:
	flake8 MazeProgram a_maze_ing.py setup.py
	mypy MazeProgram a_maze_ing.py  $(MYPYFLAGS)

lint-strict:
	flake8 MazeProgram a_maze_ing.py setup.py
	mypy MazeProgram a_maze_ing.py --strict --ignore-missing-imports

SILENT: all install run debug build install clean lint lint-strict