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
dockertext = sys.stdin.read()
outfile = os.path.join(args.coin, "Dockerfile")

for (regex, repl) in subst.items():
    dockertext = regex.sub(str(repl), dockertext)

with open(outfile, "w") as f:
    f.write(dockertext)

# Create the Explorer settings file
infile = "explorer-settings.json.in"
outfile = os.path.join(args.coin, "explorer-settings.json")

with open(infile, "r") as f:
    settings = f.read()

for (regex, repl) in subst.items():
    settings = regex.sub(str(repl), settings)

with open(outfile, "w") as f:
    f.write(settings)

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

