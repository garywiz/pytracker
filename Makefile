# Just for convenience

.PHONY: build test install clean

# Build locally
build: 
	python setup.py build

# Build and test locally
test:
	python setup.py test

# Build test and install locally
install:
	python setup.py install

# Create a source distribution for double-checking contents
dist:
	python setup.py sdist

# Update meta-data details on pypi
update:
	python setup.py register

# Upload this release to pypi
upload:
	python setup.py sdist upload

# Cleanup everything
clean:
	python setup.py clean
	test -e build && rm -rf build; true
	test -e dist && rm -rf dist; true
	test -e pytracker.egg-info && rm -rf pytracker.egg-info; true
	test -e pytracker/trackable.so && rm pytracker/trackable.so; true
	cd doc; make clean
