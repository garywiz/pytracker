# Just for convenience

.PHONY: build test install clean

build: 
	python setup.py build

test:
	python setup.py test

install:
	python setup.py install

clean:
	python setup.py clean
