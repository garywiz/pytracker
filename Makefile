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
	test -e build && rm -rf build; true
	test -e pytracker.egg-info && rm -rf pytracker.egg-info; true
	test -e pytracker/trackable.so && rm pytracker/trackable.so; true

