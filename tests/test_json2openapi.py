import yaml
from openapi3 import OpenAPI

from json2openapi.json2openapi import build_openapi


def test_get_employees_200():
  oapi = build_openapi('GET', '/employees', 200)
  OpenAPI(oapi)
  with open('test_get_employees_200.yaml') as f:
    assert yaml.safe_load(f.read()) == oapi

def test_get_employees_200_response():
  oapi = build_openapi('GET', '/employees', 200, response='../examples/employees.json')
  OpenAPI(oapi)
  with open('test_get_employees_200_response.yaml') as f:
    assert yaml.safe_load(f.read()) == oapi
