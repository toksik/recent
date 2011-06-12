import subprocess
import time

import lib.markup.markup
from lib.notifier.base import Notifier

class TmuxNotifier(Notifier):
    id = 'tmux'
    def notify(self, item):
        lm = lib.markup.markup.LogMarkup()
        lo = lib.markup.markup.LogOutputMarkup(width=0)
        lm.buff = item.title
        lm.parse(lo)
        if item.author:
            text = '[%s] %s: %s'%(item.provider, item.author, lo.buff)
        else:
            text = '[%s] %s'%(item.provider, lo.buff)
        text = text.encode('utf-8')
        subprocess.call(['tmux','display-message',text])
