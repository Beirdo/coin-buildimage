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
    if not os.path.exists(infile):
        return
    if not outfile:
        outfile = infile
    outfile = os.path.join("build", coin, outfile)
    shutil.copyfile(infile, outfile)


parser = argparse.ArgumentParser(description="Substitute in variables")
parser.add_argument('--coin', '-c', required=True, help="Which coin")
parser.add_argument('--nodaemon', '-D', action="store_false", dest="daemon",
                    help="Don't copy daemon")
args = parser.parse_args()

# First read the config file
with open("config/%s.json" % args.coin, "r") as f:
    config = json.load(f)

config = {key.lower(): value for (key, value) in config.items()}

subst = convertConfig(config)

# Create a config file
outconfig = {
    "daemon": 1,
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

buildDir = os.path.join("build", args.coin)

conffile = os.path.join(buildDir, "%s.conf" % config['coinname'])
with open(conffile, "w") as f:
    for (key, values) in sorted(outconfig.items()):
        if not isinstance(values, list):
            values = [values]
        for value in values:
            f.write("%s=%s\n" % (key, value))

# Create the Dockerfile
outfile = os.path.join(buildDir, "Dockerfile")
substituteFile("stdin", outfile, subst)

# Create the node run Dockerfile
infile = "Dockerfile.node.in"
outfile = os.path.join(buildDir, "Dockerfile.node")
substituteFile(infile, outfile, subst)

# Create the startup script
infile = "startup.sh.in"
outfile = os.path.join(buildDir, "startup.sh")
substituteFile(infile, outfile, subst)

# Create the Explorer settings file
infile = "explorer-settings.json.in"
outfile = os.path.join(buildDir, "explorer-settings.json")
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
port = config.get('p2poolport', None)
usep2pool = config.get('usep2pool', None)
if port and usep2pool:
    ports.append(port)

ports = list(map(lambda x: "-p %s:%s" % (x, x), ports))
ports = " ".join(ports)
outfile = os.path.join(buildDir, "ports.txt")
with open(outfile, "w") as f:
    f.write(ports)

# Copy over the daemon
if args.daemon:
    infile = os.path.join("..", "build", "artifacts", config["coinname"],
                          "linux", config['daemonname'])
    copyfile(args.coin, infile, config['daemonname'])

# Copy over the mongo init script and the crontab for explorer
copyfile(args.coin, "explorer.mongo")
copyfile(args.coin, "explorer-crontab")

# Copy the sudoers.d file
copyfile(args.coin, "sudoers-coinnode")

# Copy the coin-cli script
copyfile(args.coin, "coin-cli")

# Copy the nodejs archive
copyfile(args.coin, "node-v8.7.0-linux-x64.tar.xz")

if config.get('copyawscreds', False):
    copyfile(args.coin, os.path.expanduser("~/.aws/credentials"),
             "aws-credentials")
