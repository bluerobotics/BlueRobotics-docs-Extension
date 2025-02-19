#! /usr/bin/env python3

import fileinput
from datetime import date

today = date.today()
new_version = f'{today.year}.{today.month}.{today.day}'

with fileinput.input('Dockerfile', inplace=True) as dockerfile:
    for line in dockerfile:
        if line.startswith('LABEL version='):
            print(f'LABEL version="{new_version}"')
        else:
            print(line, end='')

print(f'tag={new_version}')
