import subprocess
import time

import recent.markup.markup
from recent.notifier.base import Notifier

class TmuxNotifier(Notifier):
    id = 'tmux'
    def notify(self, item):
        lm = recent.markup.markup.LogMarkup()
        lo = recent.markup.markup.LogOutputMarkup(width=0)
        lm.buff = item.title
        lm.parse(lo)
        if item.author:
            text = '[%s] %s: %s'%(item.provider, item.author, lo.buff)
        else:
            text = '[%s] %s'%(item.provider, lo.buff)
        text = text.encode('utf-8')
        subprocess.call(['tmux','display-message',text])
