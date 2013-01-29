# makefile for zCall by Iain Bancarz, ib5@sanger.ac.uk

PREFIX = 	.
DEST =		$(PREFIX)/zCall
SCRIPTS =	src/scripts
ETC =       src/etc

usage:
	@echo -e "Usage: make install PREFIX=<destination directory>\nWill install to the zCall subdirectory of PREFIX."

install:
	install -d $(DEST) $(DEST)/scripts $(DEST)/etc
	install $(SCRIPTS)/*.py $(SCRIPTS)/*.r $(DEST)/scripts
	install $(ETC)/*.ini $(DEST)/etc
