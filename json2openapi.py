import json
from typing import Dict, Tuple, Any

import sys
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
    with open(sys.argv[1]) as json_file:
        json_data = json.load(json_file)
        schema = create_element(json_data)
        print(yaml.dump(schema, indent=2, Dumper=NoAliasDumper))


if __name__ == '__main__':
    main()
