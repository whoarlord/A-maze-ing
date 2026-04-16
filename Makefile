PIP=pip install
DEPENDENCIES= requirements.txt
MAP=config.txt

PYTHON=python3
DEBUGGER= -m pdb

MAIN=a-maze-ing.py

TOCLEAN=.mypy_cache

MYPYFLAGS=--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all: install run

install:
	$(PIP) -r $(DEPENDENCIES)

run:
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(PYTHON) $(DEBUGGER) $(MAIN)

clean:
	py3clean .
	rm -rf $(TOCLEAN)

lint:
	flake8 .
	mypy .  $(MYPYFLAGS)

lint-strict:
	flake8 .
	mypy . --strict