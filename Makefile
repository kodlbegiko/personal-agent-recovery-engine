.PHONY: verify reproduce
verify:
	python -m pytest
	python scripts/verify_integrity.py
reproduce:
	python -m pytest
	python scripts/verify_integrity.py
	python -m pare.evaluation.experiment
