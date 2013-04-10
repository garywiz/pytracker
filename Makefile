# Just for convenience

.PHONY: build test install

build: 
	python setup.py build

test:
	python setup.py test

install:
	python setup.py install
