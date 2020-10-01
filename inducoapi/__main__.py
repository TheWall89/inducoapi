#!/usr/bin/env python3

#  Copyright 2020 Matteo Pergolesi <matpergo [at] gmail [dot] com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse

from openapi3 import OpenAPI
from openapi3.errors import SpecError

from inducoapi import build_openapi, _write_output


def _get_parser():
    descr = "A simple python program to generate OpenApi documentation by " \
            "supplying request/response bodies"
    fmt = argparse.ArgumentDefaultsHelpFormatter
    usage = "%(prog)s METHOD PATH CODE [options]"
    p = argparse.ArgumentParser("inducoapi.py", description=descr,
                                usage=usage, formatter_class=fmt)
    p.add_argument("method", type=str,
                   choices=["GET", "POST", "PUT", "PATCH", "DELETE"],
                   metavar="METHOD",
                   help="HTTP request method")
    p.add_argument("path", type=str, metavar="PATH",
                   help="URI path")
    p.add_argument("resp_code", type=int, metavar="CODE",
                   help="HTTP response code")
    p.add_argument("--request", type=str, metavar="PATH",
                   help="Path to file containing request body")
    p.add_argument("--response", type=str, metavar="PATH",
                   help="Path to file containing response body")
    p.add_argument("--output", type=str, metavar="PATH",
                   help="Path to output file")
    p.add_argument("--no-example", "-ne", dest="example", default=True,
                   action="store_false",
                   help="Do not generate schema examples")
    p.add_argument("--media-type", type=str, default="application/json",
                   metavar="STR",
                   help="Desired media type to be used")
    return p


def main():
    args = _get_parser().parse_args()

    oapi = build_openapi(args.method, args.path, args.resp_code,
                         request=args.request, response=args.response,
                         media_type=args.media_type, example=args.example)

    try:
        OpenAPI(oapi)
    except SpecError as e:
        print("OpenApi validation error! {}".format(e.message))
        return

    _write_output(oapi, args.output)


if __name__ == '__main__':
    main()
