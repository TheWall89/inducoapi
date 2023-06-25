import pytest
from inducoapi.inducoapi import build_openapi
from openapi_spec_validator.readers import read_from_filename

pytestmark = pytest.mark.parametrize("openapi_version", [("3.0.0"), ("3.1.0")])


def test_get_employees_200(openapi_version):
    oapi = build_openapi("GET", "/employees", "200", openapi_version=openapi_version)
    spec_dict, spec_url = read_from_filename("tests/test_get_employees_200.yaml")
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_params(openapi_version):
    oapi = build_openapi(
        "GET",
        "/employees",
        "200",
        parameters=[("id", "path"), ("limit", "query"), ("token", "header")],
        openapi_version=openapi_version,
    )
    spec_dict, spec_url = read_from_filename("tests/test_get_employees_200_params.yaml")
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_info(openapi_version):
    oapi = build_openapi(
        "GET",
        "/employees",
        "200",
        title="Custom Title",
        version="v1-custom",
        openapi_version=openapi_version,
    )
    spec_dict, spec_url = read_from_filename("tests/test_get_employees_200_info.yaml")
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_response(openapi_version):
    with open("examples/employees.json") as f:
        response = f.read()
    oapi = build_openapi(
        "GET", "/employees", "200", response=response, openapi_version=openapi_version
    )
    spec_dict, spec_url = read_from_filename(
        "tests/test_get_employees_200_response.yaml"
    )
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_response_ref(openapi_version):
    with open("examples/employees.json") as f:
        response = f.read()
    oapi = build_openapi(
        "GET",
        "/employees",
        "200",
        response=response,
        reference=True,
        openapi_version=openapi_version,
    )
    spec_dict, spec_url = read_from_filename(
        "tests/test_get_employees_200_response_ref.yaml"
    )
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_response_noexample(openapi_version):
    with open("examples/employees.json") as f:
        response = f.read()
    oapi = build_openapi(
        "GET",
        "/employees",
        "200",
        response=response,
        example=False,
        openapi_version=openapi_version,
    )
    spec_dict, spec_url = read_from_filename(
        "tests/test_get_employees_200_response_noexample.yaml"
    )
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_response_yaml(openapi_version):
    with open("examples/employees.yaml") as f:
        response = f.read()
    oapi = build_openapi(
        "GET", "/employees", "200", response=response, openapi_version=openapi_version
    )
    spec_dict, spec_url = read_from_filename(
        "tests/test_get_employees_200_response.yaml"
    )
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_get_employees_200_response_mediatype(openapi_version):
    with open("examples/employees.json") as f:
        response = f.read()
    oapi = build_openapi(
        "GET",
        "/employees",
        "200",
        response=response,
        media_type="application/yaml",
        openapi_version=openapi_version,
    )
    spec_dict, spec_url = read_from_filename(
        "tests/test_get_employees_200_response_mediatype.yaml"
    )
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_post_employees_201_request_response(openapi_version):
    with open("examples/new_employee_req.json") as f:
        request = f.read()
    with open("examples/new_employee_resp.json") as f:
        response = f.read()
    oapi = build_openapi(
        "POST",
        "/employees",
        "201",
        request=request,
        response=response,
        openapi_version=openapi_version,
    )
    spec_dict, spec_url = read_from_filename(
        "tests/test_post_employees_201_request_response.yaml"
    )
    spec_dict["openapi"] = openapi_version
    assert oapi == spec_dict


def test_post_employees_201_request_invalid_json(openapi_version):
    with open("tests/invalid.json") as f:
        request = f.read()
    with pytest.raises(ValueError) as excinfo:
        build_openapi(
            "POST",
            "/employees",
            "201",
            request=request,
            openapi_version=openapi_version,
        )
    assert "request" in str(excinfo)


def test_post_employees_201_request_invalid_yaml(openapi_version):
    with open("tests/invalid.yaml") as f:
        request = f.read()
    with pytest.raises(ValueError) as excinfo:
        build_openapi(
            "POST",
            "/employees",
            "201",
            request=request,
            openapi_version=openapi_version,
        )
    assert "request" in str(excinfo)


def test_post_employees_201_response_invalid_json(openapi_version):
    with open("tests/invalid.json") as f:
        response = f.read()
    with pytest.raises(ValueError) as excinfo:
        build_openapi(
            "POST",
            "/employees",
            "201",
            response=response,
            openapi_version=openapi_version,
        )
    assert "response" in str(excinfo)


def test_post_employees_201_response_invalid_yaml(openapi_version):
    with open("tests/invalid.yaml") as f:
        response = f.read()
    with pytest.raises(ValueError) as excinfo:
        build_openapi(
            "POST",
            "/employees",
            "201",
            response=response,
            openapi_version=openapi_version,
        )
    assert "response" in str(excinfo)
