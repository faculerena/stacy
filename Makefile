# Makefile for setting up a Python 3 virtual environment and installing packages

# Paths to install (replace with actual paths)
PATH1 = stacks_analyzer/tree-sitter-clarity
PATH2 = stacks_analyzer

.PHONY: venv fish bash ps1 csh install

venv:
	python3 -m venv venv

install: venv
	@echo "Installing tree-sitter grammar for Clarity"
	./venv/bin/pip install $(PATH1)
	@echo "Installing Stacy for Clarity"
	./venv/bin/pip install $(PATH2)

fish: venv
	@echo "Using Fish shell"
	. venv/bin/activate.fish && make install

bash: venv
	@echo "Using Bash shell"
	. venv/bin/activate && make install

ps1: venv
	@echo "Using PowerShell"
	venv\Scripts\Activate.ps1; make install

csh: venv
	@echo "Using C shell"
	. venv/bin/activate.csh && make install
