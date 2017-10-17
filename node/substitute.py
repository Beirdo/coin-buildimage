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


parser = argparse.ArgumentParser(description="Substitute in variables")
parser.add_argument('--coin', '-c', required=True, help="Which coin")
args = parser.parse_args()

# First read the config file
with open("%s.json" % args.coin, "r") as f:
    config = json.load(f)

subst = convertConfig(config)

# Create a config file
outconfig = {
    "dns": 1,
    "server": 1,
    "listen": 1,
    "rpcport": config['rpcport'],
    "rpcallowip": "127.0.0.1",
    "rpcuser": "%srpc" % config['coinname'],
    "rpcpassword": str(uuid.uuid4()),
}

addnodes = config.get('addnodes', [])
if not isinstance(addnodes, list):
    addnodes = [addnodes]

if addnodes:
    outconfig['addnode'] = addnodes

# Add the config setting to the mapping
subst.update(convertConfig(outconfig))

conffile = os.path.join(args.coin, "%s.conf" % config['coinname'])
with open(conffile, "w") as f:
    for (key, values) in sorted(outconfig.items()):
        if not isinstance(values, list):
            values = [values]
        for value in values:
            f.write("%s=%s\n" % (key, value))

# Create the Dockerfile
outfile = os.path.join(args.coin, "Dockerfile")
substituteFile("stdin", outfile, subst)

# Create the node run Dockerfile
infile = "Dockerfile.node.in"
outfile = os.path.join(args.coin, "Dockerfile.node")
substituteFile(infile, outfile, subst)

# Create the startup script
infile = "startup.sh.in"
outfile = os.path.join(args.coin, "startup.sh")
substituteFile(infile, outfile, subst)

# Create the Explorer settings file
infile = "explorer-settings.json.in"
outfile = os.path.join(args.coin, "explorer-settings.json")
substituteFile(infile, outfile, subst)

# Copy over the daemon
infile = os.path.join("..", "build", "artifacts", "linux", config['daemon'])
outfile = os.path.join(args.coin, config['daemon'])
shutil.copyfile(infile, outfile)

# Copy over the mongo init script and the crontab for explorer
infile = "explorer.mongo"
outfile = os.path.join(args.coin, infile)
shutil.copyfile(infile, outfile)

infile = "explorer-crontab"
outfile = os.path.join(args.coin, infile)
shutil.copyfile(infile, outfile)

# Copy the sudoers.d file
infile = "sudoers-coinnode"
outfile = os.path.join(args.coin, infile)
shutil.copyfile(infile, outfile)

# Copy the coin-cli script
infile = "coin-cli"
outfile = os.path.join(args.coin, infile)
shutil.copyfile(infile, outfile)
