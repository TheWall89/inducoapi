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
import sys

from openapi3.errors import SpecError

from .inducoapi import build_openapi, _get_parser, _write_output


def main():
    args = _get_parser().parse_args()

    try:
        oapi = build_openapi(args.method, args.path, args.resp_code,
                             request=args.request, response=args.response,
                             media_type=args.media_type, example=args.example)
    except SpecError as e:
        sys.exit(f'OpenApi validation error! {e.message}')

    _write_output(oapi, args.output)


if __name__ == '__main__':
    main()
