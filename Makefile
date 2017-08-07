project := scarlett_os
projects := scarlett_os
username := bossjones
container_name := scarlett_os

# label-schema spec: http://label-schema.org/rc1/

CONTAINER_VERSION  = $(shell \cat ./VERSION | awk '{print $1}')
GIT_BRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
GIT_SHA     = $(shell git rev-parse HEAD)
BUILD_DATE  = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

# NOTE: DEFAULT_GOAL
# source: (GNU Make - Other Special Variables) https://www.gnu.org/software/make/manual/html_node/Special-Variables.html
# Sets the default goal to be used if no
# targets were specified on the command
# line (see Arguments to Specify the Goals).
# The .DEFAULT_GOAL variable allows you to
# discover the current default goal,
# restart the default goal selection
# algorithm by clearing its value,
# or to explicitly set the default goal.
# The following example illustrates these cases:
.DEFAULT_GOAL := help

flake8 := flake8
COV_DIRS := $(projects:%=--cov %)
# [-s] per-test capturing method: one of fd|sys|no. shortcut for --capture=no.
# [--tb short] traceback print mode (auto/long/short/line/native/no).
# [--cov-config=path]     config file for coverage, default: .coveragerc
# [--cov=[path]] coverage reporting with distributed testing support. measure coverage for filesystem path (multi-allowed)
pytest_args := -s --tb short --cov-config .coveragerc $(COV_DIRS) tests
pytest := py.test $(pytest_args)
sources := $(shell find $(projects) tests -name '*.py' | grep -v version.py | grep -v thrift_gen)

test_args_no_xml := --cov-report=
test_args := --cov-report term-missing --cov-report xml --junitxml junit.xml
cover_args := --cov-report html

.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


define ASCILOGO
  ██████  ▄████▄   ▄▄▄       ██▀███   ██▓    ▓█████▄▄▄█████▓▄▄▄█████▓    ███▄ ▄███▓ ▄▄▄       ██ ▄█▀▓█████
▒██    ▒ ▒██▀ ▀█  ▒████▄    ▓██ ▒ ██▒▓██▒    ▓█   ▀▓  ██▒ ▓▒▓  ██▒ ▓▒   ▓██▒▀█▀ ██▒▒████▄     ██▄█▒ ▓█   ▀
░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██ ░▄█ ▒▒██░    ▒███  ▒ ▓██░ ▒░▒ ▓██░ ▒░   ▓██    ▓██░▒██  ▀█▄  ▓███▄░ ▒███
  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██▀▀█▄  ▒██░    ▒▓█  ▄░ ▓██▓ ░ ░ ▓██▓ ░    ▒██    ▒██ ░██▄▄▄▄██ ▓██ █▄ ▒▓█  ▄
▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒░██▓ ▒██▒░██████▒░▒████▒ ▒██▒ ░   ▒██▒ ░    ▒██▒   ░██▒ ▓█   ▓██▒▒██▒ █▄░▒████▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░▓  ░░░ ▒░ ░ ▒ ░░     ▒ ░░      ░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▒ ▓▒░░ ▒░ ░
░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░  ░▒ ░ ▒░░ ░ ▒  ░ ░ ░  ░   ░        ░       ░  ░      ░  ▒   ▒▒ ░░ ░▒ ▒░ ░ ░  ░
░  ░  ░  ░          ░   ▒     ░░   ░   ░ ░      ░    ░        ░         ░      ░     ░   ▒   ░ ░░ ░    ░
      ░  ░ ░            ░  ░   ░         ░  ░   ░  ░                           ░         ░  ░░  ░      ░  ░
         ░
=======================================
endef

export ASCILOGO

# http://misc.flogisoft.com/bash/tip_colors_and_formatting

RED=\033[0;31m
GREEN=\033[0;32m
ORNG=\033[38;5;214m
BLUE=\033[38;5;81m
NC=\033[0m

export RED
export GREEN
export NC
export ORNG
export BLUE

# verify that certain variables have been defined off the bat
check_defined = \
    $(foreach 1,$1,$(__check_defined))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $(value 2), ($(strip $2)))))

list_allowed_args := name

help:
	@printf "\033[1m$$ASCILOGO $$NC\n"
	@printf "\033[21m\n\n"
	@printf "=======================================\n"
	@printf "\n"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

list:
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sort

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: bootstrap
bootstrap:
	# [ "$$VIRTUAL_ENV" != "" ]
	rm -rf *.egg-info || true
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
	python setup.py install
	pip install -e .[test]

.PHONY: bootstrap-experimental
bootstrap-experimental:
	pip install -r requirements_test_experimental.txt

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

docker-build:
	docker-compose -f docker-compose.yml -f ci/build.yml build

docker-build-run: docker-build
	docker run -i -t --rm scarlettos_scarlett_master bash

lint: ## check style with flake8
	flake8 scarlett_os tests

pytest-install-test-deps: clean
	pip install -e .[test]
	python setup.py install

pytest-run:
	py.test
	# py.test -v --timeout=30 --duration=10 --cov --cov-report=

jhbuild-run-test:
	jhbuild run python setup.py install
	jhbuild run -- pip install -e .[test]
	jhbuild run -- coverage run -- setup.py test
	jhbuild run -- coverage report -m

test: ## run tests quickly with the default Python
	python setup.py test

test-clean-all: ## run tests on every Python version with tox
	pip install -e .[test]
	python setup.py install
	coverage run setup.py test

test-with-pdb:
	# pytest -p no:timeout -k test_mpris_player_and_tasker
	pytest -p no:timeout -k test_mpris_player_and_tasker

test-docker:
	sudo chown -R vagrant:vagrant *
	grep -q -F 'privileged: true' docker-compose.yml || sed -i "/build: ./a \ \ privileged: true" docker-compose.yml
	docker-compose -f docker-compose.yml -f ci/build.yml build
	docker run --privileged -v `pwd`:/home/pi/dev/bossjones-github/scarlett_os -i -t --rm scarlettos_scarlett_master make test-travis
	sudo chown -R vagrant:vagrant *

.PHONY: test-perf
test-perf:
	$(pytest) $(test_args) --benchmark-only

.PHONY: jenkins
jenkins: bootstrap
	$(pytest) $(test_args) --benchmark-skip

.PHONY: test-travis
test-travis: export TRAVIS_CI=1
test-travis:
	$(pytest) $(test_args_no_xml) --benchmark-skip
	coverage report -m

.PHONY: test-travis-scarlettonly
test-travis-scarlettonly: export TRAVIS_CI=1
test-travis-scarlettonly:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonly
	coverage report -m

.PHONY: test-travis-scarlettonlyintgr
test-travis-scarlettonlyintgr: export TRAVIS_CI=1
test-travis-scarlettonlyintgr:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonlyintgr
	coverage report -m

.PHONY: test-travis-scarlettonlyintgr-no-timeout
test-travis-scarlettonlyintgr-no-timeout: export TRAVIS_CI=1
test-travis-scarlettonlyintgr-no-timeout:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonlyintgr -p no:timeout
	coverage report -m

.PHONY: test-travis-scarlettonlyunittest
test-travis-scarlettonlyunittest: export TRAVIS_CI=1
test-travis-scarlettonlyunittest:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m scarlettonlyunittest
	coverage report -m

.PHONY: test-travis-unittest
test-travis-unittest: export TRAVIS_CI=1
test-travis-unittest:
	$(pytest) $(test_args_no_xml) --benchmark-skip -m unittest
	coverage report -m

.PHONY: test-travis-debug
test-travis-debug:
	$(pytest) $(test_args_no_xml) --benchmark-skip --pdb --showlocals
	coverage report -m

.PHONY: test-travis-leaks
test-travis-leaks: export TRAVIS_CI=1
test-travis-leaks:
	$(pytest) $(test_args_no_xml) --benchmark-skip -R :
	coverage report -m

.PHONY: cover
cover:
	$(pytest) $(cover_args) --benchmark-skip
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: cover-travisci
cover-travisci: export TRAVIS_CI=1
cover-travisci: display-env
	# $(pytest) $(cover_args) --benchmark-skip -p no:ipdb
	pytest -p no:ipdb -p no:pytestipdb -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --showlocals --trace-config
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: cover-debug
cover-debug:
	# --showlocals # show local variables in tracebacks
	$(pytest) $(cover_args) --benchmark-skip --pdb --showlocals
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: cover-debug-no-timeout
cover-debug-no-timeout:
	pytest -p no:timeout -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: display-env
display-env:
	@printf "=======================================\n"
	@printf "$$GREEN TRAVIS_CI:$$NC             $(TRAVIS_CI) \n"
	@printf "=======================================\n"

# This task simulates a travis environment
.PHONY: cover-debug-no-timeout-travisci
cover-debug-no-timeout-travisci: export TRAVIS_CI=1
cover-debug-no-timeout-travisci: display-env
	pytest -p no:timeout -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

.PHONY: shell
shell:
	ipython

coverage: ## check code coverage quickly with the default Python
		# coverage run --source scarlett_os setup.py test
		coverage run --source=scarlett_os/ setup.py test
		# defined inside of setup.cfg:
		# --cov=scarlett_os --cov-report term-missing tests/
		# coverage run --source=scarlett_os/ --include=scarlett_os setup.py test
		coverage report -m
		coverage html
		$(BROWSER) htmlcov/index.html

coverage-no-html: ## check code coverage quickly with the default Python

	coverage run --source scarlett_os setup.py test

	coverage report -m

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/scarlett_os.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ scarlett_os
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

dc-ci-build:
	docker-compose -f docker-compose.yml -f ci/build.yml build

docker-run-bash:
	docker run -i -t --rm scarlettos_scarlett_master bash

# docker-exec-bash:
# 	container_id := $(shell docker ps |grep scarlettos_scarlett_master| awk '{print $1}')
# 	docker exec -i it $(container_id) bash

install: clean ## install the package to the active Python's site-packages
	python setup.py install

install-all:
	pip install -r requirements.txt
	python setup.py install
	pip install -e .[test]

setup-venv:
	mkvirtualenv --python=/usr/local/bin/python3 scarlett-os-venv

install-travis-lint:
	bundle install --path .vendor

run-travis-lint:
	bundle exec travis lint

install-gi-osx:
	brew reinstall pygobject3 --with-python3

isort:
	python setup.py isort

dbus-monitor-signal:
	dbus-monitor "type='signal'"

dbus-monitor-all:
	dbus-monitor

run-mpris:
	python -m scarlett_os.mpris

run-tasker:
	python -m scarlett_os.tasker

run-listener:
	python -m scarlett_os.listener

# source: https://github.com/docker/machine/blob/master/docs/drivers/generic.md#interaction-with-ssh-agents
# source: http://blog.scottlowe.org/2015/08/04/using-vagrant-docker-machine-together/
create-docker-machine:
	docker-machine create -d generic \
						  --generic-ssh-user pi \
						  --generic-ssh-key /Users/malcolm/dev/bossjones/scarlett_os/keys/vagrant_id_rsa \
						  --generic-ssh-port 2222 \
						  --generic-ip-address 127.0.0.1 \
						  --engine-install-url "https://test.docker.com" \
						  scarlett-1604-packer
	eval $(docker-machine env scarlett-1604-packer)

docker-compose-build:
	@docker-compose -f docker-compose-devtools.yml build

docker-compose-build-master:
	@docker-compose -f docker-compose-devtools.yml build master

docker-compose-run-master:
	@docker-compose -f docker-compose-devtools.yml run --name scarlett_master --rm master bash

docker-compose-run-test:
	@docker-compose -f docker-compose-devtools.yml run --name scarlett_test --rm test bash python3 --version

docker-compose-up:
	@docker-compose -f docker-compose-devtools.yml up -d

docker-compose-up-build:
	@docker-compose -f docker-compose-devtools.yml up --build

docker-compose-up-build-d:
	@docker-compose -f docker-compose-devtools.yml up -d --build

docker-compose-down:
	@docker-compose -f docker-compose-devtools.yml down

docker-version:
	@docker --version
	@docker-compose --version

docker-exec:
	@scripts/docker/exec-master

docker-exec-master:
	@scripts/docker/exec-master

format:
	$(call check_defined, name, Please set name)
	yapf -i $(product).py || (exit 1)

convert-markdown-to-rst:
	pandoc --from=markdown_github --to=rst --output=README.rst README.md

install-pandoc-stuff:
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip3 install sphinx sphinx-autobuild restructuredtext-lint

.PHONY: docker-clean
docker-clean:
	docker rm $(docker ps -a -q); docker rmi $(docker images | grep "^<none>" | awk '{print $3}');

# Start here
.PHONY: docker_build_dev
docker_build_dev:
	set -x ;\
	mkdir -p wheelhouse; \
	docker build \
	    --build-arg CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    --build-arg GIT_BRANCH=$(GIT_BRANCH) \
	    --build-arg GIT_SHA=$(GIT_SHA) \
	    --build-arg BUILD_DATE=$(BUILD_DATE) \
	    --build-arg SCARLETT_ENABLE_SSHD=0 \
	    --build-arg SCARLETT_ENABLE_DBUS='true' \
	    --build-arg SCARLETT_BUILD_GNOME='false' \
	    --build-arg TRAVIS_CI='true' \
	    --build-arg STOP_AFTER_GOSS_JHBUILD='false' \
	    --build-arg STOP_AFTER_GOSS_GTK_DEPS='false' \
		--build-arg SKIP_TRAVIS_CI_PYTEST='false' \
		--build-arg STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		--file=Dockerfile \
		--tag $(username)/$(container_name):$(GIT_SHA) . ; \
	docker tag $(username)/$(container_name):$(GIT_SHA) $(username)/$(container_name):dev

.PHONY: docker_run_dev
docker_run_dev:
	set -x ;\
	mkdir -p wheelhouse; \
	docker run -i -t --rm \
		--name scarlett-dev \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD=0 \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='false' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='false' \
		-e SKIP_TRAVIS_CI_PYTEST='true' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		-e TRAVIS_CI_PYTEST='false' \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
		-v $$(pwd)/wheelhouse/:/wheelhouse:rw \
	    $(username)/$(container_name):dev /bin/bash

.PHONY: docker_run_wheelhouse
docker_run_wheelhouse:
	set -x ;\
	mkdir -p wheelhouse; \
	docker run -i -t --rm \
		--name scarlett-dev \
	    -e CONTAINER_VERSION=$(CONTAINER_VERSION) \
	    -e GIT_BRANCH=$(GIT_BRANCH) \
	    -e GIT_SHA=$(GIT_SHA) \
	    -e BUILD_DATE=$(BUILD_DATE) \
	    -e SCARLETT_ENABLE_SSHD=0 \
	    -e SCARLETT_ENABLE_DBUS='true' \
	    -e SCARLETT_BUILD_GNOME='false' \
	    -e TRAVIS_CI='true' \
	    -e STOP_AFTER_GOSS_JHBUILD='false' \
	    -e STOP_AFTER_GOSS_GTK_DEPS='false' \
	    -e SKIP_GOSS_TESTS_JHBUILD='false' \
	    -e SKIP_GOSS_TESTS_GTK_DEPS='false' \
		-e SKIP_TRAVIS_CI_PYTEST='true' \
		-e STOP_AFTER_TRAVIS_CI_PYTEST='false' \
		-e TRAVIS_CI_PYTEST='false' \
		-v $$(pwd)/:/home/pi/dev/bossjones-github/scarlett_os:rw \
		-v $$(pwd)/wheelhouse/:/wheelhouse:rw \
	    $(username)/$(container_name):dev /bin/bash

# ENV TRAVIS_CI_RUN_PYTEST ${TRAVIS_CI_RUN_PYTEST:-'false'}
# ENV TRAVIS_CI_SKIP_PYTEST ${TRAVIS_CI_SKIP_PYTEST:-'false'}
