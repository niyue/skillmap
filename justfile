dev:
	find skillmap -iname "*.py" -o -iname "*.cmake" -iname "pyproject.toml" | entr -s "poetry build && pip install ./dist/skillmap-*-any.whl --force-reinstall --no-dependencies"

setup:
	# install the library into system python
	rm -fr ./dist
	poetry build && pip install ./dist/skillmap-*-py3-none-any.whl --force-reinstall

build_sample src="tests/url_shortener.toml" dest="dist/url_shortener.md":
  echo '```mermaid' > {{ dest }} && skillmap {{ src }} >> {{ dest }} && echo '```' >> {{ dest }}

dev_sample src="tests":
  find {{ src }} -iname "*.toml" | entr -s "just build_sample"