#! /usr/bin/env python3.5
# vim:ts=4:sw=4:ai:et:si:sts=4

import argparse
import json
import re
import os
import uuid
import shutil
import sys
import requests


filterRe = re.compile(r'(?P<block>^%=(?P<mode>.)?\s+(?P<label>.*?)\s+(?P<value>[^\s\n$]+)(?:\s*.*?)?^(?P<section>.*?)^=%.*?$)', re.M | re.S)
subItemRe = re.compile(r'@_@')


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
        elif mode == '?':
            if subvalue is None:
                section = ""
        elif mode == '!':
            if subvalue is not None:
                section = ""

        sections = ''
        if not isinstance(subvalue, list):
            subvalue = [subvalue]
        for subval in subvalue:
            sections += subItemRe.sub(str(subval), section)
        text = text.replace(block, sections)

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
parser.add_argument('--pool', '-p', action="store_true",
                    help="Grab pool wallet")
args = parser.parse_args()

buildDir = os.path.join("build", args.coin)

# First read the config file
with open("config/%s.json" % args.coin, "r") as f:
    config = json.load(f)

config = {key.lower(): value for (key, value) in config.items()}
if args.pool:
    config["poolnode"] = 1
    config.pop("grabwallet", None)

subst = convertConfig(config)

if args.coin == 'coiniumserv':
    result = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4")
    subst.update(convertConfig({"hostip": result.text}))
else:
    # Create a config file
    outconfig = {
        "daemon": 1,
        "dns": 1,
        "server": 1,
        "listen": 1,
        "rpcport": config['rpcport'],
        "rpcuser": "%srpc" % config['coinname'],
    }

    if not args.pool:
        rpcallowip = "127.0.0.1"
        rpcpassword = str(uuid.uuid4())
    else:
        rpcallowip = ["127.0.0.1", "172.17.0.*"]
        rpcpassword = "pool-%s" % args.coin

    outconfig["rpcallowip"] = rpcallowip
    outconfig["rpcpassword"] = rpcpassword

    addnodes = config.get('addnodes', [])
    if not isinstance(addnodes, list):
        addnodes = [addnodes]

    if addnodes:
        outconfig['addnode'] = addnodes

    # Add the config setting to the mapping
    subst.update(convertConfig(outconfig))

    conffile = os.path.join(buildDir, "%s.conf" % config['coinname'])
    with open(conffile, "w") as f:
        for (key, values) in sorted(outconfig.items()):
            if not isinstance(values, list):
                values = [values]
            for value in values:
                f.write("%s=%s\n" % (key, value))

# Create the Dockerfile
if args.coin == 'coiniumserv':
    infile = "Dockerfile.coiniumserv.in"
else:
    infile = "Dockerfile.in"
outfile = os.path.join(buildDir, "Dockerfile")
substituteFile(infile, outfile, subst)

# Create the node run Dockerfile
infile = "Dockerfile.node.in"
if args.pool:
    outfile = os.path.join(buildDir, "Dockerfile.pool")
else:
    outfile = os.path.join(buildDir, "Dockerfile.node")
substituteFile(infile, outfile, subst)

# Create the startup script
if args.coin == 'coiniumserv':
    infile = "startup.sh-coiniumserv.in"
else:
    infile = "startup.sh.in"

if args.pool:
    suffix = "-pool.sh"
else:
    suffix = "-node.sh"

outfile = os.path.join(buildDir, "startup%s" % suffix)
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

port = config.get('coiniumservport', None)
if port:
    ports.append(port)

poolports = config.get('stratumports', None)
if poolports:
    if not isinstance(poolports, list):
        poolports = [poolports]
    ports.extend(poolports)

ports = list(map(lambda x: "-p %s:%s" % (x, x), ports))

links = config.get('links', None)
if links:
    links = list(map(lambda x: "--link %s" % x, links))
    ports.extend(links)

ports = " ".join(ports)
outfile = os.path.join(buildDir, "ports.txt")
with open(outfile, "w") as f:
    f.write(ports)

# Copy over the daemon
if args.daemon and args.coin != 'coiniumserv':
    infile = os.path.join("..", "build", "artifacts", config["coinname"],
                          "linux", config['daemonname'])
    copyfile(args.coin, infile, config['daemonname'])

if config.get('useexplorer', False):
    # Create the Explorer settings file
    infile = "explorer-settings.json.in"
    outfile = os.path.join(buildDir, "explorer-settings.json")
    substituteFile(infile, outfile, subst)

    # Copy over the mongo init script and the crontab for explorer
    copyfile(args.coin, "explorer.mongo")
    copyfile(args.coin, "explorer-crontab")

    ## Copy the nodejs archive
    #copyfile(args.coin, "node-v8.7.0-linux-x64.tar.xz")

# Copy the sudoers.d file
copyfile(args.coin, "sudoers-coinnode")

# Copy the coin-cli script
copyfile(args.coin, "coin-cli")

if config.get('copyawscreds', False):
    copyfile(args.coin, os.path.expanduser("~/.aws/credentials"),
             "aws-credentials")
