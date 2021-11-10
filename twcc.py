#!/usr/bin/env python

import json, sys, os, time, argparse
from subprocess import DEVNULL, STDOUT, PIPE, Popen, check_output

def sleep(t=5, dt=0.1, verbose=False):
    st = time.time()
    if not verbose:
        time.sleep(t)
        return
    for i in range(int(t/dt)):
        print('Waiting ... %05.2f sec.' % (time.time() - st), end='\r')
        time.sleep(dt)

def get_containers():
    containers = []
    status = {}
    sids = {}
    for js in json.loads(check_output('twccli ls ccs -json'.split()).strip()):
        if js['status'] in ['Initializing', 'Ready', 'NotReady']:
            containers.append(js)
            status[js['id']] = js['status']
            sids[js['name']] = js['id']
    return containers, status, sids

def get_sid(name, sids):
    if name not in sids:
        return -1
    return sids[name]

def build(name, gpu, stdout=STDOUT):
    Popen(('twccli mk ccs -n %s -itype PyTorch -img pytorch-21.02-py3:latest -gpu %s' % (name, gpu)).split(), stdout=stdout, stderr=stdout)

def connect(sid, ctype, cnts, status):
    ssh = check_output(('twccli ls ccs -s %s -g%s' % (sid, ctype)).split()).decode('utf-8').strip()
    while status[sid] != 'Ready':
        sleep(5, verbose=False)
        _, status, _ = get_containers()

    # Can't directly execute the command
    print('ssh %s' % (ssh))

def main(args):
    if args.cmd is None:
        args.cmd = 'cnt'
    # ls
    if args.cmd == 'ls':
        Popen('twccli ls ccs'.split()).communicate()

    # mk
    elif args.cmd == 'mk':
        build(args.name, args.gpu)
    else:
        containers, status, sids = get_containers() 
        sid = get_sid(args.name, sids) if args.name else args.site_id

    # connect
        if args.cmd == 'cnt':
            # Not found, make a new container
            if sid == -1:
                build(args.name if args.name else args.site_id, args.gpu, stdout=DEVNULL)
                sleep(5, verbose=False)
                containers, status, sids = get_containers()
                sid = get_sid(args.name, sids)
            connect(sid, args.type, containers, status)
        elif args.cmd == 'rm':
            Popen(('twccli rm ccs -s %s' % (sid)).split() + (['-f'] if args.force else [])).communicate()

if __name__ == '__main__':
    p = argparse.ArgumentParser()

    # default cnt
    g = p.add_mutually_exclusive_group()
    g.add_argument('-n', '--name', type=str, default=None)
    g.add_argument('-s', '--site_id', type=str, default=None)
    p.add_argument('-g', '--gpu', type=int, default=2)
    p.add_argument('-t', '--type', type=str, choices=['ssh', 'pynb'], default='ssh')

    # mk
    subp = p.add_subparsers(dest='cmd')
    mkp = subp.add_parser('mk')
    mkp.add_argument('-n', '--name', type=str, default=None)
    mkp.add_argument('-g', '--gpu', type=int, default=2)

    # ls
    lsp = subp.add_parser('ls')
    lsg = lsp.add_mutually_exclusive_group()
    lsg.add_argument('-n', '--name', type=str, default=None)
    lsg.add_argument('-s', '--site_id', type=str, default=None)

    # cnt
    cntp = subp.add_parser('cnt')
    cntg = cntp.add_mutually_exclusive_group()
    cntg.add_argument('-n', '--name', type=str, default=None)
    cntg.add_argument('-s', '--site_id', type=str, default=None)
    cntp.add_argument('-g', '--gpu', type=int, default=2)
    cntp.add_argument('-t', '--type', type=str, choices=['ssh', 'pynb'], default='ssh')

    rmp = subp.add_parser('rm')
    rmg = rmp.add_mutually_exclusive_group()
    rmg.add_argument('-n', '--name', type=str, default=None)
    rmg.add_argument('-s', '--site_id', type=str, default=None)
    rmp.add_argument('-f', '--force', action='store_true')

    args = p.parse_args()
    main(args)
