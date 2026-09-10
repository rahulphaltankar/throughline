PYTHONPATH=src

.PHONY: all test gates ontology pp20 plan skill check clean

# Everything CI runs.
all: check

check: test ontology gates
	@echo "All checks passed."

test:
	PYTHONPATH=$(PYTHONPATH) python -m pytest -q

# Exhaustive archetype + registry graph validation.
ontology:
	python scripts/validate_ontology.py

# Tier-0 artefact gate over the PP20 benchmark fixtures, plus proof that every
# deliberately-broken fixture is rejected.
gates: pp20
	@echo "Checking that broken fixtures are rejected..."
	@PYTHONPATH=$(PYTHONPATH) python -m pytest -q tests/test_gate.py

pp20:
	python scripts/run_pp20_pipeline.py

# Compile the PP20 intake into an artefact plan.
plan:
	PYTHONPATH=$(PYTHONPATH) python -m throughline.cli plan projects/pp20/problem.yaml --out projects/pp20/blueprint

skill:
	python scripts/package_skill.py

clean:
	rm -rf projects/*/blueprint dist build .pytest_cache
