import subprocess
import os
import time

import recent.markup.markup
from recent.notifier.base import Notifier

class X11Notifier(Notifier):
    id = 'x11notify'
    deps = ['x11']
    config_keys = ['display']
    def notify(self, item):
        if self.config['display'].startswith(':'):
            os.putenv('DISPLAY', self.config['display'])
        elif 'DISPLAY' not in os.environ:
            os.putenv('DISPLAY', ':0')
        lm = recent.markup.markup.LogMarkup()
        lo = recent.markup.markup.LogOutputMarkup(width=0)
        lm.buff = item.title
        lm.parse(lo)
        title = lo.buff
        if len(title) > 200:
            title = title[:200]+'…'
        if item.author:
            text = '<b>%s</b>: %s'%(item.author, title)
        else:
            text = title
        text = text.encode('utf-8')
        p = subprocess.Popen(['notify-send',item.provider,text])
        p.wait()
