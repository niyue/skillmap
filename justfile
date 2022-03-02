#!/usr/bin/env just --justfile
set dotenv-load := true

sample_toml := "tests/url_shortener.toml"
sample_md := "dist/url_shortener.md"
sample_png := "dist/url_shortener.png"
built_wheel := "./dist/skillmap-*-py3-none-any.whl"

# build and  install package into system python for every python file change
dev:
	find skillmap -iname "*.py" -iname "pyproject.toml" | entr -s "poetry build && pip install {{ built_wheel }} --force-reinstall"

# install package into system python
setup:
	# install the library into system python
	rm -fr ./dist
	poetry build && pip install {{ built_wheel }}  --force-reinstall

# publish package to pypi
publish:
  poetry build
  poetry publish

# generate markdown from source toml file
generate src dest:
  echo '```mermaid' > {{ dest }} && poetry run skillmap {{ src }} >> {{ dest }} && echo '```' >> {{ dest }} 

# generate png from source toml file
png src dest:
  # mermaid cli (https://github.com/mermaid-js/mermaid-cli) needs to be installed
  poetry run skillmap {{ src }} | mmdc -o {{ dest }}

# generate markdown for sample skillmap
generate_sample:
  just generate {{ sample_toml }} {{ sample_md }}

# generate png for sample skillmap
png_sample:
  just png {{ sample_toml }} {{ sample_png }}

# develop sample skillmap by hot reloading the file and generated results
dev_sample:
  find "tests" -iname "*.toml" | entr -s "just generate_sample"


