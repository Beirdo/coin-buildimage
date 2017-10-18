#! /usr/bin/env python3.5
# vim:ts=4:sw=4:ai:et:si:sts=4

import argparse
import json
import re
import os
import uuid
import shutil
import sys


def convertConfig(config):
    keys = list(map(lambda x: re.compile(r"@%s@" % x, re.I), config.keys()))
    values = list(config.values())
    subst = dict(zip(keys, values))
    return subst


def substituteFile(infile, outfile, subst):
    if infile == "stdin":
        text = sys.stdin.read()
    else:
        with open(infile, "r") as f:
            text = f.read()

    for (regex, repl) in subst.items():
        text = regex.sub(str(repl), text)

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
with open("%s.json" % args.coin, "r") as f:
    config = json.load(f)

subst = convertConfig(config)

subst.update(convertConfig({ "id": os.geteuid(), "group": os.getegid() }))

# Create the Dockerfile
outfile = os.path.join(args.coin, "Dockerfile")
substituteFile("stdin", outfile, subst)

# Create the pull-artifacts script
infile = "pull-artifacts.in"
outfile = os.path.join(args.coin, "pull-artifacts")
substituteFile(infile, outfile, subst)

