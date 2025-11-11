# Makefile
PYTHON := python3
PY_SCRIPT := flexiblecalendar.py
CONFIG := config.toml
PDFLATEX := lualatex
TEX := main.tex
RM := rm -rf

.PHONY: all latex pdf clean

all: clean latex pdf

latex:
	$(PYTHON) $(PY_SCRIPT) $(CONFIG)

pdf:
	$(PDFLATEX) -output-directory=output $(TEX)

clean:
	$(RM) ./output/tables/*
	$(RM) ./output/months/*
	$(RM) ./output/config/*
	$(RM) ./output/main.*
