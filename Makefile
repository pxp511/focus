lint:
	python3 -m yapf -ir . -vv

clean:
	rm -rf build dist *.egg-info __pycache__ focus/__pycache__

package: clean
	python3 setup.py bdist_wheel

uninstall:
	echo y | python3 -m pip uninstall focus-xp

package_install: package
	python3 -m pip install dist/*.whl -U

upload: package
	python3 -m twine upload dist/*

download:
	python3 -m pip install focus-xp -U

debug: clean uninstall package_install

focus_run:
	python3 -m focus --repository ~/mesh-label