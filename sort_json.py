import json
import sys

if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        json_data = json.load(json_file)
        print(json.dumps(json_data, sort_keys=True, indent=2))
