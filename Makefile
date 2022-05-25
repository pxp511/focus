lint:
	python3 -m yapf -ir . -vv

clean:
	rm -rf build dist *.egg-info __pycache__ focus/__pycache__

package: clean
	python3 setup.py bdist_wheel

uninstall:
	echo y | python3 -m pip uninstall focus-xp

install: package uninstall
	python3 -m pip install dist/*.whl -U

upload: package
	python3 -m twine upload dist/*

download:
	python3 -m pip install focus-xp -U