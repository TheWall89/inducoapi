import yaml
from openapi3 import OpenAPI

from json2openapi.json2openapi import build_openapi


def test_get_employees_200():
  oapi = build_openapi('GET', '/employees', 200)
  OpenAPI(oapi)
  with open('tests/test_get_employees_200.yaml') as f:
    assert yaml.safe_load(f.read()) == oapi


def test_get_employees_200_response():
  oapi = build_openapi('GET', '/employees', 200,
                       response='examples/employees.json')
  OpenAPI(oapi)
  with open('tests/test_get_employees_200_response.yaml') as f:
    assert yaml.safe_load(f.read()) == oapi


def test_get_employees_200_response_yaml():
  oapi = build_openapi('GET', '/employees', 200,
                       response='examples/employees.yaml')
  OpenAPI(oapi)
  with open('tests/test_get_employees_200_response.yaml') as f:
    assert yaml.safe_load(f.read()) == oapi


def test_post_employees_201_request_response():
  oapi = build_openapi('POST', '/employees', 201,
                       request='examples/new_employee_req.json',
                       response='examples/new_employee_resp.json')
  OpenAPI(oapi)
  with open('tests/test_post_employees_201_request_response.yaml') as f:
    assert yaml.safe_load(f.read()) == oapi
