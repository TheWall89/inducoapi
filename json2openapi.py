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


def _gen_properties(d: Dict) -> Dict:
    el = {}
    for key, val in d.items():
        el[key] = {}
        if type(val) is dict:  # recursive case
            el[key]["type"] = "object"
            el[key]["properties"] = _gen_properties(val)
        elif type(val) is list:
            el[key]["type"] = "array"
            el[key]["items"] = {}
            if val and type(val[0]) is dict:  # recursive case
                el[key]["items"]["type"] = "object"
                el[key]["items"]["properties"] = _gen_properties(val[0])
            elif val:  # base case
                el[key]["items"]["type"], el[key]["items"][
                    "example"] = get_type_ex(val[0])
        else:  # base case
            el[key]["type"], el[key]["example"] = get_type_ex(val)
    return el


def _gen_content(json_data) -> Dict:
    if not json_data:
        # TODO raise exception
        pass
    if isinstance(json_data, list):
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": _gen_properties(json_data[0])
            }
        }
    else:
        schema = {
            "type": "object",
            "properties": _gen_properties(json_data)
        }
    return {
        "application/json": {
            "schema": schema
        }
    }


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def main():
    descr = "Simple script to generate OpenAPI block from JSON request/response"
    parser = argparse.ArgumentParser("json2openapi.py", description=descr)
    parser.add_argument("req_m", type=str,
                        choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
                        help="HTTP request method")
    parser.add_argument("path", type=str, help="REST resource path")
    parser.add_argument("resp_code", type=int, help="Response code")
    parser.add_argument("--req-json", "-reqj", type=str,
                        help="Path to JSON file containing request body")
    parser.add_argument("--resp-json", "-respj", type=str,
                        help="Path to JSON file containing response body")
    args = parser.parse_args()
    res = {
        args.path: {
            args.req_m.lower(): {}
        }
    }
    if args.req_json:
        with open(args.req_json) as req_json:
            req_body = json.load(req_json)
            res[args.path][args.req_m.lower()]["requestBody"] = {
                "content": _gen_content(req_body)
            }

    if args.resp_json:
        with open(args.resp_json) as resp_json:
            resp_body = json.load(resp_json)
            res[args.path][args.req_m.lower()]["responses"] = {
                args.resp_code: {
                    "description": "",
                    "content": _gen_content(resp_body)
                }
            }

    print(yaml.dump(res, indent=2, Dumper=NoAliasDumper, sort_keys=False))


if __name__ == '__main__':
    main()
