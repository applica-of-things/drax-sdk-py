# draxsdk
Python SDK for Drax platform

### Installation 
To install the package you need to run the following command:

`$ python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps draxsdk`

### Usage 
Import drax SDK module in your code:
```python
from draxsdk import drax

```

### Generate docstring with Sphinx 
```bash
$ cd docs && make html

```

### Pypi test repository: generate and publish
```python
$ python3 -m build
$ python3 -m twine upload --repository testpypi dist/*

```

