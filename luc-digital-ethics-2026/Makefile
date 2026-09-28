MAIN      := talk
BUILDDIR  := build
LATEXMK   := latexmk
LATEXOPTS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(BUILDDIR)
PYTHON    := python3

.PHONY: all pdf pptx clean distclean open open-pptx

all: pdf pptx

pdf: $(BUILDDIR)/$(MAIN).pdf

$(BUILDDIR)/$(MAIN).pdf: $(MAIN).tex
	@mkdir -p $(BUILDDIR)
	$(LATEXMK) $(LATEXOPTS) $(MAIN).tex

pptx: $(BUILDDIR)/$(MAIN).pptx

$(BUILDDIR)/$(MAIN).pptx: build_pptx.py $(wildcard images/*)
	@mkdir -p $(BUILDDIR)
	$(PYTHON) build_pptx.py

# Remove latexmk's auxiliary files but keep the built PDF/PPTX.
clean:
	$(LATEXMK) -c -output-directory=$(BUILDDIR) $(MAIN).tex

# Remove the whole build directory, PDF and PPTX included.
distclean:
	rm -rf $(BUILDDIR)

open: pdf
	open $(BUILDDIR)/$(MAIN).pdf

open-pptx: pptx
	open $(BUILDDIR)/$(MAIN).pptx
