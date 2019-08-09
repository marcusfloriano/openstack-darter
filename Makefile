# Minimal makefile for Sphinx documentation
#

RED=\033[0;31m
BLUE=\033[0;34m
LBLUE=\033[1;34m
LGRAY=\033[0;37m
NC=\033[0m

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = openstack-darter
SOURCEDIR     = docs
BUILDDIR      = docs/_build

# Put it first so that "make" without argument is like "make help".
help:
	@printf "\n"
	@printf "${LGRAY}Darter (openstack-darter) Help${NC}\n"
	@printf "\n"
	@printf "  ${LBLUE}dochelp${NC}     to show help for documentation\n"
	@printf "  ${LBLUE}servedoc${NC}    to create simple server for show documentations\n"
	@printf "  ${LBLUE}worker${NC}      to starting the worker for wait jobs for execute\n"
	@printf "  ${LBLUE}rqdash${NC}      to starting the dashboard for Redis Queue (RQ)\n"
	@printf "\n"

dochelp:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

servedoc:
	cd docs/_build/html && python3 -m http.server 9000

gendoc:
	make copydoc
	make html

copydoc:
	sphinx-apidoc -f -o docs src

worker:
	rq worker -c settings -v

rqdash:
	rq-dashboard

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)



