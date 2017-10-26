#! /usr/bin/env python3.5
# vim:ts=4:sw=4:ai:et:si:sts=4

import argparse
import json
import re
import os
import uuid
import shutil
import sys

filterRe = re.compile(r'(?P<block>^%=(?P<mode>.)?\s+(?P<label>.*?)\s+(?P<value>[^\s\n$]+?)(?:\s*.*?)?^(?P<section>.*?)^=%.*?$)', re.M | re.S)


def convertConfig(config):
    keys = list(config.keys())
    regexes = list(map(lambda x: re.compile(r"@%s@" % x, re.I), keys))
    values = list(config.values())
    subst = zip(keys, regexes, values)
    subst = {key: {'regex': regex, 'value': value}
             for (key, regex, value) in subst}
    return subst


def substituteFile(infile, outfile, subst):
    if infile == "stdin":
        text = sys.stdin.read()
    else:
        with open(infile, "r") as f:
            text = f.read()

    for item in subst.values():
        regex = item.get('regex', None)
        repl = item.get('value', None)
        if regex is None or repl is None:
            continue
        text = regex.sub(str(repl), text)

    blocks = filterRe.findall(text)
    for (block, mode, label, value, section) in blocks:
        subvalue = subst.get(label.lower(), {}).get('value', None)
        print(mode, label, value, subvalue)
        if mode == '+' or mode == '':
            if subvalue is not None and str(subvalue) != value:
                section = ""
        elif mode == '-':
            if subvalue is None or str(subvalue) != value:
                section = ""
        text = text.replace(block, section)

    with open(outfile, "w") as f:
        f.write(text)


def copyfile(coin, infile, outfile=None):
    if not outfile:
        outfile = infile
    outfile = os.path.join(coin, outfile)
    shutil.copyfile(infile, outfile)


parser = argparse.ArgumentParser(description="Substitute in variables")
parser.add_argument('--coin', '-c', required=True, help="Which coin")
args = parser.parse_args()

# First read the config file
with open("config/%s.json" % args.coin, "r") as f:
    config = json.load(f)

subst = convertConfig(config)
subst.update(convertConfig({ "id": os.geteuid(), "group": os.getegid() }))

buildDir = os.path.join("build", args.coin)

# Create the Dockerfile
outfile = os.path.join(buildDir, "Dockerfile")
substituteFile("stdin", outfile, subst)

# Create the pull-artifacts script
infile = "pull-artifacts.in"
outfile = os.path.join(buildDir, "pull-artifacts")
substituteFile(infile, outfile, subst)

