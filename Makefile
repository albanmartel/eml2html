# Copyright (C) 2022 Centre National de la Recherche Scientifique
# Copyright (C) 2022 Institut Mines Télécom Albi-Carmaux
# Copyright (C) 2022 |Méso|Star> (contact@meso-star.com)
# Copyright (C) 2022 Université Clermont Auvergne
# Copyright (C) 2022 Université de Lorraine
# Copyright (C) 2022 Université de Lyon
# Copyright (C) 2022 Université de Toulouse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

.POSIX:
.SUFFIXES:
SHELL := /bin/bash

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

PREFIX=/usr/local

TARGET_DIR := "$(PREFIX)/bin/eml2html"
SCRIPTS_PYTHON_DIR := "$(PREFIX)/bin/eml2html/python_scripts"
SCRIPTS_BASH_DIR := "$(PREFIX)/bin/"
REQUIREMENTS := requirements.txt

INPUTS=\
 email2html.py\

SCRIPTS=\
 email2html.sh\

target:
	./install_requirements.sh

install: target
	mkdir -p $(SCRIPTS_PYTHON_DIR)
	cp $(INPUTS) $(SCRIPTS_PYTHON_DIR)
	cp $(SCRIPTS) $(SCRIPTS_BASH_DIR)

uninstall:
	@for f in $(SCRIPTS); do rm -f "$(SCRIPTS_BASH_DIR)/$${f}"; done
	@rm -r "$(TARGET_DIR)";

lint:
	@shellcheck -o all $(INPUTS) $(SCRIPTS)
