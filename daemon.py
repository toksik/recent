#!/usr/bin/python3

import lib.config
import lib.state
import lib.history
import lib.manager

import argparse
import time
import os
import sys

def get_defpath(name):
    if not os.getenv('HOME'):
        return None
    return os.path.join(os.getenv('HOME'), name)

def get_manager(config, state, history):
    conf_obj = lib.config.RecentConf(config)
    state_obj = lib.state.RecentState(state)
    hist_obj = lib.history.RecentLog(history)
    manager = lib.manager.Manager(conf_obj, state_obj, hist_obj)
    manager.load_providers()
    manager.load_notifiers()
    return manager

def run_daemon(manager):
    while True:
        manager.update()
        time.sleep(5)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='''\
A daemon that updates news sources from time to time and shows notifications
then.''')
    p.add_argument('--fork', '-f', action='store_true',
                   help='fork to background')
    p.add_argument('--config', '-c', default=get_defpath('.recent.conf'),
        help='Use an alternate config file (default is $HOME/recent.conf)')
    p.add_argument('--state', '-s', default=get_defpath('.recent.state'),
        help='Use a different file than $HOME/recent.state for storing which \
        news posts are old')
    p.add_argument('--history', '-l', default=get_defpath('.recent.log'),
        help='Set another file for history (default is $HOME/recent.log)')
    args = p.parse_args()
    if not args.config:
        sys.stderr.write('Error while generating the config file path.\n\
Please specify it by the --config/-c argument.\n')
    if not os.path.isfile(args.config):
        f = open(args.config, 'w')
        f.close()
    if not args.state:
        sys.stderr.write('Error while generating the state file path.\n\
Please specify it by the --state/-s argument.\n')
    if not os.path.isfile(args.state):
        f = open(args.state, 'w')
        f.close()
    if not args.history:
        sys.stderr.write('Error while generating the history file path.\n\
Please specify it by the --history/-l argument.\n')
    if not os.path.isfile(args.history):
        f = open(args.history, 'w')
        f.close()
    m = get_manager(args.config, args.state, args.history)
    if args.fork:
        pid = os.fork()
        if pid == 0:
            run_daemon(m)
    else:
        run_daemon(m)
