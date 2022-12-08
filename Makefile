build:
	python -m build

clean:
	rm -fr dist

test-publish:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*
