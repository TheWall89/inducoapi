import argparse
import json
from typing import Dict, Tuple, Any

import yaml


def get_type_ex(val: Any) -> Tuple[str, Any]:
    ex = val
    if val is None:
        t = "string"
        ex = ""
    elif type(val) is str:
        t = "string"
    elif type(val) is int:
        t = "integer"
    elif type(val) is float:
        t = "number"
    elif type(val) is bool:
        t = "boolean"
    else:
        t = ""
        print("unknown type: {}, value: {}".format(type(val), val))
    return t, ex


def create_element(d: Dict) -> Dict:
    el = {}
    for key, val in d.items():
        el[key] = {}
        if type(val) is dict:  # recursive case
            el[key]["type"] = "object"
            el[key]["properties"] = create_element(val)
        elif type(val) is list:
            el[key]["type"] = "array"
            el[key]["items"] = {}
            if val and type(val[0]) is dict:  # recursive case
                el[key]["items"]["type"] = "object"
                el[key]["items"]["properties"] = create_element(val[0])
            elif val:  # base case
                el[key]["items"]["type"], el[key]["items"][
                    "example"] = get_type_ex(val[0])
        else:  # base case
            el[key]["type"], el[key]["example"] = get_type_ex(val)
    return el


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def main():
    descr = "Simple script to generate OpenAPI block from JSON request/response"
    parser = argparse.ArgumentParser("json2openapi.py", description=descr)
    parser.add_argument("req_m", type=str,
                        choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
                        help="HTTP request method")
    parser.add_argument("resp_code", type=int, help="Response code")
    parser.add_argument("--req-path", "-req", type=str,
                        help="Path to JSON file containing request body")
    parser.add_argument("--resp-path", "-resp", type=str,
                        help="Path to JSON file containing response body")
    args = parser.parse_args()
    res = {
        args.req_m.lower(): {}
    }
    if args.req_path:
        with open(args.req_path) as req_path:
            req_body = json.load(req_path)
            res[args.req_m.lower()]["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": create_element(req_body)
                        }
                    },
                    "application/yaml": {
                        "schema": {
                            "type": "object",
                            "properties": create_element(req_body)
                        }
                    }
                }
            }

    if args.resp_path:
        with open(args.resp_path) as resp_path:
            resp_body = json.load(resp_path)
            if isinstance(resp_body, list) and resp_body:
                schema = {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": create_element(resp_body[0])
                    }
                }
            else:
                schema = {
                    "type": "object",
                    "properties": create_element(resp_body)
                }
            res[args.req_m.lower()]["responses"] = {
                args.resp_code: {
                    "content": {
                        "application/json": {
                            "schema": schema
                        },
                        "application/yaml": {
                            "schema": schema
                        }
                    }
                }}
    print(yaml.dump(res, indent=2, Dumper=NoAliasDumper, sort_keys=False))


if __name__ == '__main__':
    main()
