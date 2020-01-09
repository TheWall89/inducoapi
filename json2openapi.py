import json
import sys
from typing import Dict, List, AnyStr

import yaml


def get_type(val) -> AnyStr:
    if type(val) is str or val is None:
        res = "string"
    elif type(val) is int:
        res = "integer"
    elif type(val) is float:
        res = "number"
    elif type(val) is bool:
        res = "boolean"
    else:
        res = ""
        print("unknown type: {}, value: {}".format(type(val), val))
    return res


def create_element(d: Dict) -> Dict:
    el = {}
    for key, val in d.items():
        el[key] = {}
        el[key]["description"] = "None"
        # Recursive cases
        if type(val) is dict:
            el[key]["type"] = "object"
            el[key]["properties"] = create_element(val)
        elif type(val) is list:
            el[key]["type"] = "array"
            el[key]["items"] = {}
            if val and type(val[0]) is dict:
                el[key]["items"]["type"] = "object"
                el[key]["items"]["description"] = "None"
                el[key]["items"]["properties"] = create_element(val[0])
            elif val:
                el[key]["items"]["type"] = get_type(val[0])
                el[key]["items"]["description"] = "None"
                el[key]["items"]["example"] = val[0]
        # base case
        else:
            el[key]["type"] = get_type(val)
            el[key]["example"] = val
    return el


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        json_data = json.load(json_file)
        schema = create_element(json_data)
        print(yaml.dump(schema, indent=2, Dumper=NoAliasDumper))
