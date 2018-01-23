#!/usr/bin/env python
import os
import sys
import re
import toml


ENV = dict(os.environ)
ENTRYPOINT = ENV.pop('DOCKER_ENTRYPOINT')


def convert(typ, value):
    if typ is int:
        return int(value)
    elif typ == float:
        return float(value)
    elif typ == bool:
        if value.lower() in ('false', '0'):
            return False
        else:
            return True
    else:
        return value


def main():
    with open("/etc/config.toml", "w+") as dest, \
         open("/etc/config.base.toml") as base:
        parsed_toml = toml.load(base)

        for item, value in ENV.items():
            if not '_' in item:
                continue

            item = item.lower()
            section, key = item.split("_", 1)

            if section not in parsed_toml:
                continue

            parts = key.split('_')
            k = ''

            for i in range(len(parts)):
                k = "-".join(parts[:i+1])

                if k in parsed_toml[section]:
                    break

            if k not in parsed_toml[section]:
                continue

            key = k

            if '_' in value:
                array_name, value = value.split('_')

                if array_name not in parsed_toml[section][key]:
                    parsed_toml[section][key][array_name] = []

                parsed_toml[section][key][array_name].append(
                    type(parsed_toml[section][key][array_name][0]),
                    value
                )
            else:
                parsed_toml[section][key] = convert(
                    type(parsed_toml[section][key]), value
                )

        toml.dump(parsed_toml, dest)

    args = [ENTRYPOINT]
    args += sys.argv[1:]
    args += ['-config', "/etc/config.toml"]

    if not os.path.exists(parsed_toml['data']['path']):
        os.makedirs(parsed_toml['data']['path'])

    os.execv(ENTRYPOINT, args)


if __name__ == '__main__':
    main()