# npCrypto
Numpy implementation of some crypto primitives.

## Environement setup
You need to setup the environement before starting.
First, create a python virtual environement.

```bash
virtualenv -p python3 <name of virtualenv>
source <name of virtualenv>/bin/activate
```

Then, you must install the project required packages:

```bash
pip install -r requirements.txt
```

Finally you can install the npcrypto package:
```bash
pip install -e .
```

## Build the documentation

```bash
cd docs
make html
```

You can now access the html version of the documentation

```bash
<your navigator> build/html/index.html
```
