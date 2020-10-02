import yaml
from inducoapi.__main__ import _load_file
from inducoapi.inducoapi import build_openapi


def test_get_employees_200():
    oapi = build_openapi("GET", "/employees", 200)
    with open("tests/test_get_employees_200.yaml") as f:
        assert yaml.safe_load(f.read()) == oapi


def test_get_employees_200_response():
    oapi = build_openapi("GET", "/employees", 200,
                         response=_load_file("examples/employees.json"))
    with open("tests/test_get_employees_200_response.yaml") as f:
        assert yaml.safe_load(f.read()) == oapi


def test_get_employees_200_response_noexample():
    oapi = build_openapi("GET", "/employees", 200,
                         response=_load_file("examples/employees.json"),
                         example=False)
    with open("tests/test_get_employees_200_response_noexample.yaml") as f:
        assert yaml.safe_load(f.read()) == oapi


def test_get_employees_200_response_yaml():
    oapi = build_openapi("GET", "/employees", 200,
                         response=_load_file("examples/employees.yaml"))
    with open("tests/test_get_employees_200_response.yaml") as f:
        assert yaml.safe_load(f.read()) == oapi


def test_get_employees_200_response_mediatype():
    oapi = build_openapi("GET", "/employees", 200,
                         response=_load_file("examples/employees.json"),
                         media_type="application/yaml")
    with open("tests/test_get_employees_200_response_mediatype.yaml") as f:
        assert yaml.safe_load(f.read()) == oapi


def test_post_employees_201_request_response():
    oapi = build_openapi("POST", "/employees", 201,
                         request=_load_file("examples/new_employee_req.json"),
                         response=_load_file("examples/new_employee_resp.json"))
    with open("tests/test_post_employees_201_request_response.yaml") as f:
        assert yaml.safe_load(f.read()) == oapi
