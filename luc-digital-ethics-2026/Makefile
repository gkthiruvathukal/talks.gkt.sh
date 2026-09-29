MAIN      := talk
BUILDDIR  := build
LATEXMK   := latexmk
LATEXOPTS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(BUILDDIR)
VENV      := .venv
PYTHON    := $(VENV)/bin/python3

.PHONY: all pdf pptx clean distclean distclean-venv open open-pptx

all: pdf pptx

pdf: $(BUILDDIR)/$(MAIN).pdf

$(BUILDDIR)/$(MAIN).pdf: $(MAIN).tex
	@mkdir -p $(BUILDDIR)
	$(LATEXMK) $(LATEXOPTS) $(MAIN).tex

pptx: $(BUILDDIR)/$(MAIN).pptx

$(BUILDDIR)/$(MAIN).pptx: build_pptx.py $(wildcard images/*) | $(VENV)/.deps-installed
	@mkdir -p $(BUILDDIR)
	$(PYTHON) build_pptx.py

# Bootstrap a local venv with python-pptx/Pillow so `make pptx` works
# without touching the system Python.
$(VENV)/.deps-installed:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip -q
	$(VENV)/bin/pip install python-pptx pillow -q
	touch $@

# Remove latexmk's auxiliary files but keep the built PDF/PPTX.
clean:
	$(LATEXMK) -c -output-directory=$(BUILDDIR) $(MAIN).tex

# Remove the whole build directory, PDF and PPTX included.
distclean:
	rm -rf $(BUILDDIR)

# Also remove the bootstrapped venv.
distclean-venv: distclean
	rm -rf $(VENV)

open: pdf
	open $(BUILDDIR)/$(MAIN).pdf

open-pptx: pptx
	open $(BUILDDIR)/$(MAIN).pptx
