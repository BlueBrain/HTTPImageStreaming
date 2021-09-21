# HTTP image streamer

A service that streams images from one or many rendering resources.


## ChangeLog

To keep track of the changes between releases check the
[changelog](doc/Changelog.md).

## Installation
Install python 2.6 or 2.7 , and virtualenv with apt-get and pip

### In the context of the Human Brain Project
Test execution from source
```
make virtualenv
. platform_venv/bin/activate
make test
```

### In any other context

```
virtualenv env
. ./env/bin/activate
pip install -r requirements.txt
```

### Initial Configuration

##Preparation for a commit submission
This will run pep8, pylint and unit tests
```
make verify_changes
```

##SECURITY WARNING: don't run with debug turned on in production!
In the settings.py file, make sure that:
```
HISS_DEBUG = False
```

## Funding & Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2021 Blue Brain Project/EPFL
