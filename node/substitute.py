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
parser.add_argument('--nodaemon', '-D', action="store_false", dest="daemon",
                    help="Don't copy daemon")
args = parser.parse_args()

# First read the config file
with open("%s.json" % args.coin, "r") as f:
    config = json.load(f)

config = {key.lower(): value for (key, value) in config.items()}

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

# Create the ports file
ports = []
port = config.get('p2pport', None)
if port:
    ports.append(port)
port = config.get('explorerport', None)
useexplorer = config.get('useexplorer', None)
if port and useexplorer:
    ports.append(port)

ports = list(map(lambda x: "-p %s:%s" % (x, x), ports))
ports = " ".join(ports)
outfile = os.path.join(args.coin, "ports.txt")
with open(outfile, "w") as f:
    f.write(ports)

# Copy over the daemon
if args.daemon:
    infile = os.path.join("..", "build", "artifacts", "linux", config['daemon'])
    copyfile(args.coin, infile, config['daemon'])

# Copy over the mongo init script and the crontab for explorer
copyfile(args.coin, "explorer.mongo")
copyfile(args.coin, "explorer-crontab")

# Copy the sudoers.d file
copyfile(args.coin, "sudoers-coinnode")

# Copy the coin-cli script
copyfile(args.coin, "coin-cli")

# Copy the nodejs archive
copyfile(args.coin, "node-v8.7.0-linux-x64.tar.xz")
