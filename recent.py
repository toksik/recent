#!/usr/bin/python3
import lib.history
from lib.markup.markup import LogMarkup, LogOutputMarkup, LogOutputColorMarkup

import os
import sys
import argparse
import struct
import termios
import fcntl
import subprocess

def get_ttywh():
    h, w = struct.unpack('hh', fcntl.ioctl(0, termios.TIOCGWINSZ,
                                           struct.pack('hh', 0, 0)))
    return w, h

def get_defhistory():
    if not os.getenv('HOME'):
        return None
    return os.path.join(os.getenv('HOME'), '.recent.log')

def do_list(args):
    w, h = get_ttywh()
    hist = lib.history.RecentLog(args.history)
    hist.read()
    start = 0
    if len(hist.entries) > args.num:
        start = len(hist.entries)-args.num
        counter = args.num - 1
    else:
        counter = len(hist.entries) - 1
    for entry in hist.entries[start:]:
        lm = LogMarkup()
        lo = LogOutputMarkup(width=0)
        lm.buff = entry.title
        lm.parse(lo)
        if not entry.author:
            head = '[%s] %s'%(entry.provider, lo.buff)
        else:
            head = '[%s] %s: %s'%(entry.provider, entry.author, lo.buff)
        if counter < 10:
            begin = '(  %i)'%counter
        elif counter < 100:
            begin = '( %i)'%counter
        else:
            begin = '(%i)'%counter
        if args.color:
            _head = head[:w-(len(begin)+1)]
            if 'new' in entry.tags and 'unread' in entry.tags:
                line = '%s \033[1m%s\033[0m\n'%(begin, _head)
            elif 'unread' in entry.tags:
                line = '%s \033[36m%s\033[0m\n'%(begin, _head)
            else:
                line = '%s \033[0m%s\033[0m\n'%(begin, _head)
        else:
            head = head[:w-(len(begin)+4)]
            if 'new' in entry.tags and 'unread' in entry.tags:
                line = '%s *u %s\n'%(begin, head)
            elif 'unread' in entry.tags:
                line = '%s  u %s\n'%(begin, head)
            else:
                line = '%s    %s\n'%(begin, head)
        if 'unread' in entry.tags and len(head) <= w-(len(begin)+4) and \
               not entry.body:
            entry.tags.remove('unread')
        sys.stdout.buffer.write(line.encode('utf-8'))
        if 'new' in entry.tags:
            entry.tags.remove('new')
        counter -= 1
    hist.write()

def do_read(args):
    w, h = get_ttywh()
    hist = lib.history.RecentLog(args.history)
    hist.read()
    entry = hist.entries[::-1][args.num]
    if 'new' in entry.tags:
        entry.tags.remove('new')
    if 'unread' in entry.tags:
        entry.tags.remove('unread')
    hist.write()
    lm = LogMarkup()
    if args.color:
        lo = LogOutputColorMarkup(width=w)
    else:
        lo = LogOutputMarkup(width=w)
    if entry.author:
        head = '[%s] %s: %s'%(entry.provider, entry.author, entry.title)
    else:
        head = '[%s] %s'%(entry.provider, entry.title)
    lm.buff = head
    lm.parse(lo)
    text = lo.buff
    if not text.endswith('\n'):
        text = text + '\n'
    sys.stdout.buffer.write(text.encode('utf-8'))
    if entry.body:
        lm = LogMarkup()
        lm.buff = entry.body
        if args.color:
            lo = LogOutputColorMarkup(width=w-1)
        else:
            lo = LogOutputMarkup(width=w-1)
        lm.parse(lo)
        text = lo.buff.strip()
        for _line in text.split('\n'):
            if len(_line) < 2:
                sys.stdout.buffer.write(b'\n')
                continue
            _line = ' '+_line+'\n'
            sys.stdout.buffer.write(_line.encode('utf-8'))
    exit(0)

def open_url(url):
    ps_p = subprocess.Popen(['ps','-A'], stdout=subprocess.PIPE)
    if b'X\n' not in ps_p.stdout.read():
        return
    os.putenv('DISPLAY', ':0')
    p = subprocess.Popen(['xdg-open', url], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

def do_open(args):
    hist = lib.history.RecentLog(args.history)
    hist.read()
    entry = hist.entries[::-1][args.num]
    if 'link' in args and args.link != None:
        lm = LogMarkup()
        lm.buff = entry.title
        _lo = LogOutputMarkup(width=0)
        lm.parse(_lo)
        lm = LogMarkup()
        lm.buff = entry.body
        lo = LogOutputMarkup(width=0)
        lo.refs = list(_lo.refs)
        lm.parse(lo)
        open_url(lo.refs[args.link-1])
    elif entry.link:
        open_url(entry.link)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Tool for reading the news logs \
of the recent daemon.')
    subparser = p.add_subparsers()
    list_p = subparser.add_parser('list', help='List the last news posts')
    list_p.add_argument('num', nargs='?', default=20, type=int)
    list_p.add_argument('--no-color', '-c', action='store_false', dest='color',
                help='Prevent the use of colors and ansii escape sequences')
    list_p.add_argument('--history', '-l', default=get_defhistory(),
                        help='Use another history file than $HOME/recent.log')
    list_p.set_defaults(func=do_list)
    read_p = subparser.add_parser('read', help='Show a complete post')
    read_p.add_argument('num', action='store', type=int)
    read_p.add_argument('--no-color', '-c', action='store_false', dest='color',
                   help='Prevent the use of colors and ansii escape sequences')
    read_p.add_argument('--history', '-l', default=get_defhistory(),
                        help='Use another history file than $HOME/recent.log')
    read_p.set_defaults(func=do_read)
    open_p = subparser.add_parser('open',
                                  help='Open a post in the default browser')
    open_p.add_argument('num', type=int)
    open_p.add_argument('link', nargs='?', type=int)
    open_p.add_argument('--no-color', '-c', action='store_false', dest='color',
                help='Prevent the use of colors and ansii escape sequences')
    open_p.add_argument('--history', '-l', default=get_defhistory(),
                        help='Use another history file than $HOME/recent.log')
    open_p.set_defaults(func=do_open)
    args = p.parse_args()
    if not os.path.isfile(args.history):
        f = open(args.history, 'w')
        f.close()
    if 'func' in args:
        args.func(args)
