PYTHONPATH=src

.PHONY: test pp20 skill

test:
	PYTHONPATH=$(PYTHONPATH) python -m pytest -q

pp20:
	PYTHONPATH=$(PYTHONPATH) python -m throughline.cli plan projects/pp20/problem.yaml --out projects/pp20/blueprint

skill:
	python scripts/package_skill.py
