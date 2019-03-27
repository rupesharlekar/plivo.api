Verify the messaging functionality of the Plivo API as per [assignment](https://github.com/rupesharlekar/plivo.api/blob/master/Message%20API.pdf) document

Tests Performed
1. All the tests / steps mentioned in the ***Scenarios*** section of the [assignment](https://github.com/rupesharlekar/plivo.api/blob/master/Message%20API.pdf) document are coded for.
Prerequisite are taken care of by using an _function_ scoped _pytest fixture_ and actual test is performed inside _test__ definition 
 
## Technology / Frameworks used
- [python3](https://www.python.org/) as programming language
- [pytest](https://docs.pytest.org/en/latest/) versatile test framework for python
- [pytest-html](https://pypi.org/project/pytest-html/) plugin for generation of HTML reports for pytest tests
- [requests](http://docs.python-requests.org/en/master/) for working with different HTTP methods
- [json](https://www.json.org/)

## Features
- test code is scalable
- used to connect to API that uses HTTP Basic Authentication

## Installation
`git clone git@github.com:rupesharlekar/plivo.api.git  && cd plivo.api`  
`pip install -r requirements.txt`

## How to run tests
`cd ../plivo.api/src/tests/functional`  
`pytest -vs test_messaging.py -m functional`
