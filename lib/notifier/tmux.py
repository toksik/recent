import subprocess
import time

from lib.notifier.base import Notifier

class TmuxNotifier(Notifier):
    id = 'tmux'
    def notify(self, item):
        if item.author:
            text = '[%s] %s: %s'%(item.provider, item.author, item.title)
        else:
            text = '[%s] %s'%(item.provider, item.title)
        text = text.encode('utf-8')
        subprocess.call(['tmux','display-message',text])
