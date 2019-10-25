.PHONY: bootstrap
bootstrap:
	python3 -m venv venv && \
	. ./venv/bin/activate && \
	pip3 install -r requirements.txt

.PHONY: build
build:
	pip3 install --editable .
