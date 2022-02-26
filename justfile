dev:
	find skillmap -iname "*.py" -o -iname "*.cmake" -iname "pyproject.toml" | entr -s "poetry build && pip install ./dist/skillmap-*-any.whl --force-reinstall --no-dependencies"

setup:
	# install the library into system python
	rm -fr ./dist
	poetry build && pip install ./dist/skillmap-*-py3-none-any.whl --force-reinstall
