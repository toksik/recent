import subprocess
import time

from lib.notifier.base import Notifier

class TmuxNotifier(Notifier):
    id = 'tmux'
    config_keys = ['wait']
    def notify(self, item):
        if item.author:
            text = '[%s] %s: %s'%(item.provider, item.author, item.title)
        else:
            text = '[%s] %s'%(item.provider, item.title)
        text = text.encode('utf-8')
        subprocess.call(['tmux','display-message',text])
        if self.config['wait'].isnumeric():
            time.sleep(int(self.config['wait']))
        else:
            time.sleep(3)
